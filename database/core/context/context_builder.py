"""
Context Builder — builds audit context with business unit and session data.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime

from config.logging import get_logger
from database.core.storage.sqlite.sqlite_service import SQLiteService

logger = get_logger('context.builder')


@dataclass
class BusinessUnit:
    """Business unit entity."""
    id: int
    name: str
    company_id: Optional[int] = None
    code: Optional[str] = None
    
    @classmethod
    def from_row(cls, row: Dict[str, Any]) -> 'BusinessUnit':
        return cls(
            id=row.get('id', row.get('business_unit_id', 0)),
            name=row.get('name', 'Unknown'),
            company_id=row.get('company_id'),
            code=row.get('code')
        )


@dataclass
class SessionContext:
    """POS session context."""
    id: int
    name: str
    start_at: Optional[datetime] = None
    stop_at: Optional[datetime] = None
    state: str = 'unknown'
    config_id: Optional[int] = None
    business_unit_id: Optional[int] = None


@dataclass
class AuditContext:
    """
    Full audit context containing business unit, session, and environment data.
    BaseAudit expects: context.business_unit (BusinessUnit object)
    """
    business_unit: Optional[BusinessUnit] = None
    session: Optional[SessionContext] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    filters: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert context to dictionary for serialization."""
        return {
            'business_unit': {
                'id': self.business_unit.id if self.business_unit else None,
                'name': self.business_unit.name if self.business_unit else None,
            } if self.business_unit else None,
            'session': {
                'id': self.session.id if self.session else None,
                'name': self.session.name if self.session else None,
            } if self.session else None,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'filters': self.filters,
        }


class AuditContextBuilder:
    """
    Builds AuditContext from SQLite data.
    Used by BasePOSAudit and all audit modules.
    """
    
    def __init__(self, sqlite_service: SQLiteService = None):
        self.sqlite = sqlite_service or SQLiteService()
    
    def build(
        self,
        session_id: int = None,
        business_unit_id: int = None,
        date_from: str = None,
        date_to: str = None,
        **filters
    ) -> AuditContext:
        """
        Build audit context from database.
        
        Args:
            session_id: POS session ID
            business_unit_id: Business unit ID
            date_from: Start date (ISO format)
            date_to: End date (ISO format)
            **filters: Additional filters
        
        Returns:
            AuditContext with business_unit as object
        """
        context = AuditContext(
            date_from=date_from,
            date_to=date_to,
            filters=filters
        )
        
        # Load business unit
        if business_unit_id:
            context.business_unit = self._load_business_unit(business_unit_id)
        elif session_id:
            # Try to infer business unit from session
            context.session = self._load_session(session_id)
            if context.session and context.session.business_unit_id:
                context.business_unit = self._load_business_unit(
                    context.session.business_unit_id
                )
        
        # Load session if specified
        if session_id and not context.session:
            context.session = self._load_session(session_id)
        
        logger.debug(
            f"Context built: bu={context.business_unit}, "
            f"session={context.session}"
        )
        
        return context
    
    def _load_business_unit(self, bu_id: int) -> Optional[BusinessUnit]:
        """Load business unit from database."""
        try:
            rows = self.sqlite.query(
                table='business_units',
                conditions=[('id', '=', bu_id)],
                limit=1
            )
            if rows:
                return BusinessUnit.from_row(rows[0])
        except Exception as e:
            logger.warning(f"Failed to load business_unit {bu_id}: {e}")
        return None
    
    def _load_session(self, session_id: int) -> Optional[SessionContext]:
        """Load session from database."""
        try:
            rows = self.sqlite.query(
                table='pos_sessions',
                conditions=[('id', '=', session_id)],
                limit=1
            )
            if rows:
                row = rows[0]
                return SessionContext(
                    id=row.get('id', session_id),
                    name=row.get('name', f'Session {session_id}'),
                    start_at=row.get('start_at'),
                    stop_at=row.get('stop_at'),
                    state=row.get('state', 'unknown'),
                    config_id=row.get('config_id'),
                    business_unit_id=row.get('business_unit_id')
                )
        except Exception as e:
            logger.warning(f"Failed to load session {session_id}: {e}")
        return None
    
    def build_from_session_map(self, session_id: int) -> AuditContext:
        """
        Build context using session_business_units mapping table.
        Fallback for legacy schema.
        """
        context = AuditContext()
        
        try:
            # Try new table name first
            rows = self.sqlite.query(
                table='session_business_units',
                conditions=[('session_id', '=', session_id)],
                limit=1
            )
            if not rows:
                # Fallback to legacy name
                rows = self.sqlite.query(
                    table='session_business_unit_map',
                    conditions=[('session_id', '=', session_id)],
                    limit=1
                )
            
            if rows:
                bu_id = rows[0].get('business_unit_id')
                if bu_id:
                    context.business_unit = self._load_business_unit(bu_id)
                    context.session = self._load_session(session_id)
        except Exception as e:
            logger.warning(f"Session map lookup failed: {e}")
        
        return context


# Backward compatibility
SQLiteContextBuilder = AuditContextBuilder
ContextBuilder = AuditContextBuilder

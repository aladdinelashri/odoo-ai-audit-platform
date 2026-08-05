from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

class DatabasePool(ABC):
    @abstractmethod
    def get_connection(self):
        """Return a connection object (context manager or raw)."""
        pass

    @abstractmethod
    def execute_query(self, query: str, params: Optional[Tuple] = None) -> None:
        pass

    @abstractmethod
    def execute_many(self, query: str, params_list: List[Tuple]) -> None:
        pass

    @abstractmethod
    def fetch_one(self, query: str, params: Optional[Tuple] = None) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def fetch_all(self, query: str, params: Optional[Tuple] = None) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

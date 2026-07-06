from knowledge.pipeline.pipeline import KnowledgePipeline

from knowledge.builders.validation_builder import ValidationBuilder
from knowledge.builders.domain_builder import DomainBuilder
from knowledge.builders.risk_builder import RiskBuilder
from knowledge.builders.sensitive_fields_builder import SensitiveFieldsBuilder
from knowledge.builders.risk_factor_builder import RiskFactorBuilder
from knowledge.builders.risk_score_builder import RiskScoreBuilder
from knowledge.builders.audit_builder import AuditBuilder
from knowledge.builders.rule_builder import RuleBuilder


def create_pipeline():

    pipeline = KnowledgePipeline()

    pipeline.register_many([
        ValidationBuilder(),
        DomainBuilder(),
        RiskBuilder(),
        SensitiveFieldsBuilder(),
        RiskFactorBuilder(),
        RiskScoreBuilder(),
        AuditBuilder(),
        RuleBuilder(),
    ])

    return pipeline

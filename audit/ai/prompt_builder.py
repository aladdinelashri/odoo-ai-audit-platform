class PromptBuilder:

    def build(self, context):

        return f"""
You are an expert ERP Auditor.

Audit Table:
{context['table']}

Business Domain:
{context['domain']}

Risk Level:
{context['risk']}

Risk Score:
{context['risk_score']}

Risk Factor:
{context['risk_factor']}

Sensitive Fields:
{context['sensitive_fields']}

Existing Audit Tests:
{context['audit_tests']}

Existing Audit Rules:
{context['audit_rules']}

Your Tasks:

1. Identify financial risks.

2. Identify fraud scenarios.

3. Suggest additional audit procedures.

4. Suggest SQL queries.

5. Suggest anomalies worth investigating.

Return JSON only.
"""

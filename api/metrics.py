from prometheus_client import Counter, Histogram, Gauge

# Report execution metrics
REPORT_EXECUTIONS = Counter('report_executions_total', 'Total report executions', ['status'])
REPORT_DURATION = Histogram('report_execution_duration_seconds', 'Duration of report execution')
ACTIVE_JOBS = Gauge('scheduler_active_jobs', 'Number of active scheduled jobs')

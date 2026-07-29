-- scripts/add_report_tables.sql
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    query_ast TEXT NOT NULL,               -- JSON
    parameters TEXT,                       -- JSON array of {name, type, default}
    schedule TEXT,
    export_format TEXT DEFAULT 'json',
    recipients TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    last_run DATETIME,
    next_run DATETIME,
    status TEXT DEFAULT 'draft'
);

CREATE TABLE IF NOT EXISTS report_executions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id INTEGER REFERENCES reports(id) ON DELETE CASCADE,
    executed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    parameters TEXT,
    result_size INTEGER,
    execution_time_ms INTEGER,
    error TEXT,
    output_url TEXT
);

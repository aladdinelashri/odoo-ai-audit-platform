import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from flask import Flask, jsonify

from audit.reporting.executive_report import ExecutiveReport

app = Flask(__name__)


@app.route("/")
def home():

    return jsonify({
        "name": "Odoo AI Audit Platform",
        "version": "0.1.0",
        "status": "running"
    })


@app.route("/health")
def health():

    return jsonify({
        "status": "ok"
    })


@app.route("/api/executive")
def executive():

    report = ExecutiveReport().build()

    return jsonify(report)


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8080,
        debug=False
    )

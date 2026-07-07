from reporting.report_engine import ReportEngine


class JournalRiskRule:

    def __init__(self):

        self.engine = ReportEngine()

    def run(self):

        rows = self.engine.journal_risk()

        results = []

        for row in rows:

            score = 0

            reasons = []

            amount = float(row.get("total") or 0)

            if amount >= 100000:

                score += 50

                reasons.append("Very High Amount")

            partner = row.get("partner")

            if not partner:

                score += 20

                reasons.append("Missing Partner")

            journal = row.get("journal")

            if not journal:

                score += 20

                reasons.append("Missing Journal")

            if score >= 50:

                row["risk_score"] = score

                row["reasons"] = ", ".join(reasons)

                results.append(row)

        return results

class EvidenceCollector:

    def __init__(self):

        self.findings = []

    def add(self, finding):

        self.findings.append(finding)

    def summary(self):

        return {

            "total_rules": len(self.findings),

            "failed_rules": len(
                [
                    f
                    for f in self.findings
                    if f["status"] == "FAILED"
                ]
            ),

            "passed_rules": len(
                [
                    f
                    for f in self.findings
                    if f["status"] == "PASSED"
                ]
            ),

            "findings": self.findings,

        }

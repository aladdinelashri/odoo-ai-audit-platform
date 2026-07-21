class ReportComposer:

    def compose(
        self,
        title,
        sections
    ):

        return {
            "title": title,
            "sections": sections,
            "section_count": len(sections)
        }


    def add_section(
        self,
        report,
        section
    ):

        report["sections"].append(section)
        report["section_count"] = len(
            report["sections"]
        )

        return report

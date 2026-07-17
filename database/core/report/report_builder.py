class ReportBuilder:

    def build(self, title, data):

        return {
            "title": title,
            "rows": data,
            "count": len(data)
        }

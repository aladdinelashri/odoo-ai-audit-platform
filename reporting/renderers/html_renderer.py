class HTMLRenderer:

    def render(self, report):

        html = []

        html.append("<html>")
        html.append("<head>")
        html.append("<meta charset='utf-8'>")
        html.append(f"<title>{report['title']}</title>")
        html.append("</head>")
        html.append("<body>")

        html.append(f"<h1>{report['title']}</h1>")

        html.append("<table border='1' cellspacing='0' cellpadding='5'>")

        html.append("<tr>")

        for column in report["columns"]:

            html.append(f"<th>{column['title']}</th>")

        html.append("</tr>")

        for row in report["rows"]:

            html.append("<tr>")

            for column in report["columns"]:

                html.append(
                    f"<td>{row[column['field']]}</td>"
                )

            html.append("</tr>")

        html.append("</table>")

        html.append("</body>")

        html.append("</html>")

        return "\n".join(html)

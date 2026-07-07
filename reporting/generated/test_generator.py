from reporting.generator.report_generator import ReportGenerator

metadata = {

    "id": "journal_risk",

    "base_table": "account_move",

    "joins": [

        "account_journal",

        "res_partner"

    ],

    "columns": [

        "account_move.name",

        "account_move.date",

        "account_move.amount_total",

        "account_journal.name",

        "res_partner.name"

    ],

    "where":

        "account_move.state='posted'",

    "order":

        "account_move.amount_total DESC",

    "limit": 100

}

sql = ReportGenerator().generate(metadata)

print(sql)

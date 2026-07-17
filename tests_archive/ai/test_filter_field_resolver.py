from database.ai.filter_field_resolver import FilterFieldResolver

resolver = FilterFieldResolver()

print()
print("=" * 70)
print("FILTER FIELD RESOLVER")
print("=" * 70)
print()

filters = [

    {

        "field": None,

        "operator": ">",

        "value": 1000

    }

]

fields = [

    "amount_total"

]

result = resolver.resolve(

    "account.move",

    fields,

    filters

)

print(result)

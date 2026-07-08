class QueryOptimizer:

    def optimize(self, plan):

        optimized = dict(plan)

        # إزالة الـ JOIN المكررة
        optimized["joins"] = list(
            dict.fromkeys(plan["joins"])
        )

        # إزالة الحقول المكررة
        seen = set()

        fields = []

        for field in plan["select"]:

            key = field["alias"]

            if key in seen:
                continue

            seen.add(key)

            fields.append(field)

        optimized["select"] = fields

        return optimized

from database.ai.skills.numeric import NumericSkill
from database.ai.skills.date import DateSkill
from database.ai.skills.state import StateSkill
from database.ai.skills.aggregate import AggregateSkill


class SkillEngine:

    def __init__(self):

        self.skills = [

            NumericSkill(),

            DateSkill(),

            StateSkill()

        ]

        self.aggregate = AggregateSkill()

    # ---------------------------------------------------------

    def process(self, text, plan):

        for skill in self.skills:

            filters = skill.detect(

                text,

                plan

            )

            if filters:

                plan["filters"].extend(filters)

        plan = self.aggregate.detect(

            text,

            plan

        )

        return plan

from database.ai.skills.numeric import NumericSkill
from database.ai.skills.date import DateSkill
from database.ai.skills.state import StateSkill
from database.ai.skills.aggregate import AggregateSkill

from database.ai.skills.group import GroupSkill
from database.ai.skills.top import TopSkill


class SkillEngine:

    def __init__(self):

        self.skills = [

            NumericSkill(),

            DateSkill(),

            StateSkill(),

            GroupSkill(),

            TopSkill()

        ]

        self.aggregate = AggregateSkill()

    # ---------------------------------------------------------

    def process(self, text, plan):

        for skill in self.skills:

            result = skill.detect(

                text,

                plan

            )

            if result:

                if isinstance(result, dict):

                    plan.update(result)

                else:

                    plan["filters"].extend(result)

        plan = self.aggregate.detect(

            text,

            plan

        )

        return plan

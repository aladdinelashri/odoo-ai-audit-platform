class JoinBuilder:

    def __init__(self):

        self.joins = []

    def add(self, join):

        self.joins.append(join)

    def sql(self):

        return self.joins

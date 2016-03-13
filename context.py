class Context:

    def __init__(self):
        self.number_conditions = 0
        self.branch_location = []
        self.conditions_evaluation = []
        self.extra_else = 0
        self.extra_end = 0

    def set_location(self, value):
        self.branch_location[-1] = value

    def add_layer(self, condition_value):
        self.conditions_evaluation.append(condition_value)
        self.branch_location.append(True)
        self.number_conditions += 1

    def remove_layer(self):
        self.conditions_evaluation.pop()
        self.branch_location.pop()
        self.number_conditions -= 1

    def add_extra(self):
        self.extra_else += 1
        self.extra_end += 1

    def has_extra(self):
        return (self.extra_else > 0) or (self.extra_end > 0)

    def remove_extra_else(self):
        self.extra_else -= 1

    def remove_extra_end(self):
        self.extra_end -= 1

    def should_evaluate(self):
        return self.conditions_evaluation[-1] == self.branch_location[-1]
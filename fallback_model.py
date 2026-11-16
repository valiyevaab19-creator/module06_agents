class FallbackModel:
    """Use a backup model if the first model has no answer."""

    def __init__(self, first, second):
        self.first = first
        self.second = second

    def decide(self, instructions, history, tools):
        decision = self.first.decide(instructions, history, tools)
        if decision is None:
            return self.second.decide(instructions, history, tools)
        return decision

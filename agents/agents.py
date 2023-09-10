import collections

from things.Thing import Thing


class Agent(Thing):
    def __init__(self, program=None):
        self.alive = True
        self.bump = True
        self.holding = []
        self.performance = 0
        if program is None or not isinstance(program, collections.Callable):
            print("Can't find a valid program for {}, falling back to default.".format(self.__class__.__name__))

            def program(percept):
                return eval(input(":Percept={}; action? ".format(percept)))

        self.program = program

    def can_grab(self, thing):
        return False


# --------------------------------------------------
# Agent Programs

def rule_match(state, rules):
    """Find the first rule that matches state."""
    for rule in rules:
        if rule.matches(state):
            return rule


def SimpleReflexAgentProgram(rules, interpret_rules):
    def program(percept):
        state = interpret_rules(percept)
        rule = rule_match(state, rules)
        return rule.action

    return program


def ModelBasedReflexAgentProgram(rules, update_state, transition_model, sensor_model):
    def program(percept):
        program.state = update_state(program.state, program.action, percept, transition_model, sensor_model)
        rule = rule_match(program.state, rules)
        action = rule.action
        return action

    program.state = program.action = None
    return program

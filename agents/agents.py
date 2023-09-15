import collections

from things.thing import Thing


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


# Simple Reflex Agent Program

def SimpleReflexAgentProgram(rules, interpret_input):
    def program(percept):
        state = interpret_input(percept)
        rule = rule_match(state, rules)
        return rule.action

    return program


def ModelReflexAgentProgram(rules, update_state, transition_model, sensor_model):
    def program(percept):
        program.state = update_state(program.state, program.action, percept, transition_model, sensor_model)
        rule = rule_match(program.state, rules)
        return rule.action

    program.action = program.state = None
    return program

def rule_match(state, rules):
    for rule in rules:
        if rule.matches(state):
            return rule

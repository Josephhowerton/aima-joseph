import random

from agents.agents import Agent
from environments.environment import XYEnvironment
from things.thing import Thing
from time import sleep

LOC_A, LOC_B = ((0, 0), (0, 1))


class VacuumActions:
    CLEAN_DIRT = "CLEAN_DIRT"
    TURN_RIGHT = "TURN_RIGHT"
    TURN_LEFT = "TURN_LEFT"
    REST = "REST"


class State(Thing):
    pass


class Clean(State):
    pass


class Dirty(State):
    pass


class SimpleVacuumWorld(XYEnvironment):

    def __init__(self):
        super().__init__()
        self.status = {LOC_A: State, LOC_B: State}

    def percept(self, agent):
        return agent.location, self.status[agent.location]

    def execute_action(self, agent, action):
        sleep(1)
        if action == VacuumActions.CLEAN_DIRT and self.status[agent.location] == Dirty:
            print("cleaning")
            self.status[agent.location] = Clean
            agent.performance += 10
        elif action == VacuumActions.TURN_RIGHT:
            print("turning right")
            agent.location = LOC_B
            agent.performance -= 1
        elif action == VacuumActions.TURN_LEFT:
            print("turning left")
            agent.location = LOC_A
            agent.performance -= 1


def SimpleReflexVacuumAgent():
    def program(percept):
        location, status = percept
        if status == Dirty:
            return VacuumActions.CLEAN_DIRT
        elif location == LOC_A:
            return VacuumActions.TURN_RIGHT
        elif location == LOC_B:
            return VacuumActions.TURN_LEFT

    return Agent(program=program)


world = SimpleVacuumWorld()
vacuum_agent = SimpleReflexVacuumAgent()

print(world.status)

world.add_thing(vacuum_agent, random.choice([LOC_A, LOC_B]))

world.run(5)


test = []
world.status[LOC_A] = Dirty
print("Configuration 1 State: Location A {}, Location B {}".format(str(world.status[LOC_A]), str(world.status[LOC_B])))
world.run(5)
test.append(vacuum_agent.performance)

vacuum_agent.performance = 0
world.status[LOC_B] = Dirty
print("Configuration 2 State: Location A {}, Location B {}".format(str(world.status[LOC_A]), str(world.status[LOC_B])))
world.run(5)
test.append(vacuum_agent.performance)


vacuum_agent.performance = 0
world.status[LOC_A] = Dirty
world.status[LOC_B] = Dirty
print("Configuration 3 State: Location A {}, Location B {}".format(str(world.status[LOC_A]), str(world.status[LOC_B])))
world.run(5)
test.append(vacuum_agent.performance)

configuration = 0
totalPerformance = 0

for performance in test:
    configuration += 1
    totalPerformance += performance
    print("Configuration {} Performance: {}".format(configuration, performance))

print("Average performance: {}".format(totalPerformance / configuration))


# Adding internal state to reflex agent
def ModelBasedReflexVacuum():

    # keep internal state of the world: I don't think this is a model based agent
    model = {LOC_A: None, LOC_B: None}

    def program(percept):
        location, status = percept
        model[location] = status
        if model[LOC_A] == model[LOC_B] == Clean:
            return VacuumActions.REST
        elif model[location] == Dirty:
            return VacuumActions.CLEAN_DIRT
        elif location == LOC_A:
            return VacuumActions.TURN_RIGHT
        else:
            return VacuumActions.TURN_LEFT

    return Agent(program)


world.delete_thing(vacuum_agent)
vacuum_agent = ModelBasedReflexVacuum()

print(world.status)

world.add_thing(vacuum_agent, random.choice([LOC_A, LOC_B]))

world.run(5)


test = []
world.status[LOC_A] = Dirty
print("Configuration 1 State: Location A {}, Location B {}".format(str(world.status[LOC_A]), str(world.status[LOC_B])))
world.run(5)
test.append(vacuum_agent.performance)

vacuum_agent.performance = 0
world.status[LOC_B] = Dirty
print("Configuration 2 State: Location A {}, Location B {}".format(str(world.status[LOC_A]), str(world.status[LOC_B])))
world.run(5)
test.append(vacuum_agent.performance)


vacuum_agent.performance = 0
world.status[LOC_A] = Dirty
world.status[LOC_B] = Dirty
print("Configuration 3 State: Location A {}, Location B {}".format(str(world.status[LOC_A]), str(world.status[LOC_B])))
world.run(5)
test.append(vacuum_agent.performance)

configuration = 0
totalPerformance = 0

for performance in test:
    configuration += 1
    totalPerformance += performance
    print("Configuration {} Performance: {}".format(configuration, performance))

print("Average performance: {}".format(totalPerformance / configuration))

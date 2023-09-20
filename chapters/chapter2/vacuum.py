import random

from agents.agents import Agent, RandomAgentProgram
from environments.environment import XYEnvironment
from things.thing import Thing
from time import sleep

LOC_A = (0, 0)
LOC_B = (0, 1)
REST = "REST"
REST_VALUE = 3


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
        self.add_walls()
        
    def percept(self, agent):
        return agent.location, self.status[agent.location]

    def execute_action(self, agent, action):
        if action == VacuumActions.CLEAN_DIRT and self.status[agent.location] == Clean:
            print("cleaning: -5")
            agent.performance -= 5
        elif action == VacuumActions.CLEAN_DIRT and self.status[agent.location] == Dirty:
            print("cleaning: +10")
            self.status[agent.location] = Clean
            agent.performance += 10
        elif action == VacuumActions.TURN_RIGHT:
            print("TURN_RIGHT: -1")
            agent.location = LOC_B
            agent.performance -= 1
        elif action == VacuumActions.TURN_LEFT:
            print("TURN_LEFT: -1")
            agent.location = LOC_A
            agent.performance -= 1
        elif action == VacuumActions.REST:
            print("REST")
            sleep(1)


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


# -------------------------------------------------------------------------------------------------

def ModelBasedReflexVacuum():
    # keep internal state of the world: I don't think this is a model based agent
    model = {LOC_A: None, LOC_B: None}

    def program(percept):
        location, status = percept
        model[location] = status
        if model[LOC_A] == model[LOC_B] == Clean:
            return VacuumActions.REST
        elif status == Dirty:
            return VacuumActions.CLEAN_DIRT
        elif location == LOC_A:
            return VacuumActions.TURN_RIGHT
        else:
            return VacuumActions.TURN_LEFT

    return Agent(program)


test = []
# -------------------------------------------------
world_1 = SimpleVacuumWorld()
vacuum_agent = ModelBasedReflexVacuum()
world_1.add_thing(vacuum_agent, LOC_A)


world_1.status[LOC_A] = Dirty
world_1.status[LOC_B] = Clean
print("Model Based Agent")
print("Configuration 1 State: Location A Dirty, Location B Clean")
world_1.run(5)
test.append(vacuum_agent.performance)

# -----------------------------------------------------
world_2 = SimpleVacuumWorld()
vacuum_agent = ModelBasedReflexVacuum()
world_2.add_thing(vacuum_agent, LOC_A)

vacuum_agent.performance = 0
world_2.status[LOC_A] = Clean
world_2.status[LOC_B] = Dirty
print("Configuration 2 State: Location A Clean, Location B Dirty")
world_2.run(5)
test.append(vacuum_agent.performance)

# ------------------------------------------------------
world_3 = SimpleVacuumWorld()
vacuum_agent = ModelBasedReflexVacuum()
world_3.add_thing(vacuum_agent, LOC_A)

vacuum_agent.performance = 0
vacuum_agent.location = (0, 0)
world_3.status[LOC_A] = Dirty
world_3.status[LOC_B] = Dirty
print("Configuration 3 State: Location A Dirty, Location B Dirty")
world_3.run(5)
test.append(vacuum_agent.performance)

configuration = 0
totalPerformance = 0

for performance in test:
    configuration += 1
    totalPerformance += performance
    print("Configuration {} Performance: {}".format(configuration, performance))

print("Average performance: {}".format(totalPerformance / configuration))

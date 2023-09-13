from things.agents import *
from things.thing import *
from environments.environment import *


class VacuumWorld(Environment):
    def percept(self, agent):
        return self.list_things_at(agent.location)

    def execute_action(self, agent, action):
        if action == "clean dirt":
            items = self.list_things_at(agent.location, tclass=Dirt)
            if len(items) and agent.clean_dirt(items[0]):
                agent.performance += 10
                print("{} is cleaning dirt at {}".format(str(agent)[1:-1], agent.location))
                self.delete_thing(items[0])
        elif action == "rest":
            print("{} is resting at {}".format(str(agent)[1:-1], agent.location))
            agent.rest()
        elif action == "turn":
            agent.performance -= 1
            if agent.location == [0, 0]:
                print("{} is turning left at {}".format(str(agent)[1:-1], agent.location))
                agent.turn(Direction.L)
            else:
                print("{} is turning right at {}".format(str(agent)[1:-1], agent.location))
                agent.turn(Direction.R)


class Vacuum(Agent):
    location = [0, 0]
    direction = Direction("right")

    def __init__(self, program):
        super().__init__(program=program)

    def clean_dirt(self, thing):
        return isinstance(thing, Dirt)

    def rest(self):
        pass

    def turn(self, d):
        if d == Direction.L:
            self.location = [0, 1]
        else:
            self.location = [0, 0]


def SimpleVacuumProgram(percepts):
    for p in percepts:
        if isinstance(p, Dirt):
            return "clean dirt"
        if isinstance(p, Wall):
            return "turn"
    return "turn"


locA, locB = ([0, 0], [0, 1])
world = VacuumWorld()
vacuum = Vacuum(SimpleVacuumProgram)

dirt = Dirt()

world.add_thing(vacuum, vacuum.location)
world.add_thing(dirt, locB)

world.run(10)

print("{} performance measure: {}".format(str(vacuum)[1:-1], vacuum.performance))

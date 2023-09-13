import copy

from things.agents import Agent
from things.thing import Thing
import random
from environments.environment import Environment, GraphicEnvironment, Direction


class BlindDog(Agent):

    def __init__(self, program):
        super().__init__(program=program)
        self.location = [1, 1]
        self.direction = Direction("down")

    def move_forward(self):
        if self.direction.direction == Direction.R:
            self.location[0] += 1
        if self.direction.direction == Direction.L:
            self.location[0] -= 1
        if self.direction.direction == Direction.U:
            self.location[1] -= 1
        if self.direction.direction == Direction.D:
            self.location[1] += 1

    def turn(self, d):
        self.direction = self.direction + d

    def eat(self, thing):
        return isinstance(thing, Food)

    def drink(self, thing):
        return isinstance(thing, Water)


class Water(Thing):
    pass


class Food(Thing):
    pass


class Wall(Thing):
    pass


class Park(Environment):
    def percept(self, agent):
        things = self.list_things_at(agent.location)
        return things

    def execute_action(self, agent, action):
        if action == "move down":
            print("{} performing {} to {}".format(str(agent)[1:-1], action, agent.location))
            agent.move_down()
        elif action == "eat":
            items = self.list_things_at(agent.location, tclass=Food)
            if len(items) != 0:
                if agent.eat(items[0]):
                    print("{} ate {} at location {}".format(str(agent)[1:-1], str(items[0])[1:-1], agent.location))
                    self.delete_thing(items[0])
        else:
            items = self.list_things_at(agent.location, tclass=Water)
            if len(items) != 0:
                if agent.drink(items[0]):
                    print("{} drank {} at location {}".format(str(agent)[1:-1], str(items[0])[1:-1], agent.location))
                    self.delete_thing(items[0])

    def is_done(self):
        no_edibles = not any(isinstance(thing, Food) or isinstance(thing, Water) for thing in self.things)
        no_agents = not any(agent.is_alive() for agent in self.agents)
        return no_agents and no_edibles


def SimpleDogProgram(percepts):
    global choice
    for p in percepts:
        print(str(p))
        if isinstance(p, Food):
            return "eat"
        elif isinstance(p, Water):
            return "drink"
        elif isinstance(p, Wall):
            choice = random.choice((1, 2))
        else:
            choice = random.choice((1, 2, 3, 4))

    if choice == 1:
        return "turn right"
    elif choice == 2:
        return "turn left"
    else:
        return "move forward"


class Park2D(GraphicEnvironment):
    def percept(self, agent):
        things = self.list_things_at(agent.location)
        loc = copy.deepcopy(agent.location)
        if agent.direction.direction == Direction.R:
            loc[0] += 1
        if agent.direction.direction == Direction.L:
            loc[0] -= 1
        if agent.direction.direction == Direction.D:
            loc[1] += 1
        if agent.direction.direction == Direction.U:
            loc[1] -= 1
        if not self.is_inbounds(loc):
            things.append(Wall())
        return things

    def execute_action(self, agent, action):
        if action == "turn right":
            print("{} is {} to {}".format(str(agent)[1:-1], str(action), agent.location))
            agent.turn(Direction.R)
        if action == "turn left":
            print("{} is {} to {}".format(str(agent)[1:-1], str(action), agent.location))
            agent.turn(Direction.L)
        if action == "move forward":
            print("{} is {} to {}".format(str(agent)[1:-1], str(action), agent.location))
            agent.move_forward()
        elif action == "eat":
            items = self.list_things_at(agent.location, tclass=Food)
            if len(items) != 0:
                if agent.eat(items[0]):
                    print("{} is eating at location {}".format(str(agent)[1:-1], str(action), agent.location))
                    self.delete_thing(items[0])
        else:
            items = self.list_things_at(agent.location, tclass=Water)
            if len(items) != 0:
                if agent.drink(items[0]):
                    print("{} is drinking at location {}".format(str(agent)[1:-1], str(action), agent.location))
                    self.delete_thing(items[0])

    def is_done(self):
        no_edible = not any(isinstance(thing, Water) or isinstance(thing, Food) for thing in self.things)
        no_agents = not any(agent.is_alive for agent in self.agents)
        return no_edible and no_agents


dogPark2d = Park2D(10, 20, color={'BlindDog': (200, 0, 0), 'Water': (0, 200, 200), 'Food': (230, 115, 40)})

dog = BlindDog(SimpleDogProgram)

stream = Water()
puddle = Water()

hotDog = Food()
dogFood = Food()

# adding agent
dogPark2d.add_thing(dog, dog.location)

dogPark2d.add_thing(stream, location=[1, 2])
dogPark2d.add_thing(puddle, location=[10, 18])

dogPark2d.add_thing(hotDog, location=[9, 2])
dogPark2d.add_thing(dogFood, location=[14, 16])

dogPark2d.run(steps=200)

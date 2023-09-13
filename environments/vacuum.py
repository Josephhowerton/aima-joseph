from environment import *
from agents.vacuum import *
class SimpleVacuumWorld(XYEnvironment):
    def percept(self, agent):
        return self.list_things_at(agent.location)

    def execute_action(self, agent, action):
        if action == VacuumActions.CLEAN_DIRT:
            items = self.list_things_at(agent.location)
            if len(items) and agent.clean_dirt(items[0]):
                self.delete_thing(items[0])


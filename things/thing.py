class Thing:
    def __repr__(self):
        return '<{}>'.format(getattr(self, "__name__", self.__class__.__name__))

    def is_alive(self):
        return hasattr(self, "alive") and self.alive

    def show_state(self):
        print("I do not have an internal state")

    def display(self, canvas, x, y, width, height):
        pass


class Obstacle(Thing):
    pass


class Wall(Thing):
    pass


class Dirt(Thing):
    pass

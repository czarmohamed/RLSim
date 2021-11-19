from mesa import Agent
from movement import MovingAgent


# Inherits the behavior from MovingAgent
class RandomAgent1(MovingAgent):

    resource = 0 # The initial amount of resource for an agent

    def __init__(self, unique_id, pos, model, moore, resource=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.resource = resource

# Step: Moves the agent in a random direction, Observes environment and collects resource if available
    def step(self):

        self.random_move()

        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        fruit_patch = [obj for obj in this_cell if isinstance(obj, Fruit)][0]
        if fruit_patch.fully_ripe:
            self.resource += 1
            fruit_patch.fully_ripe = False
        else:
            self.resource += 0

# Same as RandomAgent1 Required Additional class definition for scheduler
class RandomAgent2(MovingAgent):

    resource = 0

    def __init__(self, unique_id, pos, model, moore, resource=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.resource = resource

    def step(self):

        self.random_move()

        this_cell = self.model.grid.get_cell_list_contents([self.pos])

        fruit_patch = [obj for obj in this_cell if isinstance(obj, Fruit)][0]
        if fruit_patch.fully_ripe:
            self.resource += 1
            fruit_patch.fully_ripe = False
        else:
            self.resource += 0

# Fruit patch representing a resource within the environment
class Fruit(Agent):

    def __init__(self, unique_id, pos, model, fully_ripe, countdown):

        super().__init__(unique_id, model)
        self.fully_ripe = fully_ripe
        self.countdown = countdown # Time left to when the fruit can be harvested
        self.pos = pos

    # Step: if fruit is fully ripe then it can be harvested, else reduce the countdown
    def step(self):
        if not self.fully_ripe:
            if self.countdown <= 0:
                # Set as fully grown
                self.fully_ripe = True
                self.countdown = self.model.fruit_ripening_time
            else:
                self.countdown -= 1

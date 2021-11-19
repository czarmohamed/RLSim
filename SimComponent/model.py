from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from agents import RandomAgent1, RandomAgent2, Fruit
from scheduler import RandomScheduling

# The game environment. Also initializes all agents and controls the flow of the game

class HarvestGame(Model):
    height = 20
    width = 20
    initial_agents1 = 10
    initial_agents2 = 10
    fruit_ripening_time = 10
    verbose = False
    description = (
        "Harvest Game Visualization."
    )

    def __init__(
            self,
            height=20,
            width=20,
            initial_agents1=10,
            initial_agents2=10,
            fruit_ripening_time=10,
    ):

        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_agents1 = initial_agents1
        self.initial_agents2 = initial_agents2

        self.fruit_ripening_time = fruit_ripening_time

        self.schedule = RandomScheduling(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {
                "RandomAgent1": lambda m: m.schedule.get_resource(RandomAgent1),
                "RandomAgent2": lambda m: m.schedule.get_resource(RandomAgent2),
            }
        )

        # Create agents:
        for i in range(self.initial_agents1):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            resource = 0
            agent = RandomAgent1(self.next_id(), (x, y), self, False, resource)
            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)
        for i in range(self.initial_agents2):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            resource = 0
            agent = RandomAgent2(self.next_id(), (x, y), self, False, resource)
            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)

        # Create fruit patches
        for agent, x, y in self.grid.coord_iter():
            # random = self.random.randrange(100)
            fully_ripe = False
            countdown = self.random.randrange(self.fruit_ripening_time)
            if countdown == 0:
                fully_ripe = True
            patch = Fruit(self.next_id(), (x, y), self, fully_ripe, countdown)
            self.grid.place_agent(patch, (x, y))
            self.schedule.add(patch)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print(
                [
                    self.schedule.time,

                    self.schedule.get_resource(RandomAgent1),
                    self.schedule.get_resource(RandomAgent2),
                ]
            )


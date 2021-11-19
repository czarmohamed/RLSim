from mesa import Agent

# General class for random 4 directional movement of agents
# Used as a base class for the RandomAgent
class MovingAgent(Agent):
    grid = None
    x = None
    y = None
    moore = False

    def __init__(self, unique_id, pos, model, moore=False):

        super().__init__(unique_id, model)
        # Agents position on the multigrid
        self.pos = pos
        # Used for 8 directional movement. Set as false to match the learning environment
        self.moore = moore

    def random_move(self):
        # Select Cell to move
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, False)
        next_move = self.random.choice(next_moves)
        self.model.grid.move_agent(self, next_move)
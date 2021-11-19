from collections import defaultdict
from mesa.time import RandomActivation

# Random Scheduler which dictates the order of agent actions
# Order is reshuffled every step
# Equivalent to NetLogo "ask breed" which is the default ABM behavior
# Requires all agents to possess a step function

class RandomScheduling(RandomActivation):

    def __init__(self, model):
        super().__init__(model)
        self.agent_schedule = defaultdict(dict)

    def add(self, agent):
        # Add agent to schedule

        self._agents[agent.unique_id] = agent
        agent_type = type(agent)
        self.agent_schedule[agent_type][agent.unique_id] = agent

    def remove(self, agent):
        # Remove agent from schedule

        del self._agents[agent.unique_id]
        agent_type = type(agent)
        del self.agent_schedule[agent_type][agent.unique_id]

    def step(self, by_type=True):
        # Executes the step function of every agent of a specific type in random order
        if by_type:
            for agent_type in self.agent_schedule:
                self.step_type(agent_type)
            self.steps += 1
            self.time += 1
        else:
            super().step()

    def step_type(self, type):
        # Shuffle order of all agent by type
        agent_keys = list(self.agent_schedule[type].keys())
        self.model.random.shuffle(agent_keys)
        for agent_key in agent_keys:
            self.agent_schedule[type][agent_key].step()

    def get_type_count(self, type_class):
        # returns the current number of agents of each type
        return len(self.agent_schedule[type_class].values())

    def get_resource(self, type_class):
        resource = 0
        for agent in self.agent_schedule[type_class]:
            current_agent = self.agent_schedule[type_class][agent]
            resource += current_agent.resource

        return resource

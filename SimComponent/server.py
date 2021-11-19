from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter
from agents import RandomAgent1, RandomAgent2, Fruit
from model import HarvestGame

# Builds the Server for visualization
def multi_agent_visualization(agent):
    if agent is None:
        return

# Agent portrayals within the environment
    portrayal = {}

    if type(agent) is RandomAgent1:
        portrayal["Shape"] = "resources/man.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    if type(agent) is RandomAgent2:
        portrayal["Shape"] = "resources/woman.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2

    elif type(agent) is Fruit:
        if agent.fully_ripe:
            portrayal["Shape"] = "resources/fruit1.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 0

    return portrayal

# Initialize the multigrid
canvas_element = CanvasGrid(multi_agent_visualization, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "RandomAgent1", "Color": "#AA0000"}, {"Label": "RandomAgent2", "Color": "#666666"}]
)

# Default model parameters
model_params = {
    "fruit_ripening_time": UserSettableParameter(
        "slider", "Fruit Ripening Time", 150, 1, 300),
    "initial_agents1": UserSettableParameter(
        "slider", "Initial RandomAgent1 Population", 10, 0, 50),
    "initial_agents2": UserSettableParameter(
        "slider", "Initial RandomAgent2 Population", 10, 0, 50),

}

server = ModularServer(
    HarvestGame, [canvas_element, chart_element], "Harvest Game", model_params
)
server.port = 8521

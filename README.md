# RLSim
2 components 
SimComponent: Creates a simulation of the Implemented Harvest Game in the Browser
TestComponent: Trains a MultiAgent Reinforcement Learning Environment of the Harvest Game
# Run 
main.py file in the SimComponent. Opens browser window to display the simulation. <br />

GridTestTrain.py in the TestComponent. Will run the Multi Agent Deep Reinforcement Learning Model<br />

# Dependencies
mesa, Gym, Ray, tensorboard, numpy
# Data 
stored in a local directory /ray_results\my_exp. 
To view tensorboard graphs for the training enter tensorboard --logdir=~/ray_results\my_exp\experimentfolder into the command prompt.

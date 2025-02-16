from main import *

data = RubikStats.read_csv("CubeTime - Default Session.csv")
data = RubikStats(data)
print(data)
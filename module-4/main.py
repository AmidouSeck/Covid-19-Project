# importing the required module
import matplotlib.pyplot as plt
from Loader import *

# x axis values
p = Loader()
res = p.progressionParRegion("touba")
print(res)
x = res[0]
y = res[1]

# plotting the points
plt.plot(x, y)

# naming the x axis
plt.xlabel('x - axis')
# naming the y axis
plt.ylabel('y - axis')

# giving a title to my graph
plt.title('corona!')

# function to show the plot
plt.show()

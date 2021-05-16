# importing the required module
import matplotlib.pyplot as plt
from Loader import *

# x axis values
p = Loader()
res = p.progressionParRegion("dakar")
print(res)
x = res[0]
y = res[1]

# plotting the points
plt.plot(x, y)


# res = p.evolutionCasRegion("touba")
# x = res[0]
# y = res[1]

# plt.plot(x,y)

# res = p.progressionGenerale("casPositifs")
# x = res[0]
# y = res[1]

# plt.plot(x,y)
# naming the x axis
plt.xlabel('mois')
# naming the y axis
plt.ylabel('cas')

# giving a title to my graph
plt.title('Touba')

# function to show the plot
plt.show()

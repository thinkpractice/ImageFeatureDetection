from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import csv

histogram = []
with open(r"/home/tjadejong/Documents/CBS/ZonnePanelen/histogram.csv", 'r') as csvFile:
    csvReader = csv.reader(csvFile)
    for row in csvReader:
        r, g, b, v = row
        histogram.append((r,g,b))


fig = pyplot.figure()
ax = Axes3D(fig)

r = []
g = []
b = []
colors = []
for row in histogram:
    x,y,z = row
    r.append(x)
    g.append(y)
    b.append(z)
    colors.append(row)
ax.scatter(r, g, b) #, color=colors)
pyplot.show()
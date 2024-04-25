import numpy as np
import matplotlib.pyplot as plt

# Generate 15 random points
n = 15
points = [(-3.21058089e+01, -2.88302437e+01),
 (-1.80221227e+01, -3.57180523e+00),
 ( 2.55418206e+01,  2.96651222e+01),
 ( 1.27399985e+01, -3.73658911e+01),
 (-1.92782318e+01,  3.84368653e+01),
 ( 1.96874507e+01, -2.47539404e+01),
 ( 3.20027696e+00,  3.40681428e+01),
 ( 4.32294298e+00, -8.01133588e+00),
 (-1.37535788e+01,  1.88445528e+01),
 ( 1.14866975e+01,  4.64783593e+00),
 (-7.18515965e+00, -4.27640252e+01),
 ( 3.12523970e+01,  1.00812417e+01),
 (-2.80187346e+01, -6.38942097e+00),
 ( 3.37861998e+01, -1.10922332e-03),
 (-2.36541476e+01,  1.59440109e+01)]
print(points)
points = np.array(points)
# Create a graph by connecting all points to each other
edges = []
for i in range(n):
    for j in range(i + 1, n):
        edges.append((i, j))

# Plot the points
plt.scatter(points[:, 0], points[:, 1], color='blue')

tour = [
                 3,
                5,
                10,
                0,
                12,
                1,
                7,
                9,
                13,
                11,
                2,
                6,
                4,
                8,
                14
            ]
rolled_tour = np.roll(tour, -1)
edges_weights = [
                  15.0,
                    33.0,
                    29.0,
                    23.0,
                    11.0,
                    23.0,
                    15.0,
                    23.0,
                    11.0,
                    21.0,
                    23.0,
                    23.0,
                    21.0,
                    11.0,
                    64.0
                ]
edges_to_highlight = []
for i in range(len(tour)):
  edges_to_highlight.append((tour[i], rolled_tour[i]))


# Plot the edges
for edge in edges:
    plt.plot([points[edge[0], 0], points[edge[1], 0]], [points[edge[0], 1], points[edge[1], 1]], color='#dddddd')
i = 0
for edge in edges_to_highlight:
    plt.annotate("", xy=points[edge[1]], xytext=points[edge[0]], arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="red"))
    # plt.plot([points[edge[0], 0], points[edge[1], 0]], [points[edge[0], 1], points[edge[1], 1]], color='red')
    plt.text(((points[edge[0], 0] + points[edge[1], 0]) / 2)*0.75, (points[edge[0], 1] + points[edge[1], 1]) / 2, str(edges_weights[i]), color='black')
    # plt.text(points[edge[0], 0], points[edge[0], 1], str("999"), color='black')
    i += 1

plt.title('Graph of {} Points'.format(n))
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
plt.show()
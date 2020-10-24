import matplotlib.pyplot as plt
y = []
for i in range(50):

    plt.xlabel("X axis label")
    plt.ylabel("Y axis label")
    y.append(i)
    plt.plot(y)
    plt.draw()
    plt.pause(0.0001)
    plt.clf()
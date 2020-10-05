import matplotlib.pyplot as plt
fin = open("plot", "r")

OUR = []
GRE = []
RAN = []
our = fin.readline().split(" ")[:-1]
gre = fin.readline().split(" ")[:-1]
ran = fin.readline().split(" ")[:-1]

for i in our:
  OUR.append(float(i))
for i in gre:
  GRE.append(float(i))
for i in ran:
  RAN.append(float(i))

TIME = list(range(10, (len(OUR)+1)*10, 10))
plt.title("average CM number of each cluster")
plt.xlabel("time")
plt.ylabel("#CM")
#plt.ylim(0,20)
plt.plot(TIME, OUR, label="OUR")
plt.plot(TIME, GRE, label="GRE")
plt.plot(TIME, RAN, label="RAN")
plt.legend()
plt.show()

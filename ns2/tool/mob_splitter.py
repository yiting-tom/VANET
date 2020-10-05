import sys

#===================================================mob file
finput = sys.argv[1]
foutputMob = sys.argv[2]
foutputNod = sys.argv[3]
print("Writing ... "+foutputNod)
print("Writing ... "+foutputMob)

if finput == "":
  finput = "../mob.tcl"
if foutputNod == "":
  foutputNod = "out.nod.tcl"
if foutputMob == "":
  foutputMob = "out.mob.tcl"

fin = open(finput, "r")
foutNod = open(foutputNod, "w")
foutMob = open(foutputMob, "w")

lines = []
block = []
startNode = sys.argv[4]
endNode   = sys.argv[5]
startTime = sys.argv[6]
endTime   = sys.argv[7]


for line in fin:
  lines.append(line)

# initial file
for i in range(len(lines)):
  block = lines[i].split(" ")

  if len(block) == 4:
    if float((block[0].split("("))[1].split(")")[0]) >= float(startNode) and \
       float((block[0].split("("))[1].split(")")[0]) <= float(endNode):
      for j in block:
        foutNod.write(j.rstrip("\n") + " ")
      foutNod.write("\n")


# mobilitys file
  #limit time
  else:
    if float(block[2]) <= float(endTime) and \
       float(block[2]) >= float(startTime) and \
       float((block[3].split("("))[1].split(")")[0]) >= float(startNode) and \
       float((block[3].split("("))[1].split(")")[0]) <= float(endNode):
      for j in block:
        foutMob.write(j.rstrip("\n") + " ")
      foutMob.write("\n")

print("Complete ... "+foutputNod)
print("Complete ... "+foutputMob)

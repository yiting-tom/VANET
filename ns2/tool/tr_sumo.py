import sys
from operator import attrgetter, itemgetter

class Car:
  nu = str
  time = str
  x  = str
  y  = str
  an = 0
  sp = 0
  end = "-"
  def __init__(self, block):
    self.nu = int((block[3].split("(")[1]).split(")")[0])
    self.time = float(block[2])
    self.x  = float(block[5])
    self.y  = float(block[6])
  def info(self):
    return ("%s %s %s %s %s %s %s" %(self.time, self.nu, self.x, self.y, self.an, self.sp, self.end))

finputTr  = sys.argv[1]
finputSu  = sys.argv[2]
foutput   = sys.argv[3]
startTime = float(sys.argv[4])
endTime   = float(sys.argv[5])
startNode = int(sys.argv[7])
endNode   = int(sys.argv[7])

if finputTr == "":
  finputTr = "out/main.tr.ana"
if finputSu == "":
  finputSu = "out/out.mob.sor.tcl"
if foutput == "":
  foutput = "out/main.trSumo"

finTr = open(finputTr, "r")
finSu = open(finputSu, "r")
fout = open(foutput, "a")

lines = []
block = []
Table = []
count = 0
flag = 0

preNode = startNode
maxTime = float(startTime)
minTime = float(endTime)
preTime = 0

for line in finSu: lines.append(line)
for i in range(len(lines)): 
  block = lines[i].split(" ")
  Table.append(Car(block))

lines = []

for line in finTr:
  fout.write(line)

print("Writing ..."+foutput)

carlist = []
for car in Table:
  if not(car.nu in carlist):
    carlist.append(car.nu)
    fout.write("A "+car.info()+"\n")
  else: 
    fout.write("M "+car.info()+"\n")

print("Complete ..."+foutput)

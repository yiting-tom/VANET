from CarClass import Car
from EVENT import *
from Game import *
import sys

#-----------------------------------------------------
# CarTable # name    endtime    x     y     speed     angular    state     cluster     Pcm[]     Pch[]     Pd[]
#-----------------------------------------------------
#GMs = {"RAN":"r--", "GRE":"g--", "OUR":"b--"}
#TIME = []
#for i in range(1, 21):
#  TIME.append(i*10)

GM = sys.argv[1]
#for GM in GMs:
timeTrace = []
lines = []
line = []
fin = open("../main.out", "r")
fout = open("conclusion/%s.out"%(GM), "w")
fout.write("%s\n"%(GM))

print("%s running..."%(GM))
for line in fin:
  lines.append(line)

#for i in range(1000):
for i in range(len(lines)):
  print('%.3f%%'%(i/len(lines)*100), end='\r')
  block = lines[i].split(" ")
  event = block[0]

  if event is "M":
    EVENT_M(block, GM)
  elif event is "D":
    EVENT_D(block)
  elif event is "r":
    EVENT_r(block)
  elif event is "L":
    EVENT_L(block)
fin.close()
print("%s done"%(GM), end="\r")
writeConclusion(fout)
fout.close()

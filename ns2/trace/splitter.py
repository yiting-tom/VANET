import sys
import math 
def tran(x, center):
  theta = math.atan2(x[1]-center[1], x[0]-center[0])/math.pi*180
  if theta < 0 : return str(360 + theta)
  return str(theta)

finput1 = "main.out"
foutput1 = "main.srDM"
fin = open(finput1, "r")
fout = open(foutput1, "w")

line = []
lines = []
block = []
nodeList = []
event = str
time = str
rec = str
sen = str

for line in fin:
  lines.append(line)

for i in range(len(lines)):
  block = lines[i].split(" ")
  if block[0] is "s" or block[0] is "r" or block[0] is "D":
    block = lines[i].split(" ")
    event = block[0]
    time = block[1]

#-------------------------------SEN
    if event == "s":
      sen = int(block[2].split("_")[1], base=10)
      rec = int(block[10], base=16)
      if sen in nodeList and rec in nodeList:
        if rec == "ffffffff": fout.write("%s %s %d -1 -\n" %(event, time, sen))
        else: fout.write("%s %s %d %s -\n" %(event, time, sen, str(rec)))
#-------------------------------REC
    elif event == "r":
      rec = int(block[2].split("_")[1], base=10)
      sen = int(block[11], base=16)
      if sen in nodeList and rec in nodeList:
        if rec == "ffffffff": fout.write("%s %s %d -1 -\n" %(event, time, sen))
        else: fout.write("%s %s %d %s -\n" %(event, time, sen, str(rec)))
#-------------------------------DRO
    elif event == "D":
      sen = int(block[11], base=16)
      rec = int(block[10], base=16)
      if sen in nodeList and rec in nodeList:
        fout.write("%s %s %d %d -\n" %(event, time, sen, rec))
#-------------------------------MOV
  elif block[0] == "M":
    event = block[0]
    time = block[1]
    node = block[2]
    pX = float((block[3].split("(")[1]).split(",")[0])
    pY = float((block[4].split(",")[0]))
    pre = [pX, pY]
    cX = float((block[6].split("(")[1]).split(",")[0])
    cY = float((block[7].split(",")[0]).split(")")[0])
    cur = [cX, cY]
    an = tran(pre, cur)
    spX = cX - pX
    spY = cY - pY
    fout.write("%s %s %s %f %f %f %f %s -\n" %(event, time, node, cX, cY, spX, spY, an))
    if not(node in nodeList): nodeList.append(int(node))

import sys

from operator import itemgetter, attrgetter



class Node:
  minTime = float
  maxTime = float
  node = int
  def __init__(self, node, minTime, maxTime):
    self.node = node
    self.minTime = minTime
    self.maxTime = maxTime



def AGENT(agent, n1, n2, sign=""):
    return str(str(sign)+str(agent)+"_("+str(n1)+"-"+str(n2)+") ")



def NODE(node):
    return str("$node_("+str(node)+") ")



def TIME(time):
    return str("at " + str(time) + " ")



#===================================================mob file
finput = sys.argv[1]
foutputAct = sys.argv[2]
print("Writing ...", foutputAct)

if finput == "":
  finput = "out.mob.sor.tcl"
if foutputAct == "":
  foutputAct = "out.act.tcl"
foutput = "out/main.trSumo"

fin = open(finput, "r")
foutAct = open(foutputAct, "w")
fout = open(foutput, "w")


startNode = int(sys.argv[3])
endNode = int(sys.argv[4])+1
startTime = float(sys.argv[5])
endTime = float(sys.argv[6])
APPpro = str(sys.argv[7])
NLpro = str(sys.argv[8])


# link activitys file

Table = []
lines = []
block = []
preNode = startNode
maxTime = startTime
minTime = endTime
preTime = 0

#print("N\tstartTime\tendTime")
for line in fin:
  lines.append(line)

for i in range(len(lines)):
  block = lines[i].split(" ")
  curNode = int((block[3].split("(")[1]).split(")")[0])
  curTime = float(block[2])

  maxTime = max(preTime, maxTime)
  minTime = min(preTime, minTime)
  if curNode != preNode or i == len(lines)-1:
    if i == len(lines)-1:
      if (curTime>maxTime): maxTime = curTime
      if (curTime<minTime): minTime = curTime
    if maxTime > endTime: maxTime = endTime
    if minTime < startTime: minTime = startTime
    Table.append(Node(preNode, minTime, maxTime))
    maxTime = int(startTime)
    minTime = int(endTime)
  preTime = curTime
  preNode = curNode
Table = sorted(Table, key = attrgetter('node'))

##############################################
# instruction
# $ns_ at 1.0 "$node color black"
# $ns_ at 1.0 "$ns_ attach-agent $node_($i) $udp_($i-$j)"
# $ns_ at 1.0 "$ns_ detach-agent $node_($i) $udp_($i-$j)"
# $ns_ at 1.0 "$ns_ connect $udp $null"
# $ns_ at 1.0 "$cbr attach-agent $udp"
# $ns_ at 1.0 "$cbr start"
# $ns_ at 1.0 "$cbr end"
###############################################
for n in Table:
  NS = str(block[0] + " ")
  foutAct.write(NS+TIME(n.minTime)+"\""+NODE(n.node)+" color black\"\n")
  foutAct.write(NS+TIME(n.maxTime)+"\""+NODE(n.node)+" color white\"\n")
  for j in Table:
    if n != j:
#      print(str(n.node) + " " + str(j.node))
##NL
      foutAct.write("set "+AGENT(NLpro,n.node,j.node)+"[new Agent/UDP]\n")
      foutAct.write("set "+AGENT("null",j.node,n.node)+"[new Agent/Null]\n")

      time = max(n.minTime, j.minTime)
      foutAct.write(NS+TIME(time)+"\""+NS+"attach-agent "+NODE(n.node)+AGENT(NLpro,n.node,j.node,"$")+"\"\n")
      foutAct.write(NS+TIME(time)+"\""+NS+"attach-agent "+NODE(j.node)+AGENT("null",j.node,n.node,"$")+"\"\n")
      foutAct.write(NS+TIME(time)+"\""+NS+"connect "+AGENT(NLpro,n.node,j.node,"$")+AGENT("null",j.node,n.node,"$")+"\"\n")

      time = min(n.maxTime, j.maxTime)
      foutAct.write(NS+TIME(time)+"\""+NS+"detach-agent "+NODE(n.node)+AGENT(NLpro,n.node,j.node,"$")+"\"\n")
      foutAct.write(NS+TIME(time)+"\""+NS+"detach-agent "+NODE(j.node)+AGENT("null",j.node,n.node,"$")+"\"\n")
##APP
      foutAct.write("set "+AGENT(APPpro,n.node,j.node)+"[new Application/Traffic/CBR]\n")

      time = max(n.minTime, j.minTime)
      foutAct.write(NS+TIME(time)+"\""+AGENT(APPpro,n.node,j.node,"$")+"attach-agent "+AGENT(NLpro,n.node,j.node,"$")+"\"\n")
      foutAct.write(NS+TIME(time)+"\""+AGENT(APPpro,n.node,j.node,"$")+"start\"\n")
#      foutAct.write(NS+TIME+"\""+AGENT(APPpro,n.node,j.node,"$")+"detach-agent "+AGENT(NLpro,n.node,j.node,"$")+"\"\n")

#      time = min(n.maxTime, j.maxTime)
#      foutAct.write(NS+TIME(time)+"\""+AGENT(APPpro,n.node,j.node,"$")+"stop\"\n")
#############################################

for i in Table:
  print(str(i.node)+"\t"+str(i.minTime)+"\t\t"+str(i.maxTime))
  fout.write("d "+str(float(i.maxTime-0.0000001))+" "+str(i.node)+" -\n")
for i in Table:
  print(str(float(i.maxTime)-0.0000001)+" "+str(i.node)+" -")


print("Complete ...", foutputAct)

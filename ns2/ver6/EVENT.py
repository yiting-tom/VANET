from CarClass import Car 
from Game import *
import queue

############################# GLOBAL_VAR  #############################
#--------------------------GLOBAL_VARIABLES
CarDict = {}  # {'Cid : <Car>'}
CHDict  = {}  # {'Cid : <Car>'}
ConnectCount = 0
DisconnectCount = 0
cluCreateCount = 0
cluDeleteCount = 0
maxCluCount = 0
TR = 300
gameMode = str
cluCountDict = {}
totalNodeNum = 50
sample = 10
ColorDict = {}
ColorQ = queue.Queue(totalNodeNum)
for i in range(2):
  ColorQ.put("Blue")
  ColorQ.put("violet")
  ColorQ.put("red")
  ColorQ.put("pink")
  ColorQ.put("yellow")
  ColorQ.put("orange")
  ColorQ.put("green")
  ColorQ.put("magenta")
  ColorQ.put("brown")
  ColorQ.put("dodgerblue")
  ColorQ.put("darkviolet")
  ColorQ.put("darkblue")
  ColorQ.put("darkred")
  ColorQ.put("darkorange")
  ColorQ.put("darkgreen")
  ColorQ.put("darkmagenta")
fnam = False

#--------------------------EVENT_M
def EVENT_L(block):
  curTime = float(block[1])
  Cid = int(block[2])
  global fnam

  if CarDict[Cid].parentCar != -1:
    print("END : %f (%d %s) #child:%d parent (%d %s)"%(curTime, Cid,CarDict[Cid].state, len(CarDict[Cid].childList), CarDict[Cid].parentCar.Cid, CarDict[Cid].parentCar.state))
  else:
    print("END : %f (%d %s) #child:%d parent (NULL)"%(curTime, Cid,CarDict[Cid].state, len(CarDict[Cid].childList)))

# remove delCar pak 
  for carNid in CarDict:
    carN = CarDict[carNid]
    if Cid in carN.Pun:
      del carN.Pun[Cid]
    if Cid in carN.Pcm:
      del carN.Pcm[Cid]
    if Cid in carN.Pch:
      del carN.Pch[Cid]

# disconnect with parent
  if CarDict[Cid].parentCar != -1:
    CAR_DISCONNECT(CarDict[Cid], CarDict[Cid].parentCar, curTime)

# disconnect with children
  if len(CarDict[Cid].childList) != 0:
    for child in CarDict[Cid].childList:
      print("(%d, %s)"%(child.Cid, child.state), end = " ")
      CAR_DISCONNECT(child, CarDict[Cid], curTime)
      EVENT_TIMEUP(child, curTime, True)

  del CarDict[Cid]
  fnam.write("n -t %f -s %d -x -3199 -y -3199 -c white\n"%(curTime, Cid))
  fnam.write("m -t %f -s %d -n m1 -X\n"%(curTime, Cid))

def EVENT_M(block, GM):
  global gameMode
  global fnam

  gameMode = GM
  if not(fnam): fnam = open("%s.nam"%GM, "a")
  curTime = float(block[1])
  Cid  = int(block[2])
  x    = float(block[3])
  y    = float(block[4])
  Vx   = float(block[5])
  Vy   = float(block[6])
  an   = float(block[7])

# new Car come in
  if not(Cid in CarDict):
    fnam.write("n -t %f -s %d -x %f -y %f -c black\n"%(curTime,Cid,x,y))
    newCar = Car(curTime, Cid, x, y, Vx, Vy, an)
    CarDict[Cid] = newCar
    print("STA : %f %d"%(curTime, Cid))
# previous Car come in
  else:
  # check time up
    EVENT_TIMEUP(CarDict[Cid], curTime)
    CarDict[Cid].changePVA(x, y, Vx, Vy, an)


#--------------------------EVENT_r
def EVENT_r(block):
  curTime = float(block[1])
  sen = int(block[3])
  rec = int(block[2])

  if not(sen in CarDict and rec in CarDict): return 
  rec = CarDict[rec]
#   check time up
  EVENT_TIMEUP(rec, curTime)
#   mantain Pch and Pcm
  if CarDict[sen].state == "UN":
    if not(sen in rec.Pun): rec.Pun[sen] = 1
    else: rec.Pun[sen] += 1
  elif CarDict[sen].state == "CM":
    if not(sen in rec.Pcm): rec.Pcm[sen] = 1
    else: rec.Pcm[sen] += 1
  elif CarDict[sen].state == "CH":
    if not(sen in rec.Pch): rec.Pch[sen] = 1
    else: rec.Pch[sen] += 1

#--------------------------EVENT_D
def EVENT_D(block):
  curTime = float(block[1])
  sen = int(block[3])
  rec = int(block[2])

  if not(rec in CarDict): return 
# check time up
  EVENT_TIMEUP(CarDict[rec], curTime)
# maintain drop packet dict
  if not(sen in CarDict[rec].Pd): CarDict[rec].Pd[sen] = 1
  else: CarDict[rec].Pd[sen] += 1


################################# CAR ################################
def CAR_CONNECT(car, parent, curTime):
  global ConnectCount

#  print("\033[1;32;40m  CAR_CONNECT    : (%d, %s) (%d, %s)\033[1;37;0m"%(car.Cid, car.state, parent.Cid, parent.state))

  if car in parent.childList:
    print("  CAR_CONNECT ERROR : %d already in %d childList"%(car.Cid, parent.Cid))
    exit()
  if car in parent.getAncientList():
    print("  CAR_CONNECT ERROR : (%d, %s) is (%d, %s)'s ancient"%(car.Cid, car.state, parent.Cid, parent.state))
    exit()

  ConnectCount += 1
  fnam.write("m -t %f -s %d -n m1 -X\n"%(curTime, car.Cid))
  if car.parentCar != -1: 
    car.parentCar.childList.remove(car)
  if car.state == "CH":
    CAR_CLU_DELETE(car, curTime)
  car.changeParent(curTime, parent)
  if car.state != "CM": car.changeState(curTime, "CM")
  car.changeLayer(curTime, parent.layer+1)
  parent.childList.append(car)
  car.changeClu(curTime, parent.Clid)
  
  fnam.write("m -t %f -s %d -n m1 -c %s -h circle\n"%(curTime, car.Cid, ColorDict[parent.Clid]))


  print("\033[1;32;40m  CAR_CONNECT    : (%d, %s)-(%d, %s) --- OK\033[1;37;0m"%(car.Cid, car.state, parent.Cid, parent.state))
#  printCluDict()

def CAR_DISCONNECT(car, parent, curTime):

#  print("\033[1;31;40m  CAR_DISCONNECT : (%d, %s)-(%d, %s) \033[1;37;0m"%(car.Cid, car.state,parent.Cid, parent.state))
  if type(car) != type(Car()) or  type(parent) != type(Car()):
    print("  CAR_DISCONNECT ERROR : type ERROR type(car) : %s type(parent) : %s"%(type(car), type(parent)))
    exit()
  if car.state != "CM":
    print("  CAR_DISCONNECT ERROR : (%d,%s) state error %d"%(car.Cid, car.state,parent.Cid))
    exit()

  reCCchildren = []


  if len(car.childList) == 0:
    if car.parentCar != -1: car.changeParent(curTime, -1)
    car.changeState(curTime, "UN")
    car.changeLayer(curTime, -1)
    car.childList = []
    print("\033[1;31;40m  CAR_DISCONNECT : (%d, %s) (%d, %s) --- OK\033[1;37;0m"%(car.Cid, car.state, parent.Cid, parent.state))
  else:
    CAR_CLU_CREATE(car, curTime)

  if car in parent.childList:
    parent.childList.remove(car)
  fnam.write("m -t %f -s %d -n m1 -c black -h circle\n"%(curTime, car.Cid))


#  printCluDict()


def CAR_CLU_CREATE(car, curTime):
  global cluCreateCount

#  print("\033[0;37;42m  CAR_CLU_CREATE : (%d, %s) #CLU:%d\033[1;37;0m"%(car.Cid, car.state, len(CHDict)))
  if car in CHDict:
    print("CAR_CLU_CREATE ERROR : (%d, %s) already in CHDict"%(car.Cid, car.state))
    exit()

  cluCreateCount += 1

  ColorDict[car.Cid] = ColorQ.get()
  car.changeClu(curTime, car.Cid)
  fnam.write("m -t %f -s %d -n m1 -c %s -h circle\n"%(curTime,car.Cid,ColorDict[car.Cid]))


  car.changeState(curTime, "CH")
  car.changeLayer(curTime, 0)
  if car.parentCar != -1: car.changeParent(curTime, -1)
  CHDict[car] = car.getLinkQ().qsize()

  global maxCluCount
  if len(CHDict) > maxCluCount: maxCluCount = len(CHDict)

#  print("\033[0;37;42m  CAR_CLU_CREATE : (%d, %s) #CLU:%d --- OK\033[1;37;0m"%(car.Cid, car.state, len(CHDict)))


def CAR_CLU_DELETE(CH, curTime):
  global cluDeleteCount

#  print("\033[0;37;41m  CAR_CLU_DELETE : (%d, %s #%d)\033[1;37;0m"%(CH.Cid, CH.state, len(CHDict)))
  if CH.state != "CH":
    print("CAR_CLU_CREATE ERROR : (%d, %s) not a CH"%(car.Cid, car.state))
    exit()


  cluDeleteCount += 1
  del CHDict[CH]  
  ColorQ.put(ColorDict[CH.Cid])
  del ColorDict[CH.Cid]

#  print("\033[0;37;41m  CAR_CLU_DELETE : (%d, %s #%d) --- OK\033[1;37;0m"%(CH.Cid, CH.state, len(CHDict)))


def CAR_MAINTAIN_CHILDREN(car, curTime):
#  print("CAR_MAINTAIN_CHILDREN : (%d, %s)"%(car.Cid, car.state))
  for child in car.childList:
    if not(child in car.Pcm) and not(child in car.Pch):
      if car.parentCar != -1:
        if not(car in car.parentCar.Pcm) and not(car in car.parentCar.Pch):
          global DisconnectCount
          DisconnectCount += 1
          CAR_DISCONNECT(child, car, curTime)
          EVENT_TIMEUP(child, curTime, True)
#  print("CAR_MAINTAIN_CHILDREN : (%d, %s) --- OK"%(car.Cid, car.state))


#################################  EVENT  ################################
#--------------------------EVENT_TIMEUP
def EVENT_TIMEUP(car, curTime, force = False):
  global gameMode

  if (curTime+1)%sample == 0:
    if not(curTime in cluCountDict):
      cluCountDict[curTime] = len(CarDict)/len(CHDict)

  if car.isTimeUp(curTime) or force: 
#    print("\nisTimeUp : %f (%d, %s)"%(curTime, car.Cid, car.state))
    CAR_MAINTAIN_CHILDREN(car, curTime)
    
#================== UN ==================
    if car.state is "UN":
      if len(car.Pcm) + len(car.Pch) == 0:
        CAR_CLU_CREATE(car, curTime)
#      elif gameMode == "RAN" and int(curTime)%2 == 1:
#        CAR_CLU_CREATE(car, curTime)
      else:
        newParentList = GAME_CAR(car, CarDict, TR, gameMode, totalNodeNum)
        CAR_CONNECT(car, newParentList[0], curTime)
##================== CM ==================
    elif car.state is "CM":
      flag = True
      if len(car.Pcm) + len(car.Pch) != 0:
        newParentList = GAME_CAR(car, CarDict, TR, gameMode, totalNodeNum)
        for newParent in newParentList:
          if not(newParent in car.getGrandsonList()):
            if newParent != car.parentCar: 
#              print("new parent : (%d, %s)"%(newParent.Cid, newParent.state))
              flag = False
              CAR_CONNECT(car, newParent, curTime)
              break
#        if flag: print("    No change parent")
##================== CH ==================
    elif car.state is "CH":
      flag = True
      if len(car.Pcm) + len(car.Pch) != 0:
        newParentList = GAME_CAR(car, CarDict, TR, gameMode, totalNodeNum)
        for newParent in newParentList:
          if not(newParent in car.getGrandsonList()):
#            print(car.getGrandsonList())
#            print("new parent : (%d, %s)"%(newParent.Cid, newParent.state))
            flag = False
            CAR_CONNECT(car, newParent, curTime)
            break
#        if flag: print("    No change parent")

##================== ERROR ==================
    else: 
      print("STATE ERROR")
      exit()

    car.resetPak()
    car.resetTime(curTime)
#    print("isTimeUp : %f (%d, %s) --- OK\n"%(curTime, car.Cid, car.state))

################################  PRINT  ################################
#--------------------------printCarDict
def printCarDict():
  for i in CarDict: CarDict[i].printCar()

#--------------------------printCluDict
def printCluDict():
  print("printCluDict: #%d"%(len(CHDict)))
  for CH in CHDict:
    print("  (%d, %s #%d) "%(CH.Cid, CH.state, CHDict[CH]), end="")
    Q = CH.getLinkQ()
    Q.get()
    Qlist = list(Q.queue)
    preLayer = -1
    while not(Q.empty()):
      link = Q.get()
      if preLayer != link[0].layer: 
        print()
      print("    (%2d, %s %2d)"%(link[0].Cid, link[0].state, link[0].layer), end="-")
      print("(%2d, %s %2d) "%(link[1].Cid, link[1].state, link[1].layer), end="")
      preLayer = link[0].layer
    print()
  print()
#--------------------------printConclustion
def writeConclusion(fout):
  global ConnectCount
  global DisconnectCount
  global cluCreateCount
  global cluDeleteCount
  global maxCluCount
  global cluCountDict

  foutCon = open("conclusion/plot", "a")
  fout.write("Car Disonnect count : %d\n"%(DisconnectCount))
  fout.write("Cluster Create count : %d\n"%(cluCreateCount))
  fout.write("Cluster Delete count : %d\n"%(cluDeleteCount))
  fout.write("Maximum Cluster Count : %d\n"%(maxCluCount))
  for i in cluCountDict:
    fout.write(str(i) + " : " + str(cluCountDict[i])+"\n")
    foutCon.write(str(cluCountDict[i]) + " ")
  foutCon.write("\n")
  foutCon.close()

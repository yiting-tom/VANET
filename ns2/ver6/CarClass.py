import queue
Tun = 1
Tcm = 5
Tch = 5
totalNodeNum = 50
class Car:
  Clid = -1
  Cid = -1
  clock = 0
  X = 0
  y = 0
  Vx = 0
  Vy = 0
  angular = 0
  state = "UN"
  layer = -1
  Q = False

  Pun = {}     # {'Cid : pakCount'}
  Pcm = {}     # {'Cid : pakCount'}
  Pch = {}     # {'Cid : pakCount'}
  Pd  = {}     # {'Cid : pakCount'}

  parentCar = -1
  childList = []
  fout = open("CarInfo/stateChange", "a+")


  def __init__(self, curTime=0, Cid=-1, x=0, y=0, Vx=0, Vy=0, an=0):
    self.clock = curTime+Tun
    self.Clid = -1
    self.Cid = Cid
    self.X  = x
    self.Y  = y
    self.Vx  = Vx
    self.Vy  = Vy
    self.angular = an
    self.Pcm = {}
    self.Pch = {}
    self.Pd  = {}
    self.childList = []

  def changePVA(self, x, y, Vx, Vy, an):
    self.X  = x
    self.Y  = y
    self.Vx  = Vx
    self.Vy  = Vy
    self.angular = an

  def changeState(self, curTime, state):
#    print("    changeState: (%d, %s) %s" %(self.Cid, self.state, state))
    if self.Cid == -1:
      print("changeState ERROR : -1 car.Cid")
      exit()
    if self.state == state:
      print("changeState ERROR : same state")
      exit()

    self.fout.write("%f %d %s %s -\n"%(curTime, self.Cid, self.state, state))

    if state == "UN":
      self.clock = curTime+Tun
      self.state = state
    elif state == "CM":
      self.clock = curTime+Tcm
      self.state = state
    elif state == "CH":
      self.clock = curTime+Tch
      self.state = state

#    print("    changeState: (%d, %s) --- OK" %(self.Cid, self.state))

  def changeLayer(self, curTime, layer):
#    print("    changeLayer : (%d, %s, %d)"%(self.Cid, self.state, self.layer))
    if self.layer <= -1 and layer < 0:
      print("changeLayer ERROR : (%d, %s) layer is %d"%(self.Cid, self.state, self.layer))
      exit()

    self.layer = layer

#    print("    changeLayer : (%d, %s, %d) --- OK"%(self.Cid, self.state, self.layer))
    if len(self.childList) == 0: return 0
    else:
      for child in self.childList:
        child.changeLayer(curTime, self.layer+1)

  def changeClu(self, curTime, Clid):
    self.Clid = Clid

    if len(self.childList) == 0: return 0
    else:
      for child in self.childList:
        child.changeClu(curTime, Clid)


  def changeParent(self, curTime, parent):
#    if parent == -1:
#      print("    changeParent : (%d, %s)-(%d, %s)"%(self.Cid, self.state, self.parentCar.Cid, self.parentCar.state))
#    else:
#      if self.parentCar == -1:
#        print("    changeParent : (%d, %s)-(-1) (%d, %s)"%(self.Cid, self.state, parent.Cid, parent.state))
#      else:
#        print("    changeParent : (%d, %s)-(%d, %s) (%d, %s)"%(self.Cid, self.state, self.parentCar.Cid, self.parentCar.state, parent.Cid, parent.state))
    self.parentCar = parent
#    if parent == -1:
#      print("    changeParent : (%d, %s)-(-1) --- OK"%(self.Cid, self.state))
#    else:
#      print("    changeParent : (%d, %s)-(%d, %s) --- OK"%(self.Cid, self.state, self.parentCar.Cid, self.parentCar.state))


  def getPakCar(self, pak, CarTable):
    PakList = []
    if pak == "Pcm":
      for i in self.Pcm:
        PakList.append(CarTable[i])
    elif pak == "Pch":
      for i in self.Pch:
        PakList.append(CarTable[i])
    elif pak == "Pd":
      for i in self.Pd:
        PakList.append(CarTable[i])
    else:
      print("getPakCar ERROR : '%s' pak invalid"%(pak))
      exit()
    return PakList


  def isTimeUp(self, curTime):
    if float(curTime) >= self.clock: return True
    return False

  def resetPak(self):
    self.Pch = {}
    self.Pcm = {}
    self.Pd  = {}

  def resetTime(self, curTime):
    if self.state == "UN": addTime = Tun
    elif self.state == "CM": addTime = Tcm
    else: addTime = Tch
    self.clock = curTime + addTime


  def getLinkQ(self):
    linkQueue = queue.Queue(totalNodeNum)
    carQueue = queue.Queue(totalNodeNum)
    carQueue.put(self)

    while not(carQueue.empty()):
      parent = carQueue.get()
      link = []
      link.append(parent.parentCar)
      link.append(parent)
      linkQueue.put(link)
      for car in parent.childList:
        carQueue.put(car)

    return linkQueue


  def findCHr(self):
    if self.parentCar == -1: return self
    return self.parentCar.findCHr()

  def getCH(self):
    if self.state == "UN":
      print("getCH ERROR : (%d, %s) is a UN"%(self.Cid, self.state))
      exit()
    return self.findCHr()

  def getAncientList(self):
    car = self
    ancientList = []

    while car.parentCar != -1:
      ancientList.append(car.parentCar)
      car = car.parentCar

    return ancientList


  def getGrandsonList(self):
    carQ = queue.Queue(totalNodeNum)
    carQ.put(self)
    grandsonList = []

    while not(carQ.empty()):
      car = carQ.get()
      if len(car.childList) != 0:
        for child in car.childList:
          grandsonList.append(child)
          carQ.put(child)

    return grandsonList


  def printClu(self):
    if self.state != "CH":
      print("printClu ERROR : (%d,%s) isnot a CH"%(self.Cid, self.state))
      exit()
    Q = self.findLinkQ()
    while not(Q.empty()):
      link = Q.get()
      if link[0] != -1:
        print("(%d, %d) "%(link[0].Cid, link[1].Cid),end="")
    print()


  def printCar(self):
    print("%d %s %d"%(self.Cid, self.state, self.layer))
    print("Pun : ", end = "")
    for i in self.Pun:
      print("(%d : %d)"%(i, self.Pun[i]), end = " ")
    print("\nPcm : ", end = "")
    for i in self.Pcm:
      print("(%d : %d)"%(i, self.Pcm[i]), end = " ")
    print("\nPch : ", end = "")
    for i in self.Pch:
      print("(%d : %d)"%(i, self.Pch[i]), end = " ")
    print("\n")

#  def getCluList(self, CarList, ClusterTable):
#    CluList = []
#    for car in CarList:
#      CluList.append(ClusterTable[car.Clid])
#    return CluList

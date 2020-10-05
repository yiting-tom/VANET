from CarClass import Car
import queue


def LLT(car0, car1, TR):
    dVx = car1.Vx - car0.Vx
    dVy = car1.Vy - car0.Vy
    dX  = car1.X  - car0.X
    dY  = car1.Y  - car0.Y

    if dVx == 0 : dVx = 0.000001
    if dVy == 0 : dVy = 0.000001


    return (((-(dVx)*(dX) + abs(dVx)*TR)/(dVx**2))**2 +\
            ((-(dVy)*(dY) + abs(dVy)*TR)/(dVy**2))**2) ** (0.5)

def LLTav(car1, TR, totalNodeNum):
  LLTtotal = 0
  carQueue = queue.Queue(totalNodeNum)
  CH = car1.getCH()
  linkQueue = CH.getLinkQ()
  linkNum = linkQueue.qsize() - 1

  while not(linkQueue.empty()):
    link = linkQueue.get()
    if link[0] != -1: LLTtotal += LLT(link[0], link[1], TR)
  if linkNum != 0: return LLTtotal/linkNum
  else : return 0



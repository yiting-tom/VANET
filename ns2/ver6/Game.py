from CarClass import Car
from Factor import *
import operator
import math
import random

LLTF = 0.5        #LLT effect
ANGF = 0.3        #angular effect
PCLF = 0.1        #previous cluster effect
PCHF = 1        #previous CH effect



def GAME_CAR_OUR(car, CarDict, TR, totalNodeNum):
#    print("        GAME_CAR_OUR : (%d,%s)"%(car.Cid, car.state))

    CarList = car.Pch
    CarList.update(car.Pcm)

    if len(CarList) == 0:
        print("        GAME_CAR_OUR ERROR : CarList is empty")
        exit()
    candCar = {}
    bestCHvalue = float("-inf")
    for carNum in CarList:
        carN = CarDict[carNum]
        if carN.state != "UN":
            CH = carN.getCH()
#            print("            carN: %d\tCH: %d"%(carN.Cid, CH.Cid))
#        else:
#            print("            carN: %d\tCH: -1"%(carN.Cid))

        if not(carN in candCar): candCar[carN] = 0


        # base on number of cars in cluster
#        GameValue = ((-1/90)*(len(car.CluMember)**2) + 5)
        GameValue = 0

# PAK effect
        if carNum in car.Pch: GameValue += car.Pch[carNum]
        if carNum in car.Pcm: GameValue += car.Pch[carNum]
        if carNum in car.Pd : GameValue -= car.Pch[carNum]
#        print("                PAK effect : %3f"%(GameValue))

# LLT effect

        dLLT = LLT(car, carN, TR) - LLTav(carN, TR, totalNodeNum)
        if dLLT > 0: GameValue *= ((1+dLLT)*LLTF)
        if dLLT < 0: GameValue *= ((1+dLLT)*LLTF)
#        print("                LLT effect : %.3f\t%.3f\tF:%.2f"%(dLLT, GameValue, LLTF))

# angluar effect
        dANG = abs(carN.angular - car.angular)
        if dANG > 180: dANG = 360-dANG

        if dANG < 45 : GameValue += GameValue*(1-(dANG)/45)*ANGF
        if dANG > 135: GameValue -= GameValue*(1-((180-dANG)/45))*ANGF
#        print("                ANG effect : %.3f\t%.3f\tF:%.2f"%(dANG, GameValue, ANGF))


## previous cluster effect
#        if carN is car.getCH() : GameValue *= PCLF
#        print("PCL effect : %3f"%(GameValue))

# carN and car in same Clustering
        if carN.state != "UN":
            if car is carN.getCH():
                GameValue *= (1+PCHF)
    #            print("                PCH effect : %.3f\t\tF:%.2f"%(GameValue, PCHF))

        candCar[carN] += GameValue

    CCarList = []
    CValList = []
    for i in candCar:
        CCarList.append(i)
        CValList.append(candCar[i])

    for i in range(len(CValList)):
        for j in range(len(CValList)):
            if CValList[i] > CValList[j]:
                CValList[i], CValList[j] = CValList[j], CValList[i]
                CCarList[i], CCarList[j] = CCarList[j], CCarList[i]

#    for i in range(len(CValList)):
#        print("(%2d, %.3f) "%(CCarList[i].Cid, CValList[i]), end="")

#    print()

    return    CCarList



def GAME_CAR_RANDOM(car, CarDict, TR):
#    print("GAME_CAR_RANDOM : (%d,%s)"%(car.Cid, car.state))
    carList = car.Pch
    carList.update(car.Pcm)
    CCarList = []

    for carN in carList:
        CCarList.append(CarDict[carN])

    random.shuffle(CCarList)

    return CCarList



def GAME_CAR_LID(car, CarDict, TR):
#    print("GAME_CAR_RANDOM : (%d,%s)"%(car.Cid, car.state))
    carList = car.Pch
    carList.update(car.Pcm)
    CCarList = []

    for carN in sorted(carList):
        CCarList.append(CarDict[carN])

    return CCarList



def GAME_CAR_HCC(car, CarDict, TR):
#    print("GAME_CAR_RANDOM : (%d,%s)"%(car.Cid, car.state))
    carList = car.Pch
    carList.update(car.Pcm)
    carList = list(carList.keys())
    CCarList = []
    tmp_dict = {}
    car_list = []
    car_child_len = []

    for carN in carList:
        car_list.append(CarDict[carN])
        car_child_len.append(len(CarDict[carN].childList))

    for i, val_i in enumerate(car_child_len):
        for j, val_j in enumerate(car_child_len):
            if val_i > val_j:
                car_list[i], car_list[j] = car_list[j], car_list[i]
            elif val_i == val_j:
                if carList[i] < carList[j]:
                    car_list[i], car_list[j] = car_list[j], car_list[i]

    return car_list



def GAME_CAR_GREEDY(car, CarDict, TR):
#    print("GAME_CAR_GREEDY : (%d,%s)"%(car.Cid, car.state))
    CarList = car.Pch
    CarList.update(car.Pcm)
    candCar = {}

    s_CarList = sorted(CarList.items(), key=lambda item: item[1], reverse=True)
    CCarList = []
    for carN in s_CarList:
        CCarList.append(CarDict[carN[0]])

#    for carNum in CarList:
#        carN = CarDict[carNum]
#        CH = carN.getCH()
#        GameValue = 0
##        print("            carN : %d\tCH : %d"%(carN.Cid, CH.Cid))
#
#        if not(carN in candCar): candCar[carN] = 0
#
#        if carNum in car.Pch: GameValue += car.Pch[carNum]
#        if carNum in car.Pcm: GameValue += car.Pch[carNum]
#        if carNum in car.Pd : GameValue -= car.Pch[carNum]
##        print("        PAK effect : %3f"%(GameValue))
#        candCar[carN] += GameValue
#
#    CCarList = []
#    CValList = []
#    for i in candCar:
#        CCarList.append(i)
#        CValList.append(candCar[i])
#
#    for i in range(len(CValList)):
#        for j in range(len(CValList)):
#            if CValList[i] > CValList[j]:
#                CValList[i], CValList[j] = CValList[j], CValList[i]
#                CCarList[i], CCarList[j] = CCarList[j], CCarList[i]

    return CCarList



def GAME_CAR_LLT(car, CarDict, TR, totalNodeNum):
#    print("GAME_CAR_GREEDY : (%d,%s)"%(car.Cid, car.state))
    CarList = car.Pch
    CarList.update(car.Pcm)
    candCar = {}

    for carNum in CarList:
        carN = CarDict[carNum]
#        print("            carN : %d\tCH : %d"%(carN.Cid, CH.Cid))
        if not(carN in candCar): candCar[carN] = 0
#        print("        PAK effect : %3f"%(GameValue))
# LLT effect
        candCar[carN] += LLT(car, carN, TR) - LLTav(carN, TR, totalNodeNum)

    CCarList = []
    CValList = []
    for i in candCar:
        CCarList.append(i)
        CValList.append(candCar[i])

    for i in range(len(CValList)):
        for j in range(len(CValList)):
            if CValList[i] > CValList[j]:
                CValList[i], CValList[j] = CValList[j], CValList[i]
                CCarList[i], CCarList[j] = CCarList[j], CCarList[i]

    return CCarList




def GAME_CAR(car, CarDict, TR, mod, totalNodeNum):
    if mod == "OUR":
        return GAME_CAR_OUR(car, CarDict, TR, totalNodeNum)
    elif mod == "RAN":
        return GAME_CAR_RANDOM(car, CarDict, TR)
    elif mod == "LID":
        return GAME_CAR_LID(car, CarDict, TR)
    elif mod == "HCC":
        return GAME_CAR_HCC(car, CarDict, TR)
    elif mod == "GRE":
        return GAME_CAR_GREEDY(car, CarDict, TR)
    elif mod == "LLT":
        return GAME_CAR_LLT(car, CarDict, TR, totalNodeNum)
    else:
     print("GAME_CAR ERROR : invalid mod value")
     exit()



def GAME_CLU_OUR(carQ, TR):
#    print("GAME_CLU_OUR : Qsize: %d"%(carQ.qsize()))
    valueList = {}
    LLTtotal = 0
    while not(carQ.empty()): valueList[carQ.get()] = 0

    for car in carList:
        for carN in carList:
            if car != carN:
                valueList[car] += LLT(car, carN, TR)

    bestCar = max(valueList.items(), key=operator.itemgetter(1))[0]

#    print("GAME_CLU_OUR : (%d, %s) --- OK"%(bestCar.Cid, bestCar.state))
    return bestCar


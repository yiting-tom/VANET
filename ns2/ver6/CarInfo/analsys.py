import sys

filenames = ["OUR", "GRE", "HCC", "LID"]
fout_name = "analsys.out"
for filename in filenames:
    fin = open("./stateChange."+filename, "r")
    fout = open(fout_name, "a+")

    line_num = 1
    line = fin.readline()
    CM = 0
    CH = 0
    UN = 0

    CM_switch = 0.1
    CH_switch = 0.1
    UN_switch = 0.1

    CM_list = []
    CH_list = []
    time_cache = []

    car_dict = {}
    while line:
        sp = line.split(" ")
        time = float(sp[0])
        Cid = sp[1]
        pre_state = sp[2]
        cur_state = sp[3]



        if Cid in car_dict.keys():

#            if cur_state == car_dict[Cid][1]:
                #print(f"time={time} Cid={Cid} pre={pre_state} cur={cur_state}")

            if pre_state == "CM":
                CM += time - car_dict[Cid][0]
                CM_switch += 1

            if pre_state == "CH":
                CH += time - car_dict[Cid][0]
                CH_switch += 1

            if pre_state == "UN":
                UN += time - car_dict[Cid][0]
                UN_switch += 1


#        if time not in time_cache:
#            time_cache.append(time)
#            fout.write(f"{filename} {time} {CM/CM_switch} {CH/CH_switch} \n")
#            print(f"{filename} CM = {CM/CM_switch}, CH = {CH/CH_switch}")
#            print(f"CMs = {CM_switch} CHs = {CH_switch} UNs = {UN_switch}")
#            print()



        car_dict[Cid] = [time, pre_state, cur_state]
        line_num += 1
        line = fin.readline()
#    for k, v in car_dict.items():
#        print(f"{k} = {v}")
#    print(f"{filename} CM = {CM/CM_switch}, CH = {CH/CH_switch}, UN = {UN/UN_switch}")
    print(f"{filename} CM = {CM/CM_switch}, CH = {CH/CH_switch}")
    print(f"CMs = {CM_switch} CHs = {CH_switch} UNs = {UN_switch}")
    print()

import queue
CAR_INFO = "info/state_change.txt"

class Car:
    fout = open(CAR_INFO, "a+")

    def __init__(self, time, Cid, x, y, Vx, Vy, an):
        self.clock = time+Tin
        self.Clid = -1
        self.Cid = Cid
        self.x = x
        self.y = y
        self.Vx = Vx
        self.Vy = Vy
        self.an = an
        self.Pcm = {}
        self.Pch = {}
        self.Pd = {}
        self.childList = []

    def change_PVA(self, x, y, Vx, Vy, an):
        """ change position, speed, angular

            @Return None
        """
        self.x = x
        self.y = y
        self.Vx = Vx
        self.Vy = Vy
        self.an = an

    def change_state(self, time, state):
        """ change state and record at CAR_INFO

            @Return None
        """



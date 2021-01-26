import time
import csv

class CaptureTime:
    def __init__(self):
        self.running = True
        self.pressTime = None
        self.releaseTime = None
        self.password = ".tie5Roanl"
        self.dicTimes = dict()
        self.user = None
        self.entryFreq = 2
        self.entryCount = 1
        self.passOk = None
        self.dicKeystrokesTimes = None
        self.dicCSVTimes = dict()
        self.listTimes = list()
        self.sessionFreq = 0
        self.sessionCount = 1
    
    def __call__(self):
        self.running = True
        self.pressTime = None
        self.releaseTime = None
        self.password = ".tie5Roanl"
        self.dicTimes = dict()
        self.user = None
        self.entryFreq = 2
        self.entryCount = 1
        self.passOk = None
        self.dicKeystrokesTimes = None
        self.dicCSVTimes = dict()
        self.listTimes = list()
        self.sessionFreq = 0
        self.sessionCount = 1

    def setUser(self, user):
        self.user = user

    def setEntryFreq(self, entryFreq):
        self.entryFreq = entryFreq
    
    def setSessionFreq(self, sessionFreq):
        self.sessionFreq = sessionFreq

    #20210123 MH: this function will be excecuted every time a key is pressed 
    def KeyDownEvent(self, event ):
        try:
            if event.Key == "Return":
                self.dicTimes[event.Key]["keyDown"] = time.time()
            else:
                self.dicTimes[event.Key.lower()]["keyDown"] = time.time()
        except KeyError:
            pass

        #20210123 MH: If the key ASCII value is equal to ESC ASCII value then the program ends
        if event.Ascii == 27:
            self.running = False

    #20210123 MH: this function will be excecuted every time a key is released
    def KeyUpEvent(self, event ):
        try:
            if event.Key == "Return":
                self.dicTimes[event.Key]["keyUp"] = time.time()
            else:
                self.dicTimes[event.Key.lower()]["keyUp"] = time.time()
        except KeyError:
            pass   

    #20210123 MH: Create dictionary which will storage raw keyboard use times    
    def CreateDicTimes(self):
        for char in list(self.password):
            if char.isupper():
                # if character is uppercase, have an additional dict key for corresponding lowercase letter!
                self.dicTimes[char.lower()] = {"keyUp": None, "keyDown": None}
            elif char == ".":
                self.dicTimes["period"] = {"keyUp": None, "keyDown": None}
            else:
                self.dicTimes[char] = {"keyUp": None, "keyDown": None}

        self.dicTimes["Return"] = {"keyUp": None, "keyDown": None}
    
    #20210123 MH: Calculate keystroke times. Hold (H), PressPress (DD) and ReleasePress (UD).
    def CalculateKeystrokesDynamics(self):
        while self.sessionCount <= self.sessionFreq:
            while self.entryCount <= self.entryFreq:
                print("Session: {}".format(self.sessionCount) + ". Enter {} times more!".format(1+self.entryFreq-self.entryCount))
                input_pwd = input("Enter \'{}\' : ".format(self.password))
                self.passOk = False
                
                if input_pwd == self.password:
                    print("pwd correct!")
                    self.passOk = True
                
                self.dicKeystrokesTimes = dict()
                self.dicKeystrokesTimes["hold_time"] = dict()
                self.dicKeystrokesTimes["ud_key1_key2"] = dict()
                self.dicKeystrokesTimes["dd_key1_key2"] = dict()
                self.dicKeystrokesTimes["password_entry_count"] = self.entryCount
                self.dicKeystrokesTimes["password_session_count"] = self.sessionCount

                if self.passOk:
                    self.entryCount = self.entryCount + 1
                    #Hold Time
                    for key in list(self.password):
                        if key == ".":
                            self.dicKeystrokesTimes["hold_time"]["period"] = self.dicTimes["period"]["keyUp"] - self.dicTimes["period"]["keyDown"]
                        elif key.isupper():
                            try:
                                self.dicKeystrokesTimes["hold_time"][key] = self.dicTimes[key.lower()]["keyUp"] - self.dicTimes[key.lower()]["keyDown"]
                            except Exception:
                                self.dicKeystrokesTimes["hold_time"][key] = self.dicTimes[key]["keyUp"] - self.dicTimes[key]["keyDown"]
                        else:
                            self.dicKeystrokesTimes["hold_time"][key] = self.dicTimes[key]["keyUp"] - self.dicTimes[key]["keyDown"]

                    #UD and DD times
                    for key1, key2 in zip(self.password, self.password[1:]):
                        if key1 == "." or key2 == ".":
                            if key1 == ".":
                                key1 = "period"
                            else:
                                key2 = "period"
                            
                            self.dicKeystrokesTimes["dd_key1_key2"]["DD."+key1+"."+key2] = self.dicTimes[key2]["keyDown"] - self.dicTimes[key1]["keyDown"]
                            self.dicKeystrokesTimes["ud_key1_key2"]["UD."+key1+"."+key2] = self.dicTimes[key2]["keyDown"] - self.dicTimes[key1]["keyUp"]
                        
                        elif key1.isupper() or key2.isupper():
                            try:
                                self.dicKeystrokesTimes["dd_key1_key2"]["DD." + key1 + "." + key2] = self.dicTimes[key2.lower()]["keyDown"] - self.dicTimes[key1.lower()]["keyDown"]
                                self.dicKeystrokesTimes["ud_key1_key2"]["UD." + key1 + "." + key2] = self.dicTimes[key2.lower()]["keyDown"] - self.dicTimes[key1.lower()]["keyUp"]
                            except Exception:
                                self.dicKeystrokesTimes["dd_key1_key2"]["DD." + key1 + "." + key2] = self.dicTimes[key2]["keyDown"] - self.dicTimes[key1]["keyDown"]
                                self.dicKeystrokesTimes["ud_key1_key2"]["UD." + key1 + "." + key2] = self.dicTimes[key2]["keyDown"] - self.dicTimes[key1]["keyUp"]
                        else:
                            self.dicKeystrokesTimes["dd_key1_key2"]["DD." + key1 + "." + key2] = self.dicTimes[key2]["keyDown"] - self.dicTimes[key1]["keyDown"]
                            self.dicKeystrokesTimes["ud_key1_key2"]["UD." + key1 + "." + key2] = self.dicTimes[key2]["keyDown"] - self.dicTimes[key1]["keyUp"]
                    
                    time.sleep(1)
                    self.dicKeystrokesTimes["hold_time"]["Return"] = self.dicTimes["Return"]["keyUp"] - self.dicTimes["Return"]["keyDown"]
                    self.dicKeystrokesTimes["ud_key1_key2"]["UD." + list(self.password)[-1] + ".Return"] = self.dicTimes["Return"]["keyDown"] - self.dicTimes[list(self.password)[-1]]["keyUp"]
                    self.dicKeystrokesTimes["dd_key1_key2"]["DD." + list(self.password)[-1] + ".Return"] = self.dicTimes["Return"]["keyDown"] - self.dicTimes[list(self.password)[-1]]["keyDown"]

                    self.listTimes.append(self.dicKeystrokesTimes)
                
                else:
                    print("Password entered was not correct! Please type \'{}\' again !".format(self.password))

            self.entryCount = 1
            self.sessionCount = self.sessionCount + 1

        if self.sessionFreq < self.sessionCount:
            print("Thanks for your help! Press Escape (ESC) to exit.")

        self.dicCSVTimes["timings"] = self.listTimes
        self.dicCSVTimes["user"] = self.user

        self.CreateCSV(self.dicCSVTimes)
                
    #20210123 MH: Create CSV output file       
    def CreateCSV(self, csvFile):
        rows = []
        #cnt = 1
        
        data = csvFile

        for timing in data['timings']:

            row = dict()

            for key in timing["hold_time"].keys():
                if key == "5":
                    new_key = "H.five"
                elif key == "R":
                    new_key = "H.Shift.r"
                else:
                    new_key = "H."+key
                
                row[new_key] = timing["hold_time"][key]
            
            for key in timing["dd_key1_key2"].keys():
                if key == "DD.5.R":
                    new_key = "DD.five.Shift.r"
                elif key == "DD.R.o":
                    new_key = "DD.Shift.r.o"
                elif key == "DD.e.5":
                    new_key = "DD.e.five"
                else:
                    new_key = key
                
                row[new_key] = timing["dd_key1_key2"][key]

            for key in timing["ud_key1_key2"].keys():
                if key == "UD.5.R":
                    new_key = "UD.five.Shift.r"
                elif key == "UD.R.o":
                    new_key = "UD.Shift.r.o"
                elif key == "UD.e.5":
                    new_key = "UD.e.five"
                else:
                    new_key = key
                
                row[new_key] = timing["ud_key1_key2"][key]

            row["subject"] = self.user
            row["rep"] = timing["password_entry_count"]
            row["sessionIndex"] = timing["password_session_count"]
            rows.append(row)

        column_names = ["subject", "sessionIndex", "rep", "H.period", "DD.period.t", "UD.period.t", "H.t", "DD.t.i", "UD.t.i", "H.i",	"DD.i.e", "UD.i.e", "H.e",
                "DD.e.five", "UD.e.five", "H.five", "DD.five.Shift.r", "UD.five.Shift.r", "H.Shift.r", "DD.Shift.r.o",
                "UD.Shift.r.o", "H.o", "DD.o.a", "UD.o.a", "H.a", "DD.a.n", "UD.a.n",	"H.n", "DD.n.l", "UD.n.l",
                "H.l", "DD.l.Return", "UD.l.Return", "H.Return"]

        try:
            with open('output/{}_timings.csv'.format(self.user), 'w') as csvOutputFile:
                writer = csv.DictWriter(csvOutputFile, fieldnames=column_names)
                writer.writeheader()
                for r in rows:
                    writer.writerow(r)
        except IOError:
            print("Error writing CSV output file.")
        
        
    



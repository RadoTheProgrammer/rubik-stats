import webbrowser
import json
import os
import pandas as pd
import matplotlib.pyplot as plt

INFORMATION_COLUMNS = {"Comment","Scramble","Date","Status"}
TOTAL_COLUMN = "Total"
class Metric(pd.DataFrame):
    pass

    def clean(self):
        new =  self.astype({"Date":"datetime64[s]"}) # 1. change type of data
        for phase in set(new.columns)-INFORMATION_COLUMNS: # 2. round the time
            new[phase] = new[phase].apply(lambda t:round(t,ndigits=3))
        new = new.sort_values(by="Date").reset_index(drop=True) # 3. sort by date
        return Metric(new)

    CONVERT_STATUS = {0:"OK",2000:"+2",-1:"DNF"}
    @classmethod
    def read_cstimer(cls,file,session_id=1):
        with open(file) as f:
            data = json.load(f)[f"session{session_id}"]

        nphases = max(len(solve[0]) for solve in data)-1
        multiphases = nphases>1
        #print(nphases)
        phases_columns = [f"P{nphase+1}" for nphase in range(nphases)] if multiphases else []
        df={column:[] for column in ["Status", TOTAL_COLUMN, *phases_columns, "Comment", "Scramble", "Date"]}

        for nsolve, solve in enumerate(data):
            times = solve[0]

            df["Status"].append(cls.CONVERT_STATUS[times.pop(0)])
            df[TOTAL_COLUMN].append(sum(times)/1000)
            df["Comment"].append(solve[2]), 
            df["Scramble"].append(solve[1])
            df["Date"].append(solve[3])

            
            if multiphases:
                for phase_col,phase_time in zip(phases_columns,times):
                    df[phase_col].append(phase_time/1000)

        return cls(df).clean()
                
    def apply_metric(self,metric):
        if metric.startswith("ao"):
            number=metric[2:]
            
# Example usage

# data = pd.read_csv("CubeTime - Default Session.csv")
data = Metric.read_cstimer("CubeTime Export (csTimer).json")
#data.trend()
print(data)
# print(data)

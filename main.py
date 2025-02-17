import webbrowser
import json
import os
import pandas as pd
import matplotlib.pyplot as plt

# display(file_cstimer,"display-cstimer.json")
# display(file_cubetime,"display-cubetime.json")

# with open(file_cubetime) as f:
#     data = json.load(f)
# sessionData = json.loads(data["properties"]["sessionData"])
# display(sessionData,"display-cubetime-session.json")
#display("cstimer_20250202_160540.txt")



class RubikStats(pd.DataFrame):
    """
    A subclass of pandas DataFrame with custom methods.
    """
    
    def __init__(self, *args, clean=True, **kwargs):
        super().__init__(*args, **kwargs)
        if clean:
            self["Time"] = self["Time"].apply(lambda t:round(t,ndigits=3))
            self["Date"] = pd.to_datetime(self["Date"],unit="s")
            self.sort_values(by="Date",inplace=True)
            self.reset_index(drop=True, inplace=True)

    
    @classmethod
    def read_csv(self,file):
        return RubikStats(pd.read_csv(file))
    
    CONVERT_STATUS = {0:"OK",2000:"+2",-1:"DNF"}
    @classmethod
    def read_cstimer(cls,file,session_id=1):
        with open(file) as f:
            data = json.load(f)[f"session{session_id}"]

        nphases = max(len(solve[0]) for solve in data)-1
        multiphases = nphases>1
        #print(nphases)
        phases_columns = [f"P{nphase+1}" for nphase in range(nphases)] if multiphases else []
        df = pd.DataFrame(columns=["Status", "Time", *phases_columns, "Comment", "Scramble", "Date"])
        for nsolve, solve in enumerate(data):
            times = solve[0]

            row = {
                "Status":cls.CONVERT_STATUS[times.pop(0)],
                "Time":sum(times)/1000,
                "Comment":solve[2], 
                "Scramble":solve[1], 
                "Date":pd.to_datetime(solve[3],unit="s"),
            }
            
            if multiphases:
                for phase_col,phase_time in zip(phases_columns,times):
                    row[phase_col] = phase_time/1000
                    
            df.loc[nsolve] = row
            
        return RubikStats(df)
                
    def trend(self):
        plt.plot(self.index, self["Time"], label="Time")
        
        #plt.xlabel('Date')
        plt.ylabel('Time')
        plt.title('Time Trend')
        #plt.gcf().autofmt_xdate()
        plt.legend()
        plt.show()
            
    def add(self,*columns):
        """Add a new column of ao or avg"""
        for to_display in columns:
            if "," in to_display:
                phase,_,to_display=to_display.partition(",")
                

# Example usage

# data = pd.read_csv("CubeTime - Default Session.csv")
data = RubikStats.read_cstimer("CubeTime Export (csTimer).json")
data.trend()
print(data)
# print(data)

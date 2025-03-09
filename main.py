import webbrowser
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import math

INFORMATION_COLUMNS = ["Comment","Scramble","Date","Status"]
TOTAL_COLUMN = "Total"

class Metric:
    
    @classmethod
    def to_metric_obj(cls,metric):
        if isinstance(metric,cls):
            return metric
        elif isinstance(metric,int):
            if metric==1:
                return single()
            return ao(metric)
        elif isinstance(metric,str):
            if metric.startswith("ao"):
                return ao(int(metric[2:]))
            elif metric.startswith("avg"):
                return avg(int(metric[3:]))
            elif metric=="single":
                return single()

class ao(Metric):
    def __init__(self,n):
        self.n=n
        self.n_removed=math.ceil(self.n*0.05)
        self.n_remaining=self.n-self.n_removed*2
        
    def on_series(self,series):
        return series.rolling(self.n).apply(self.apply_func)
    
    def apply_func(self,values):
        new_values = sorted(values)[self.n_removed:-self.n_removed] # remove the fastest and slowest times
        result = sum(new_values)/self.n_remaining
        return result
    
    def __repr__(self):
        return f"ao{self.n}"
class avg(Metric):
    def __init__(self,n):
        self.n=n
        
    def on_series(self,series):
        return series.rolling(self.n).apply(self.apply_func)
    
    def apply_func(self,values):
        return sum(values)/self.n
    
    def __repr__(self):
        return f"avg{self.n}"
    
class single(Metric):
    def on_series(self,series):
        return series.copy()
    
    def __repr__(self):
        return "single"
class DataPhases(pd.DataFrame):
    pass
    @property
    def _constructor(self):
        return DataPhases

    def round_time(self):
        for phase in self.columns: # 2. round the time
            if phase in INFORMATION_COLUMNS:
                continue
            self[phase] = self[phase].apply(lambda t:round(t,ndigits=3))
        return self
    
    def sort_by_date(self):
        return self.sort_values(by="Date").reset_index(drop=True)
    
    def astype_date(self):
        return self.astype({"Date":"datetime64[s]"})
    
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
            df["Status"].append(cls.CONVERT_STATUS[times[0]])
            df[TOTAL_COLUMN].append(times[1]/1000)
            df["Comment"].append(solve[2]), 
            df["Scramble"].append(solve[1])
            df["Date"].append(solve[3])
            
            if multiphases:
                for nphase in range(1,nphases+1): # to start from 1
                    phase_col = f"P{nphase}"
                    phase_time = times[-1] if nphase==1 else times[-nphase]-times[-nphase+1]
                    df[phase_col].append(phase_time/1000)
                    
        #df = {"a":[],"b":[],"c":[]}
        return cls(df).astype_date().sort_by_date()
                
    def apply_metric(self,metric):
        new = DataPhases(self)
        metric=Metric.to_metric_obj(metric)
        print(self.columns)
        for phase in self.columns:
            if phase in INFORMATION_COLUMNS:
                continue
            new[phase]=metric.on_series(self[phase])
        return new.round_time()

    def ao(self,n):
        return self.apply_metric(ao(n))
    
    def avg(self,n):
        return self.apply_metric(avg(n))
                
    def analyse_phase(self,phase,*metrics):
        if not metrics:
            pass # do later
        new=Phase(self[INFORMATION_COLUMNS])
        for metric in metrics:
            metric = Metric.to_metric_obj(metric)
            new[str(metric)] = metric.on_series(self[phase])
        return new
        
class Phase(pd.DataFrame):
    @property
    def _constructor(self):
        return Phase
# Example usage

# data = pd.read_csv("CubeTime - Default Session.csv")
data = DataPhases.read_cstimer("cstimer_data.txt")
print(data.analyse_phase("Total",1,5,12))

# print(data)

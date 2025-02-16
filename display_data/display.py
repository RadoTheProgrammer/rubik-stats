import webbrowser
import json
import os

def display(data,file_output="display.json"):
    if isinstance(data,str): # file
        
        with open(data) as f:
            data = json.load(f)
    
    with open(file_output,"w") as f:
        json.dump(data,f,indent=4)
    webbrowser.open(f"file://{os.path.realpath(file_output)}")
    
display("/Users/alain/Downloads/CubeTime Export (csTimer) 2.json","display-cubetime-test.json")
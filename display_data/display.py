import webbrowser
import json
import os
import argparse

def display(data,file_output="display.json"):
    if isinstance(data,str): # file
        
        with open(data) as f:
            data = json.load(f)
    
    with open(file_output,"w") as f:
        json.dump(data,f,indent=4)
    webbrowser.open(f"file://{os.path.realpath(file_output)}")
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Display JSON data in a browser.")
    parser.add_argument("input", help="Input file containing JSON data or a JSON string.")
    parser.add_argument(
        "--output",
        default="display.json",
        help="Output file to save the JSON data (default: display.json).",
    )

    args = parser.parse_args()
    display(args.input, args.output)
#display(r"display_data\\cstimer_20250416_124212.txt", r"display_data\\cstimer_20250416_124212.json")
#display("cstimer_data.txt","display_data/cstimer_data_display.json")

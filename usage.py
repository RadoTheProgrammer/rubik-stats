import main

data = main.read_cstimer("cstimer_data.txt")
phase = data.analyse_phase("Total")
phase.trends()
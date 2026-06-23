#batteryWeightEstimation.py
from batteryVoltageConvertion import batteryVoltage

def batteryWeight(capacity_mAh, numCells,batteryType):

    if batteryType == "LiPo":

        energyDensity_Wh_kg=150
        voltage_V = batteryVoltage(numCells)   # tensione nominale
        capacity_Ah = capacity_mAh / 1000
        energy_Wh = capacity_Ah * voltage_V
        weight_kg = energy_Wh / energyDensity_Wh_kg
        return int(round(weight_kg * 1000))      # converti in grammi
    
    elif batteryType == "LiIon":

        energyDensity_Wh_kg=175
        voltage_V = batteryVoltage(numCells)   # tensione nominale
        capacity_Ah = capacity_mAh / 1000
        energy_Wh = capacity_Ah * voltage_V
        weight_kg = energy_Wh / energyDensity_Wh_kg
        return int(round(weight_kg * 1000))      # converti in grammi

        
    
    else:
        
        print("ERROR:error type battery")
        return 1

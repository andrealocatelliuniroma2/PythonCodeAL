# main.py
import json
import weightDrone
import infoDisplay
from droneData import DroneInfo

from pathlib import Path
from datasheetLoader import load_datasheet, selectBlock
from datasheetCSVLoader import load_datasheet_csv, selectBlock_csv
from currentEstimate import estimateCurrent

SCRIPT_DIR = Path(__file__).resolve().parent

from displayDatasheet import displayDatasheet
from autonomyEstimate import autonomyTime
from batteryVoltageConvertion import batteryVoltage
from batteryWeightEstimate import batteryWeight

def main():
    

    # file json with info 
    with open(SCRIPT_DIR / "config.json", encoding="utf-8") as f:
        cfg = json.load(f)

    # Extracting and removing the motor datasheet filename
    datasheetFile = cfg.pop("datasheetFile")

    # If battery weight is not provided (-1), estimate it
    if cfg["weightBattery_g"] == -1:
        cfg["weightBattery_g"] = batteryWeight(
            cfg["battery_mAh"], cfg["batteryV_S"], cfg["batteryType"])

    # Build DroneInfo from json file values
    info = DroneInfo(**cfg)
    infoDisplay.displayInfo(info)


    # Total weight
    weightVector = [info.weightFrame_g,info.weightBattery_g,info.numMotor*info.weightMotor_g,info.numMotor*info.weightProp_g,info.weightPayload_g,info.weightExtra_g]    
    weightTot = weightDrone.weightSum(weightVector)


    # Load datasheet
    datasheet = SCRIPT_DIR / "datasheetMotor" / datasheetFile
    #datasheetMotor = load_datasheet(datasheet) # vecchio codice
    datasheetMotor = load_datasheet_csv(datasheet)
    
    # print datasheet
    #displayDatasheet(datasheetMotor)

    print(f"Total weight: {weightTot} g")

    #Thrust(g) -> A
    thrustSingleMotor_g = weightTot/info.numMotor
    motorVoltage = batteryVoltage(info.batteryV_S)
    print(f"Motor Voltage: {motorVoltage} V")
    
    #tabDatasheet = selectBlock(datasheetMotor, kv=info.motorKV, voltage=motorVoltage, prop=info.propType)  # vecchio codice
    tabDatasheet = selectBlock_csv(datasheetMotor, kv=info.motorKV, voltage=motorVoltage, prop=info.propType)
    
    # Etimated current per motor
    estimateI_A = estimateCurrent(thrustSingleMotor_g, tabDatasheet["thrust_g"], tabDatasheet["current_A"])
    print(f"Estimated Current per Motor: {estimateI_A:.2f} A")

    # Estimated flight time
    autonomyTimeEstimate = autonomyTime(estimateI_A,info.battery_mAh,info.numMotor)
    print(f"Estimated flight time: {autonomyTimeEstimate:.2f} min")

if __name__ == "__main__":
    main()
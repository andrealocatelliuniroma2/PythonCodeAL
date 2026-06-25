# Author: Andrea Locatelli <andrea.locatelli.1997@gmail.com>
# Copyright (c) 2026 Andrea Locatelli

#infoDisplay.py

def displayInfo(info):
    print()
    print("---------------------------Drone info ----------------------")
    print(f"Frame : {info.frameType}")
    print(f"Number of motors:   {info.numMotor}")
    print(f"Frame weight:   {info.weightFrame_g} g")
    print(f"Battery weight: {info.weightBattery_g} g")
    print(f"Motor weight: {info.weightMotor_g} g")
    print(f"Extra weight(ESC,flight controller,wiring,...): {info.weightExtra_g} g")
    print(f"Payload: {info.weightPayload_g} g")
    print(f"Propeller weight: {info.weightProp_g} g")
    print(f"Battery : {info.batteryType} {info.batteryV_S}S / {info.battery_mAh} mAh")
    print(f"Motor : {info.motorType} {info.motorKV}")
    print(f"Propeller : {info.propType}")
    print("------------------------------------------------------------")
    print()

    
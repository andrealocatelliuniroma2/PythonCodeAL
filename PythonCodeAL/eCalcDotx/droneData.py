# Author: Andrea Locatelli <andrea.locatelli.1997@gmail.com>
# Copyright (c) 2026 Andrea Locatelli

# droneData.py
from dataclasses import dataclass

@dataclass
class DroneInfo:
    frameType: str
    numMotor: int
    weightFrame_g: float
    weightBattery_g: float
    weightMotor_g: float
    weightExtra_g: float
    weightPayload_g: float
    weightProp_g: float
    battery_mAh: float
    batteryV_S: int
    batteryType: str
    motorKV: str
    motorType: str
    propType: str
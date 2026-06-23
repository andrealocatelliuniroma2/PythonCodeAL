#autonomyEstimate.py

def autonomyTime(estimateI_A,battery_mAh,numMotor):
    autonomy = ((battery_mAh/1000)/(numMotor*estimateI_A))*60
    return autonomy
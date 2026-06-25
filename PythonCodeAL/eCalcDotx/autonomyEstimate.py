#autonomyEstimate.py

def autonomyTime(estimateI_A,I_avionics_A,battery_mAh,numMotor):
    USABLE_FRACTION = 0.85
    
    autonomy = ((USABLE_FRACTION*battery_mAh/1000)/(I_avionics_A + numMotor*estimateI_A))*60
    return autonomy
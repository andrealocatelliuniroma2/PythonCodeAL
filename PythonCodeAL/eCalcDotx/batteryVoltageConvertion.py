#batteryVoltageConvertion.py

def batteryVoltage(numCells):
    """Tensione nominale di un pacco LiPo dato il numero di celle in serie (S)."""
    return round(numCells * 3.7,1)
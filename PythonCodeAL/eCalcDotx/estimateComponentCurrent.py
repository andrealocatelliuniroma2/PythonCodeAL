def estimate_avionics_current(pack_voltage_V,
                              num_esc,
                              autopilot_power_W=2.5,
                              esc_idle_power_W=0.25,
                              converter_efficiency=0.87):
    """
    Estimate the continuous current drawn from the main battery pack by the
    avionics (everything except the motor mechanical load), referred to the
    pack voltage.

    Parameters
    ----------
    pack_voltage_V : float
        Nominal battery pack voltage [V] (same one used for the datasheet lookup).
    num_esc : int
        Number of ESCs (typically equals the number of motors).
    autopilot_power_W : float
        Continuous power drawn by the Pixhawk AND its standard peripherals
        (GPS, RC receiver, telemetry radio). Order of magnitude: ~2-6 W
        depending on how many peripherals are attached. Default 5.0 W.
    esc_idle_power_W : float
        Per-ESC *idle/logic* power (MCU + gate-driver supply), NOT the load
        losses. Small, ~0.1-0.5 W each. Default 0.25 W.
    converter_efficiency : float
        Efficiency of the power module / BEC stepping pack voltage down to the
        5 V rail. Typical 0.85-0.90. Default 0.87.

    Returns
    -------
    float
        Avionics current as seen by the pack [A].

    Note
    ----
    The ESC *conversion losses at load* are already included in the datasheet
    current (measured at the pack input). This function only adds the ESC
    standby/logic draw, to avoid double counting.
    """
    total_power_W = autopilot_power_W + num_esc * esc_idle_power_W
    return total_power_W / (pack_voltage_V * converter_efficiency)
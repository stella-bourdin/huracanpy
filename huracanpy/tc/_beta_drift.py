import numpy as np

def beta_drift(lat, wind_max, radius_wind_max,):
    """
    Based on Smith, 1993: https://journals.ametsoc.org/view/journals/atsc/50/18/1520-0469_1993_050_3213_ahbdl_2_0_co_2.xml?tab_body=pdf

    Parameters
    ----------
    lat : TYPE
        DESCRIPTION.
    wind_max : TYPE
        DESCRIPTION.
    radius_wind_max : TYPE
        DESCRIPTION.

    Returns
    -------
    V_drift : TYPE
        DESCRIPTION.
    theta_drift : TYPE
        DESCRIPTION.

    """
    
    # Treat input
    ## Convert lat to rad
    if lat.max() > np.pi: # We assume lats are in degrees if they exceed pi
        lat = lat / 180 * np.pi
    ## Convert rmw to m
    if radius_wind_max.max() < 10000: # We assume rmw are in km if they are below 10,000
        radius_wind_max = radius_wind_max*1000
    
    # Coriolis parameters
    Omega = 7.2921e-5 #rad/s Rotation rate of the Earth
    a = 6.378e6 #m Mean radius of the Earth
    beta = 2 * Omega * np.cos(lat) / a #s-1 m-1
    
    # Beta-drift parameters
    V_char = (radius_wind_max ** 2) * beta # m/s
    B = V_char / wind_max               # non-dimensionnal
    V_drift_adim =0.72*B**(-0.54)       # non-dmensionnal
    V_drift = V_drift_adim*V_char       # m/s 
    theta_drift = 308 - 9.6 * np.log(B) # degrees
    
    return V_drift, theta_drift

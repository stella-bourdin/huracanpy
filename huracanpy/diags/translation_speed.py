"""
Module containing functions to compute translation speed
"""

from haversine import haversine
import numpy as np
import xarray as xr


def translation_speed(data):
    """
    Compute translation speed along tracks

    Parameters
    ----------
    data : xr.Dataset

    Returns
    -------
    xr.Dataset
        Translation speeds. Output is stored for points that correspond to the middle of two consecutive points in the initial dataset.

    """
    data = data.sortby(["track_id", "time"])
    V, lat, lon, t, tid = [], [], [], [], []  # To store results temporarily
    for i in range(len(data.obs) - 1):
        p = data.isel(obs=i)  # Current point
        q = data.isel(obs=i + 1)  # Next point
        if p.track_id == q.track_id:  # If both points belong to the same track
            dt = np.timedelta64((q.time - p.time).values, "s")  # Temporal interval in s
            dx = haversine(
                (p.lat, p.lon), (q.lat, q.lon), unit="m"
            )  # Displacement in m
            v = dx / dt.astype(float)  # translation speed in m/s
            V.append(v)
            # Results will be stored with coordinates corresponding to the middle of p and q
            lat.append((p.lat + q.lat).values / 2)
            lon.append((p.lon + q.lon).values / 2)
            t.append((p.time + (q.time - p.time) / 2).values)
            tid.append(p.track_id.values)

    # Transform into clean dataset
    V = xr.DataArray(V, dims="mid_obs", coords={"mid_obs": np.arange(len(V))})
    lon = xr.DataArray(lon, dims="mid_obs", coords={"mid_obs": np.arange(len(lon))})
    lat = xr.DataArray(lat, dims="mid_obs", coords={"mid_obs": np.arange(len(lat))})
    t = xr.DataArray(t, dims="mid_obs", coords={"mid_obs": np.arange(len(t))})
    tid = xr.DataArray(tid, dims="mid_obs", coords={"mid_obs": np.arange(len(tid))})

    return xr.Dataset(
        {"lon": lon, "lat": lat, "time": t, "track_id": tid, "translation_speed": V}
    )
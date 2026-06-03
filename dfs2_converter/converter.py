import os

import numpy as np
import pandas as pd
import xarray as xr
import mikeio


def build_output_path(input_path, output_dir=None, output_name=None):
    if output_dir is None or output_dir.strip() == "":
        output_dir = os.getcwd()
    output_dir = os.path.abspath(output_dir)
    if not os.path.isdir(output_dir):
        raise FileNotFoundError(f"Output directory does not exist: {output_dir}")

    if output_name is None or output_name.strip() == "":
        output_name = os.path.splitext(os.path.basename(input_path))[0] + ".dfs2"
    if not output_name.lower().endswith(".dfs2"):
        output_name = output_name + ".dfs2"

    return os.path.join(output_dir, output_name)


def convert_nc_to_dfs2(infile, outfile=None, u_var="u10", v_var="v10"):
    infile = os.path.abspath(infile)
    if not os.path.isfile(infile):
        raise FileNotFoundError(f"Input file not found: {infile}")

    if outfile is None:
        outfile = build_output_path(infile)
    outfile = os.path.abspath(outfile)
    output_dir = os.path.dirname(outfile)
    os.makedirs(output_dir, exist_ok=True)

    with xr.open_dataset(infile) as ds_xr:
        if u_var not in ds_xr.data_vars:
            raise ValueError(f"U variable '{u_var}' not found in {infile}")
        if v_var not in ds_xr.data_vars:
            raise ValueError(f"V variable '{v_var}' not found in {infile}")

        if 'valid_time' in ds_xr.coords:
            time_coord = pd.to_datetime(ds_xr['valid_time'].values)
        elif 'time' in ds_xr.coords:
            time_coord = pd.to_datetime(ds_xr['time'].values)
        else:
            raise ValueError('No time coordinate found (expected valid_time or time)')

        lat = ds_xr['latitude'].values
        lon = ds_xr['longitude'].values

        u = np.asarray(ds_xr[u_var].values, dtype=float)
        v = np.asarray(ds_xr[v_var].values, dtype=float)

    if lat.ndim != 1 or lon.ndim != 1:
        raise ValueError('Latitude and longitude coordinates must be 1D arrays')

    # Ensure latitude and longitude are increasing as required by mikeio.Grid2D
    if lat[0] > lat[-1]:
        lat = lat[::-1]
        u = u[:, ::-1, :]
        v = v[:, ::-1, :]
    if lon[0] > lon[-1]:
        lon = lon[::-1]
        u = u[:, :, ::-1]
        v = v[:, :, ::-1]

    grid = mikeio.Grid2D(x=lon, y=lat, projection='LONG/LAT')
    items = [u_var, v_var]
    dataset = mikeio.Dataset.from_numpy([u, v], time=time_coord, items=items, geometry=grid)
    dataset.to_dfs(outfile)
    return outfile

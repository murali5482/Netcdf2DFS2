# DFS2 Converter

A small Python package to convert NetCDF wind fields (`u10`, `v10`) into DHI MIKE 21 `dfs2` files.

## Install

```bash
python -m pip install -e .
```

## Usage

Run interactively:

```bash
python convert_nc_to_dfs2.py
```

Or with arguments:

```bash
python convert_nc_to_dfs2.py --infile ERA5_wind_UV_2024.nc --outfile output/ERA5_wind_UV_2024.dfs2
```

The script will ask for:
- input NetCDF file
- output folder
- output file name

## Package CLI

After install, use:

```bash
convert-nc-to-dfs2
```

## Notes

If no output filename is provided, the converter defaults to the input basename with `.dfs2`.

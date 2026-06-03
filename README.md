# Netcdf2DFS2

Lightweight converter to generate DHI MIKE 21 `dfs2` files from NetCDF U/V wind fields.

Key points:
- Converts paired U/V variables (default `u10`/`v10`) into a `dfs2` time series using `mikeio`.
- Interactive prompts let you choose the input `.nc`, output folder, and output filename.
- Large raw/data files were intentionally removed from this repository; use Git LFS if you need to store binaries.

Quick start:

Install in editable mode:

```powershell
python -m pip install -e .
```

Run interactively:

```powershell
convert-nc-to-dfs2 --ask
```

Or run non-interactively:

```powershell
convert-nc-to-dfs2 --infile path\to\file.nc --outfile path\to\out.dfs2
```

If you need to keep large datasets with this project, enable Git LFS and track the appropriate extensions (`.nc`, `.dfs2`, etc.).

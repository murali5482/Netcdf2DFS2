import argparse
import os

from .converter import build_output_path, convert_nc_to_dfs2


def prompt_text(message, default=None):
    if default:
        prompt = f"{message} [{default}]: "
    else:
        prompt = f"{message}: "
    value = input(prompt).strip()
    return value if value else default


def prompt_input_file(default=None):
    while True:
        path = prompt_text('Enter input NetCDF file path', default)
        if not path:
            print('Input file path cannot be empty.')
            continue
        if not os.path.isfile(path):
            print(f'File not found: {path}')
            continue
        if not path.lower().endswith('.nc'):
            print('Please provide a .nc file.')
            continue
        return os.path.abspath(path)


def prompt_output_path(input_file, default_dir=None, default_name=None):
    default_dir = default_dir or os.getcwd()
    default_name = default_name or os.path.splitext(os.path.basename(input_file))[0] + '.dfs2'

    while True:
        output_dir = prompt_text('Enter output folder', default_dir)
        if not output_dir:
            print('Output folder cannot be empty.')
            continue
        output_dir = os.path.abspath(output_dir)
        if os.path.isfile(output_dir):
            print('Output folder must be a directory, not a file.')
            continue
        if not os.path.isdir(output_dir):
            create = prompt_text(f'Directory does not exist. Create {output_dir}? (y/n)', 'y')
            if create.lower().startswith('y'):
                os.makedirs(output_dir, exist_ok=True)
            else:
                continue
        break

    output_name = prompt_text('Enter output file name', default_name)
    if not output_name.lower().endswith('.dfs2'):
        output_name += '.dfs2'

    return build_output_path(input_file, output_dir, output_name)


def main():
    parser = argparse.ArgumentParser(description='Convert NetCDF U/V wind data to DHI MIKE 21 dfs2 files.')
    parser.add_argument('--infile', help='Input NetCDF file path')
    parser.add_argument('--outfile', help='Output dfs2 file path or filename')
    parser.add_argument('--u', default='u10', help='U variable name in NetCDF')
    parser.add_argument('--v', default='v10', help='V variable name in NetCDF')
    parser.add_argument('--ask', action='store_true', help='Ask interactively for input and output paths')
    args = parser.parse_args()

    infile = args.infile
    if infile is None or args.ask:
        infile = prompt_input_file(infile)
    if infile is None:
        raise SystemExit('Input NetCDF file is required.')

    outfile = args.outfile
    if outfile is None or args.ask:
        outfile = prompt_output_path(infile)
    elif not os.path.isabs(outfile):
        outfile = os.path.abspath(outfile)

    outfile = build_output_path(infile, os.path.dirname(outfile), os.path.basename(outfile))
    converted = convert_nc_to_dfs2(infile, outfile, args.u, args.v)
    print(f'Converted to: {converted}')

import argparse
import os
import re

import yaml


def replace(s, values):
    s = re.sub(r"<%(.*?)%>", lambda x: values.get(x, x), s)
    return re.sub(r"$\((.*?)\)", lambda x: os.environ.get(x, x), s)


def render_file(src, dst, values):
    basename = os.path.basename(src)
    new_name = replace(basename, values)
    with open(f"{dst}/{new_name}", "w") as new:
        with open(f"{src}", "r") as old:
            new.write(replace(old.read(), values))


def render(src, dst, values={}):
    if os.path.isfile(src):
        render_file(src, dst, values)
        return
    for f in os.scandir(src):
        if f.name.startswith("."):
            continue
        if f.is_file:
            render_file(f.path, dst, values)
            return
        else:
            new_dst = replace(f"{dst}/{f.name}", values)
            os.mkdir(new_dst)
            render(f.path, new_dst, values)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Replaces all <%%> in all files in src with values provided, and writes the results to dst folder. $() is reserved for environment variables. File/dir that starts with . are ignored"
    )
    parser.add_argument(
        "-s",
        "--src",
        type=str,
        dest="src",
        required=True,
        help="src can be either a valid folder of directory. Note that src directory itself is not rendered. .* files/dirs are ignored.",
    )
    parser.add_argument(
        "-d",
        "--dst",
        type=str,
        dest="dst",
        required=True,
        help="Dst needs to be a directory.",
    )
    parser.add_argument(
        "-v",
        "--values",
        type=str,
        dest="values",
        default=None,
        help="values need to be valid file if provided",
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    src = os.path.abspath(args.src)
    dst = os.path.abspath(args.dst)
    values = os.path.abspath(args.values)
    if args.values is not None:
        values = os.path.abspath(args.values)
    # Validate src and values. Dst needs to be a directory. src can be either a valid folder of directory. values need to be valid file if provided.
    if not os.path.exists(src):
        raise Exception("src path is invalid")
    if not os.path.exists(dst) or not os.path.isdir(dst):
        raise Exception("dst path is invalid")
    if values and (not os.path.exists(values) or not os.path.isfile(values)):
        raise Exception("values path is invalid")
    # Lookup for values.yaml in src folder if values is not provided
    if os.path.isdir(src) and values is None and os.path.exists(f"{src}/values.yaml"):
        values = f"{src}/values.yaml"
    config_dict = {}
    if values is not None:
        with open(values) as f:
            config_dict = yaml.safe_load(f)
    render(src, dst, config_dict)


if __name__ == "main":
    main()

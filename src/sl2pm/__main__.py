import os
import sys
import argparse
import sl2pm


parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parentdir)


def main():
    doc = f"""
    Version: {'.'.join([str(i) for i in sl2pm.__version__])}

    A package for tracking particles, red blood cells (RBCs), and blood vessel walls with super-localization from images recorded with two-photon microscopy (2PM)."""
    parser = argparse.ArgumentParser(
        prog="sl2pm",
        description=doc,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,
    )
    helpos = parser.add_argument_group(title="Help and version", description=None)
    helpos.add_argument("-h", "--help", help="print help and exit", action="help")
    helpos.add_argument(
        "--version",
        action="version",
        version=f'SL2PM {".".join(map(str, sl2pm.__version__))}',
    )
    args = parser.parse_args()

    # if args.subcommand == COMMAND_CENTRIFUGE:
    #     df_result = centrifuge_data(args.input)
    # else:
    #     assert False

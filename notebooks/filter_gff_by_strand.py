"""Filter a GFF file by strand, feature type, and/or start-position range."""
import argparse


def filter_gff(in_path, out_path, strand=None, featuretype=None, positionrange=None):
    start, end = positionrange if positionrange else (None, None)
    total = 0
    kept = 0
    with open(in_path) as infile, open(out_path, "w") as outfile:
        for line in infile:
            total += 1
            fields = line.rstrip("\n").split("\t")
            if strand is not None and fields[6] != strand:
                continue
            if featuretype is not None and fields[2] != featuretype:
                continue
            if start is not None and not (start <= int(fields[3]) <= end):
                continue
            kept += 1
            outfile.write(line)
    return total, kept


def parse_positionrange(value):
    start_str, end_str = value.split("-")
    return int(start_str), int(end_str)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="input GFF path")
    parser.add_argument("--output", required=True, help="output GFF path")
    parser.add_argument("--strand", choices=["+", "-"], help="keep only this strand (column 7)")
    parser.add_argument("--featuretype", help="keep only this feature type (column 3), e.g. 'gene'")
    parser.add_argument(
        "--positionrange",
        type=parse_positionrange,
        help="keep only rows whose start (column 4) falls in START-END, e.g. 1000-2000",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    total, kept = filter_gff(
        args.input,
        args.output,
        strand=args.strand,
        featuretype=args.featuretype,
        positionrange=args.positionrange,
    )
    print(f"{kept}/{total} rows kept ({kept / total:.1%})")

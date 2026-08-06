#!/usr/bin/env python3
"""Practice makegff.py — sorted BAM -> 5'-end coverage GFF, using pysam only.

Usage:
    python my_makegff.py [--separate_strand] [--log_scale] <sorted.bam> [out.gff]
"""
import argparse
import math
from collections import Counter

import pysam


def five_prime_position(read):
    """1-based position of the read's 5' end on the reference."""
    if read.is_reverse:
        # pysam reference_end is 0-based, exclusive -> already equals the
        # 1-based coordinate of the last aligned base (the 5' end for a
        # reverse-strand read).
        return read.reference_end
    # pysam reference_start is 0-based -> +1 gives the 1-based leftmost
    # aligned base (the 5' end for a forward-strand read).
    return read.reference_start + 1


def count_five_prime_ends(bam_path):
    """Count reads per (seqname, 5' end position), separately per strand."""
    plus_counts = Counter()
    minus_counts = Counter()
    with pysam.AlignmentFile(bam_path, "rb") as bam:
        for read in bam.fetch(until_eof=True):
            if read.is_unmapped or read.is_secondary or read.is_supplementary:
                continue
            # Match the annotation's seqname convention: NC_000913.3 -> NC_000913
            chrom = read.reference_name.split(".")[0]
            pos = five_prime_position(read)
            if read.is_reverse:
                minus_counts[(chrom, pos)] += 1
            else:
                plus_counts[(chrom, pos)] += 1
    return plus_counts, minus_counts


def score(count, log_scale):
    return math.log2(count + 1) if log_scale else float(count)


def write_gff(plus_counts, minus_counts, out_path, name, separate_strand, log_scale):
    with open(out_path, "w") as out:
        if separate_strand:
            # +/- strands as two independent tracks — both scores positive.
            for (chrom, pos), count in sorted(plus_counts.items()):
                out.write(f"{chrom}\t\t{name}_(+)\t{pos}\t{pos}\t{score(count, log_scale):.2f}\t+\t.\t.\n")
            for (chrom, pos), count in sorted(minus_counts.items()):
                out.write(f"{chrom}\t\t{name}_(-)\t{pos}\t{pos}\t{score(count, log_scale):.2f}\t-\t.\t.\n")
        else:
            # Single track — reverse strand rendered as negative scores.
            for (chrom, pos), count in sorted(plus_counts.items()):
                out.write(f"{chrom}\t\t{name}\t{pos}\t{pos}\t{score(count, log_scale):.2f}\t+\t.\t.\n")
            for (chrom, pos), count in sorted(minus_counts.items()):
                out.write(f"{chrom}\t\t{name}\t{pos}\t{pos}\t{-score(count, log_scale):.2f}\t-\t.\t.\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bam", help="sorted BAM file")
    parser.add_argument("out", nargs="?", default=None, help="output GFF path (default: <bam basename>.gff)")
    parser.add_argument("--name", default=None, help="track/feature name for column 3 (default: BAM basename)")
    parser.add_argument("--separate_strand", action="store_true",
                         help="write +/- strands as two independent tracks instead of one signed track")
    parser.add_argument("--log_scale", action="store_true",
                         help="write log2(count+1) instead of the raw read count")
    args = parser.parse_args()

    out_path = args.out or (args.bam.rsplit(".", 1)[0] + ".gff")
    name = args.name or args.bam.split("/")[-1].split(".")[0]

    plus_counts, minus_counts = count_five_prime_ends(args.bam)
    write_gff(plus_counts, minus_counts, out_path, name, args.separate_strand, args.log_scale)


if __name__ == "__main__":
    main()

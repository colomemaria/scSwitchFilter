import argparse
import time
import scswitchfilter.bam2sam as bam2sam
import scswitchfilter.sam2tsv as sam2tsv
import scswitchfilter.generate_negative_matrix as generate_negative_matrix


def main():
    start_time = time.time()
    parser = argparse.ArgumentParser(
                    prog='compute_correction_matrix',
                    description='Generate the correction count matrix for hopped reads in plate-based sequencing experiments')
    parser.add_argument('filename', help='bam file with raw sequencing counts')
    parser.add_argument('outname', help='output filename')
    parser.add_argument('--samtools_path', help='path to samtools tool', type=str)
    parser.add_argument('--threshold', help='filtering threshold', type=float, default=0.8)
    parser.add_argument('--tag', help='Length of the TAG in CB of reads', type=int, default=0)
    parser.add_argument('--index1', help='Length of the index1 of reads', type=int)
    parser.add_argument('--index2', help='Length of the index2 of reads', type=int)
    args = parser.parse_args()
    bam2sam(args.filename, args.outname, args.samtools_path)
    sam2tsv(f"{args.outname}.sam", f"{args.outname}.tsv", args.tag, args.index1, args.index2)
    is_tag = False if is_tag == 0 else True
    neg_matrix = generate_negative_matrix(f"{args.outname}.tsv", threshold=args.threshold, is_tag=is_tag)
    neg_matrix.to_csv(f"{args.outname}_negative_matrix.csv")
    print(f'Elapsed time: {time.time() - start_time} seconds.')

    
if __name__ == '__main__':
    main()

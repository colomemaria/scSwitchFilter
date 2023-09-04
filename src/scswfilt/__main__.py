import argparse
import time
import scswfilt.bam2sam as bam2sam
import scswfilt.sam2tsv as sam2tsv
import scswfilt.generate_negative_matrix as generate_negative_matrix


def main():
    start_time = time.time()
    parser = argparse.ArgumentParser(
                    prog='ComputeNegativeMatrix',
                    description='Generate the negative count matrix for hopped reads in plate-based sequencing experiments',
                    epilog='It is recommended to run with screen or srun')
    parser.add_argument('filename', help='bam file with raw sequencing counts')
    parser.add_argument('outname', help='output filename')
    parser.add_argument('--samtools_path', help='path to samtools tool', type=str)
    parser.add_argument('--threshold', help='filtering threshold', type=float)
    args = parser.parse_args()
    bam2sam(args.filename, args.outname, args.samtools_path)
    sam2tsv(f"{args.outname}.sam", f"{args.outname}.tsv")
    threshold = 0.8 if args.threshold is None else args.threshold
    neg_matrix = generate_negative_matrix(f"{args.outname}.tsv", threshold=threshold)
    neg_matrix.to_csv(f"{args.outname}_negative_matrix.csv")
    print(f'Elapsed time: {time.time() - start_time} seconds.')

    
if __name__ == '__main__':
    main()

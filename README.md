# scSwitchFilter

## Introduction
Index swithcing is a common problem in single-cell RNA-seq (scRNA-seq) experiments. This phenomenon occurs when the index of a read is swapped with the index of another read during the sequencing process. Index switching happens with a higher rate on sequencers that use patterned flow cells with exclusion amplification chemistry (like HiSeqX, HiSeq4000, and NovaSeq).
Incorrectly assigned reads affect the downstream analysis of scRNA-seq data by mixing signals from different single cells. (http://biorxiv.org/content/early/2017/04/09/125724, https://www.illumina.com/content/dam/illumina-marketing/documents/products/whitepapers/index-hopping-white-paper-770-2017-004.pdf)
In order to correct for the hopped reads in plate-based scRNA-seq experiments, we developed the scSwitchFilter, a python package that can generate find and correct switched reads in plate-based scRNA-seq data. 
scSwitchFiler takes the bam file, parses all single cell reads and analyze all reads that have the same UMI assigned to the same gene across multiple cells with shared i5 or i7 index. Then it generates a correction count matrix for all reads that have been identified as hopped reads.
![image](docs/switching.png)
## Usage
The package can be run as a CLI tool or as a python package. The CLI tool can be run as follows:

'''bash
usage: compute_correction_matrix [-h] [--samtools_path SAMTOOLS_PATH]
                                 [--threshold THRESHOLD] [--tag TAG]
                                 [--index1 INDEX1] [--index2 INDEX2]
                                 filename outname

Generate the correction count matrix for hopped reads in plate-based
sequencing experiments

positional arguments:
  filename              bam file with raw sequencing counts
  outname               output filename

optional arguments:
  -h, --help            show this help message and exit
  --samtools_path SAMTOOLS_PATH
                        path to samtools tool
  --threshold THRESHOLD
                        filtering threshold (default 0.8)
  --tag TAG             Length of the TAG in CB of reads
  --index1 INDEX1       Length of the index1 of reads
  --index2 INDEX2       Length of the index2 of reads
'''
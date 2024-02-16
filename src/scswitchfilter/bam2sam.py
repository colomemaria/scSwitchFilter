import subprocess


def bam2sam(bamfile, outname, samtools_path=None):
    if samtools_path is None:
        subprocess.call(f"samtools view -h -o {outname}.sam {bamfile}", shell=True)
    else:
        subprocess.call(f"{samtools_path} view -h -o {outname}.sam {bamfile}", shell=True)

# sc-switch-filtering

This tools is developed for computational correction of single cell data produced during plate based sequencing experiments. According to several papers (..., ...) modern sequencers are generating false counts because of the new flow cell form(?). Our tool takes the initial bam file and performs the computational correction of sequencing results.

(scheme of index switching stuff and etc)

Current tool has three branches (?):
- main (bam parsing + count matrix correction)
- read_filter (bam parsing + read_id parsing + bam file correction)
- no_bash (experimental branch with only python code)
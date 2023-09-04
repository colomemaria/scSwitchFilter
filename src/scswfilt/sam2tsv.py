import subprocess


def sam2tsv(input_file, output_file):
    cmd = f'''
    #!/usr/bin/bash
    HEADER="gene_id\\tindex1\\tindex2\\ttag\\tumi"
    INPUT_FILE={input_file}
    OUTPUT_FILE={output_file}

    echo -e $HEADER > $OUTPUT_FILE
    # extract rows with reads (skip metadata) from sam file 
    # extract columns GN, CB, UB 
    # extract rows without "-" in columns 
    # remove STAR attribute tags| parse CB to index1, index2, TAG
    grep -E 'GN:Z' $INPUT_FILE|cut -f17,19,20|grep -v ':-'|sed -r 's/(..:Z:)//g'|awk '{{s1=substr($2,1,8)}}{{s2=substr($2,9,8)}}{{s3=substr($2,17,11)}}{{print $1"\\t"s1"\\t"s2"\\t"s3"\\t"$3}}'>>$OUTPUT_FILE
    rm {input_file}
    '''
    subprocess.call(cmd, shell=True)
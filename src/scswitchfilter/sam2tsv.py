import subprocess


def sam2tsv(input_file, output_file, tag_len, index1_len, index2_len):
    if tag_len == 0:
        pos1 = index1_len + 1
        cmd = f'''
                #!/usr/bin/bash
                HEADER="gene_id\\tindex1\\tindex2\\tumi"
                INPUT_FILE={input_file}
                OUTPUT_FILE={output_file}
                INDEX1_LEN={index1_len}
                INDEX2_LEN={index2_len}
                POS1={pos1}

                echo -e $HEADER > $OUTPUT_FILE
                # extract rows with reads (skip metadata) from sam file 
                # extract columns GN, CB, UB 
                # extract rows without "-" in columns 
                # remove STAR attribute tags| parse CB to index1, index2, TAG
                grep -E 'GN:Z' $INPUT_FILE| cut -f17,19,20 | grep -v ':-' | sed -r 's/(..:Z:)//g' | head |
                awk '{{s1=substr($2,1,{index1_len})}} \\
                     {{s2=substr($2,{pos1},{index2_len})}} \\
                     {{print $1"\\t"s1"\\t"s2"\\t"s3"\\t"$3}}' >> $OUTPUT_FILE
            '''
    else:
        pos1 = index1_len + 1
        pos2 = index1_len + index2_len + 1
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
                grep -E 'GN:Z' $INPUT_FILE|cut -f17,19,20|grep -v ':-'|sed -r 's/(..:Z:)//g'| head |
                awk '{{s1=substr($2,1,{index1_len})}} \\
                     {{s2=substr($2,{pos1},{index2_len})}} \\
                     {{s3=substr($2,{pos2},{tag_len})}} \\
                     {{print $1"\\t"s1"\\t"s2"\\t"s3"\\t"$3}}' >> $OUTPUT_FILE
            '''
    subprocess.call(cmd, shell=True)

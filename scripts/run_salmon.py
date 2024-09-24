#!/usr/bin/env python
import os
import pandas as pd
import json
from subprocess import run

# def parse_args():
#     parser = argparse.ArgumentParser(description="Run Salmon for RNA-seq data")
#     parser.add_argument("--index", required=True, help="Input file with sequences")
#     parser.add_argument("--r1", required=True, help="R1 fastq file")
#     parser.add_argument("--r2", required=True, help="R2 fastq file")
#     parser.add_argument("--output", required=True, help="Output directory for Salmon results")
#     parser.add_argument("--sample", required=True, help="Sample name")
#     parser.add_argument("--threads", help="Number of threads", default=multiprocessing.cpu_count())
#     return parser.parse_args()

def run_salmon(index, r1, r2, output, sample, threads):
    # set output paths for salmon run
    quant_dir = os.path.join(output, f'{sample}/quants')
    tsv = os.path.join(quant_dir, 'quant.sf')
    formatted_tsv = os.path.join(quant_dir, f'{sample}.quant.tsv')
    json_file = os.path.join(quant_dir, f'{sample}.quant.json')
    stats = os.path.join(quant_dir, 'aux_info/meta_info.json')

    # ensure output directory exists
    os.makedirs(quant_dir, exist_ok=True)

    # run salmon quant
    run([
        "salmon", "quant", "-i", index, "-l", "A", "-1", r1, "-2", r2,
        "-p", str(threads), "-o", quant_dir, "--validateMappings", "--writeUnmappedNames"
    ])

    # process quant.sf and add sample column
    df = pd.read_csv(tsv, delimiter='\t')
    df['sample'] = sample
    df.to_csv(formatted_tsv, sep='\t', index=False)

    # save to json
    with open(json_file, 'w+') as f:
        json.dump(df.to_dict('records'), f)

    # return dictionary of outputs
    return {
        "quant_dir": quant_dir,
        "tsv": tsv,
        "formatted_tsv": formatted_tsv,
        "json": json_file,
        "stats": stats
    }
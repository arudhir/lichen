#!/usr/bin/env python
import pandas as pd
import argparse
import json
import multiprocessing
from run_salmon import run_salmon

ITS_index = "/mnt/data2/references/unite/ITS"

def parse_args():
    parser = argparse.ArgumentParser(description="Run Salmon for RNA-seq data")
    parser.add_argument("--index", help="Input file with sequences", default=ITS_index)
    parser.add_argument("--r1", required=True, help="R1 fastq file")
    parser.add_argument("--r2", required=True, help="R2 fastq file")
    parser.add_argument("--output", required=True, help="Output directory for Salmon results")
    parser.add_argument("--sample", required=True, help="Sample name")
    parser.add_argument("--threads", help="Number of threads", default=multiprocessing.cpu_count())
    return parser.parse_args()

def process_quantsf(quantsf, tpm_threshold=32):
    # read the file
    df = pd.read_csv(quantsf, delimiter="\t")

    # regex pattern to extract each taxonomic level
    pattern = r'k__(?P<kingdom>[^;]*);p__(?P<phylum>[^;]*)(?:;c__(?P<class>[^;]*))?(?:;o__(?P<order>[^;]*))?(?:;f__(?P<family>[^;]*))?(?:;g__(?P<genus>[^;]*))?(?:;s__(?P<species>[^;]*))?'

    # applying the regex and splitting into columns
    df_taxonomy = df['Name'].str.extract(pattern)

    # concatenate the original dataframe with the new taxonomy columns
    df = pd.concat([df, df_taxonomy], axis=1)

    # filtering and sorting
    df = df.pipe(lambda df: df[df["TPM"] > tpm_threshold])
    df["TPM"] = df["TPM"].astype(float)
    df = df.sort_values(by="TPM", ascending=False)
    df = df.drop(columns=["Name"], axis=1)

    # selecting columns
    df = df.loc[:, ["kingdom", "phylum", "class", "order", "family", "genus", "species", "TPM", "NumReads", "Length", "EffectiveLength"]]

    return df

def main():
    args = parse_args()
    result = run_salmon(args.index, args.r1, args.r2, args.output, args.sample, args.threads)
    quantsf = process_quantsf(result["tsv"])
    print(quantsf['phylum'].value_counts())


if __name__ == "__main__":
    main()

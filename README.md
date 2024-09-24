# lichen
Lichen mining stuff. Right now just assembling transcriptomes. A mix between handwritten code and AI slop.

# High-level Overview

1. Assemble + annotate Lichen transcriptomes
2. Look for evidence of a second fungal partner by mapping to ITS sequences
3. Hunt for novel compounds

## srx2sra.py
We got the SRX IDs for paired-end RNAseq studies on Lecanoromycetes from: https://www.ncbi.nlm.nih.gov/sra/?term=Lecanoromycetes.

We turn those into SRR IDs amenable for `planter`:

```
$ uv run scripts/srx2sra.py
warning: `VIRTUAL_ENV=/home/ubuntu/scripts/venv` does not match the project environment path `.venv` and will be ignored
SRX SRX24880704 -> SRR SRR29366264
```

## `planter`
From the `planter` directory:
```console
docker-compose run --rm planter \
    snakemake \
        --cores 16 \
        --config samples="[SRR29366264, SRR29366265, SRR29366266, SRR22904707, SRR22271585, SRR22271586, SRR22271587, SRR22271588, SRR22271589, SRR19034772, SRR19034773, SRR18070778, SRR18070779, SRR18070780, SRR18070781, SRR18070782, SRR18070783, SRR18070784, SRR18070785, SRR18070786, SRR18070787, SRR18070788, SRR18070789, SRR18070790, SRR18070791, SRR18070792, SRR18070793, SRR18070794, SRR18070795, SRR14292007, SRR14292008, SRR10444679, SRR10444680, SRR10444681, SRR10444682, SRR10444683, SRR10444684, SRR8859643, SRR8859644, SRR8859645, SRR8859646, SRR8859647, SRR8859648, SRR6048009, SRR5489198]" \
        outdir="outputs" \
        s3_bucket="recombia.planter" \
        --keep-going --rerun-incomplete
```

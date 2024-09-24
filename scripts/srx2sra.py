#!/usr/bin/env python

import requests
import time

# function to fetch SRR ID from SRX accession
def get_srr_id(srx):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    efetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    
    # esearch step
    params = {
        "db": "sra",
        "term": srx,
        "retmode": "json"
    }
    
    # request esearch to find the query key and webenv
    response = requests.get(base_url, params=params)
    response.raise_for_status()  # will raise an error for bad responses
    
    # parse the json response to find the SRR ID
    result = response.json()
    if 'esearchresult' in result and 'idlist' in result['esearchresult'] and len(result['esearchresult']['idlist']) > 0:
        sra_id = result['esearchresult']['idlist'][0]
        
        # fetch the run info for this SRA ID
        efetch_params = {
            "db": "sra",
            "rettype": "runinfo",
            "id": sra_id,
            "retmode": "text"
        }
        
        run_info = requests.get(efetch_url, params=efetch_params)
        run_info.raise_for_status()
        
        # parse and find the SRR ID in the run info output
        for line in run_info.text.splitlines():
            if line.startswith("SRR"):
                return line.split(",")[0]
    return None

# read the SRX accessions from the file
with open('data/lichen-srx.txt', 'r') as f:
    srx_list = [line.strip() for line in f]

# open a file to save the output
with open('data/lichen-srr.txt', 'w') as output_file:
    for srx in srx_list:
        try:
            srr = get_srr_id(srx)
            if srr:
                output_file.write(f"{srx}: {srr}\n")
                print(f"SRX {srx} -> SRR {srr}")
            else:
                print(f"No SRR found for {srx}")
            # avoid getting rate-limited
            time.sleep(3)  # adjust this delay if needed
        except Exception as e:
            print(f"Error processing {srx}: {e}")

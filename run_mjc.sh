#!/usr/bin/env bash
# Run multijurisdiction HIV-TRACE analysis
# Calls `merge_fasta.py` to merge individual jurisdictions' aligned FASTAs, and then runs HIV-TRACE starting with TN93

# define variables for analysis
PYTHON=$python                                 # path to `python` executable
MJC_MERGE_FASTA_SCRIPT=$mjc_merge_fasta_script # path to `merge_fasta.py` script
MJC_OUTPUT_FASTA=$mjc_output_fasta             # path to a single output FASTA file
MJC_OUTPUT_JSON=$mjc_output_json               # path to a single output JSON file
MJC_INPUT_FASTAS=$mjc_input_fastas             # bash array containing >1 paths to input FASTA files

# fix `MJC_INPUT_FASTAS` if it was interpreted as a single string "(...)" instead of an array of strings
if [[ "$MJC_INPUT_FASTAS" =~ ^\(.+\)$ ]]; then
    read -r -a MJC_INPUT_FASTAS <<< "${MJC_INPUT_FASTAS:1:${#MJC_INPUT_FASTAS}-2}"
fi

# check variables for validity
if [ -f "$MJC_OUTPUT_FASTA" ] ; then echo "Output FASTA file ($MJC_OUTPUT_FASTA) already exists" ; exit 1 ; fi
if [ -f "$MJC_OUTPUT_JSON" ] ; then echo "Output JSON file ($MJC_OUTPUT_JSON) already exists" ; exit 1 ; fi
if [ ${#MJC_INPUT_FASTAS[@]} -eq 0 ] ; then echo "No input FASTA files specified" ; exit 1 ; fi
for mjc_input_fasta in "${MJC_INPUT_FASTAS[@]}" ; do
    if [ ! -f "$mjc_input_fasta" ] ; then echo "Input FASTA file ($mjc_input_fasta) not found" ; exit 1 ; fi
done

# run `merge_fasta.py`
echo $PYTHON $MJC_MERGE_FASTA_SCRIPT -of $MJC_OUTPUT_FASTA -oj $MJC_OUTPUT_JSON "${MJC_INPUT_FASTAS[@]}"
$PYTHON $MJC_MERGE_FASTA_SCRIPT -of $MJC_OUTPUT_FASTA -oj $MJC_OUTPUT_JSON "${MJC_INPUT_FASTAS[@]}"

# run HIV-TRACE pipeline, starting with feeding `$MJC_OUTPUT_FASTA` to TN93
# TODO

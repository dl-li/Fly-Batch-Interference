# FBI - Fly Batch Interference: Batch Design RNAi Primers for Drosophila

[中文](/README.md) | English

This script operates the browser to visit [DSIR](http://biodev.cea.fr/DSIR/DSIR.html) to calculate target sequences, then designs shRNA primers according to [Ni Lab's Protocol](http://www.bio-protocol.org/e3158). **Note: The generated primer specificity has not been verified through [BLAST](https://flybase.org/blast/)**, please verify before use.

## Preparation
- **Python** and **selenium** package
- **WebDriver**:
    Go to the browser developer website to download the corresponding WebDriver. Here we use Microsoft Edge browser's msedgedriver, **note that the version number must match the browser version**. After downloading, place it in the project root directory.
- **FASTA file**:
    Prepare a single FASTA file containing all target sequences. You can use FlyBase ID Validator to batch obtain FlyBase IDs, then use FlyBase Sequence Downloader's "Bulk ID" mode to get compliant FASTA files. If you have multiple FASTA files, you can use the `join_fasta_files.py` script to merge them.

## join_fasta_files.py: Merge Multiple FASTA Files
```python
directory = "all fasta files"  # Change this to your directory path
output_file = "merged.fasta"  # Output file name
all_sequences = False  # True=merge all sequences, False=only the first sequence from each file
```

## get_AS_seq.py: Get AS Sequence Based on Target Sequences
After ensuring msedgedriver is placed in the project root directory, fill in the input and output paths
```python
fasta_file = "Example.fasta"
output_csv = "AS_results.csv"
```
Run the script and wait for completion. (It has been observed that if DSIR returns no results, it will wait for a while before processing the next sequence, please be patient)
The output CSV file contains the input target sequences and the top five AS Sequences calculated by DSIR.

## get_primers.py: Design Primers Based on AS Sequence
Fill in the input and output paths
```python
def main():
    input_file = 'AS_results.csv'
    output_file = 'Primer_results.csv'
```
Optionally output primers with bulges for better silencing effect.
```python
def main():
    ...
    generate_primers(row['AS Sequence - 1'], introduce_bulges=True)
```
Run the script to get a CSV file containing primer sequences.
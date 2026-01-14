# FBI - Fly Batch Interference: Batch Design RNAi Primers for Drosophila

[中文](/README.md) | English

This script operates the browser to visit [DSIR](http://biodev.cea.fr/DSIR/DSIR.html) to calculate target sequences, then designs shRNA primers according to [Ni Lab's Protocol](http://www.bio-protocol.org/e3158). **Note: The generated primer specificity has not been verified through [BLAST](https://flybase.org/blast/)**, please verify before use.

## Preparation
- **Python** and **selenium** package
- **WebDriver**:
    Go to the browser developer website to download the corresponding WebDriver. Here we use Microsoft Edge browser's msedgedriver, **note that the version number must match the browser version**. After downloading, place it in the project root directory.
- **Biopython**:
    Used for calling NCBI BLAST API for sequence verification. Can be installed using `pip install biopython` or `uv add biopython`.
- **FASTA file**:
    Prepare a single FASTA file containing all target sequences. You can use FlyBase ID Validator to batch obtain FlyBase IDs, then use FlyBase Sequence Downloader's "Bulk ID" mode to get compliant FASTA files. If you have multiple FASTA files, you can use the `join_fasta_files.py` script to merge them.

## join_fasta_files.py: Merge Multiple FASTA Files
```python
# Input directory: Directory containing multiple FASTA files
directory = os.path.join(project_root, "example", "all fasta files")

# Output file: Merged FASTA file
output_file = os.path.join(project_root, "example", "merged.fasta")

# Whether to merge all sequences (False=only first sequence from each file)
all_sequences = False
```

## get_AS_seq.py: Get AS Sequence Based on Target Sequences
After ensuring msedgedriver is placed in the project root directory, fill in the input and output paths
```python
fasta_file = os.path.join(project_root, "example", "Example.fasta")
output_csv = os.path.join(project_root, "example", "AS_results.csv")
```
Run the script and wait for completion. (It has been observed that if DSIR returns no results, it will wait for a while before processing the next sequence, please be patient)
The output CSV file contains the input target sequences and the top five AS Sequences calculated by DSIR.

## get_primers.py: Design Primers Based on AS Sequence with BLAST Verification
Fill in the input and output paths
```python
def main():
    input_file = os.path.join(project_root, 'example', 'AS_results.csv')
    output_file = os.path.join(project_root, 'example', 'Primer_results.csv')
```
Optionally output primers with bulges for better silencing effect.
```python
def main():
    ...
    forward_primer, reverse_primer = generate_primers(as_sequence, introduce_bulges=True)
```
Run the script to get a CSV file containing:
- Flybase ID
- AS Sequence
- AS Sequence Number
- Primer-F (forward primer)
- Primer-R (reverse primer)
- Max Non-Target Match (maximum non-target site match)

**Note**: The script will automatically perform BLAST verification for each AS Sequence, which requires network connection. The verification process may take some time to complete.
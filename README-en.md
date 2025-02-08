# FBI - Fly Batch Interference: Batch Design RNAi Primers for Drosophila

[中文](/README.md) | English

These scripts navigates to [DSIR](http://biodev.cea.fr/DSIR/DSIR.html) to calculate the target sequence, then designs shRNA primers based on [Ni Lab's Protocol](http://www.bio-protocol.org/e3158). **Note: The designed primers' specificity has not been verified by BLAST (https://flybase.org/blast/).** Please verify their specificity before use.

## Preparation
- **Python** and the **selenium** library
- **WebDriver**: 
    Go to the developer's website of the browser you are using to download the corresponding WebDriver. Here, Microsoft Edge browser's msedgedriver is used. **Ensure that the version number matches the browser version**. After downloading, place it in the project root directory.
- **FASTA File**: 
    Prepare a single FASTA file containing all target sequences. You can obtain FlyBase IDs in bulk with the help of the FlyBase ID Validator, and then use the "Bulk ID" mode of the FlyBase Sequence Downloader to obtain the FASTA files.

## get_AS_seq.py
Ensure that msedgedriver is placed in the project root directory after installation. Fill in the input and output paths as follows:
```python
fasta_file = "Example.fasta"
output_csv = "AS_results.csv"
```
Run the script, and wait for the operation to complete. (It's observed that if DSIR returns no results, it will wait for a while before operating on the next sequence, please be patient)
The resulting CSV file contains the input sequences and the top five "AS Sequence" outputs.

## get_primers.py
Fill in the input and output paths as follows:
```python
def main():
    input_file = 'AS_results.csv'
    output_file = 'Primer_results.csv'
```
Optionally, generate primers with a bulge for better silence effect.
```python
def main():
    ...
    generate_primers(row['AS Sequence - 1'], introduce_bulges=True)
```
Run the script to obtain a CSV file containing the sequences of the designed primers.
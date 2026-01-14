import csv
import os
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML

# Get project root directory
project_root = os.path.dirname(os.path.abspath(__file__))

def main():
    # 输入文件：包含AS序列的CSV文件
    input_file = os.path.join(project_root, 'example', 'AS_results.csv')
    
    # 输出文件：存储引物设计结果和BLAST验证结果
    output_file = os.path.join(project_root, 'example', 'Primer_results.csv')
    output_data = []
    
    with open(input_file, mode='r') as infile:
        # First pass: count total rows
        reader = csv.DictReader(infile)
        total = sum(1 for row in reader)
        
        # Second pass: process rows
        infile.seek(0)
        reader = csv.DictReader(infile)  # Create new reader
        next(reader)  # Skip header
        
        for index, row in enumerate(reader, start=1):
            flybase_id = row['Flybase ID']
            print(f"Processing {index}/{total}: {flybase_id}...")
            
            # Process each AS Sequence
            for i in range(1, 6):
                as_seq_key = f'AS Sequence - {i}'
                as_sequence = row[as_seq_key]
                
                if as_sequence:
                    # Generate primers
                    forward_primer, reverse_primer = generate_primers(as_sequence)
                    
                    # Perform BLAST verification
                    max_non_target_match = blast_verification(as_sequence)
                    
                    # Store result
                    new_row = {
                        'Flybase ID': flybase_id,
                        'AS Sequence': as_sequence,
                        'AS Sequence Number': i,
                        'Primer-F': forward_primer,
                        'Primer-R': reverse_primer,
                        'Max Non-Target Match': max_non_target_match
                    }
                    output_data.append(new_row)
    
    # Write results to output file
    if output_data:
        with open(output_file, mode='w', newline='') as outfile:
            fieldnames = ['Flybase ID', 'AS Sequence', 'AS Sequence Number', 'Primer-F', 'Primer-R', 'Max Non-Target Match']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            for data in output_data:
                writer.writerow(data)
        print(f"Script completed. Results saved to {output_file}.")
    else:
        print("No AS sequences found to process.")

def generate_primers(sequence, sequence_type="as-sequence", introduce_bulges=False):
    # Generate PCR primers based on the input sequence.

    # Parameters:
    # sequence (str): The input DNA sequence (21 nucleotides).
    # sequence_type (str): Type of the input sequence. Can be 'as-sequence' or 'as-recom'.
    #                      If 'as-sequence', the reverse complement of the input sequence is used.
    #                      If 'as-recom', the input sequence is used directly.
    # introduce_bulges (bool): Whether to introduce bulges in the primers. Default is False.
    #                          If True, specific positions in the primers are replaced with their complementary bases.

    # Returns:
    # tuple: A tuple containing two strings representing the forward and reverse primers.

    def reverse_complement(seq):
        complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
        return ''.join(complement[base] for base in reversed(seq))

    # Preprocess the input sequence
    my_seq = sequence.replace(" ", "").upper().replace("U", "T")

    # Check if the sequence type is as-sequence and take the reverse complement
    if sequence_type == "as-sequence":
        my_seq = reverse_complement(my_seq)

    # Check if the length of the sequence is 21 nucleotides
    if len(my_seq) != 21:
        raise ValueError("Error: Input sequence must be 21 nucleotides long.")

    # Calculate the reverse complement of mySeq
    rc_seq = reverse_complement(my_seq)

    # Build the forward and reverse primers
    primer_f_sequence = f"ctagcagt{my_seq}tagttatattcaagcata{rc_seq}gcg"
    primer_r_sequence = f"aattcgc{my_seq}tatgcttgaatataacta{rc_seq}actg"

    # Introduce bulges if specified
    if introduce_bulges:
        complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
        
        # Replace bases at positions 18 and 27 in primer F with their complements
        primer_f_sequence = list(primer_f_sequence)
        primer_f_sequence[18] = complement[primer_f_sequence[18]]
        primer_f_sequence[27] = complement[primer_f_sequence[27]]
        primer_f_sequence = ''.join(primer_f_sequence)

        # Replace bases at positions 47 and 56 in primer R with their complements
        primer_r_sequence = list(primer_r_sequence)
        primer_r_sequence[47] = complement[primer_r_sequence[47]]
        primer_r_sequence[56] = complement[primer_r_sequence[56]]
        primer_r_sequence = ''.join(primer_r_sequence)

    return primer_f_sequence, primer_r_sequence

def blast_verification(sequence):
    """
    Perform BLAST verification for a sequence and return max non-target match.
    
    Parameters:
    sequence (str): The AS Sequence to BLAST
    
    Returns:
    str: Max non-target match in format "x/y"
    """
    try:
        # Ensure sequence is 21nt
        if len(sequence) != 21:
            print(f"Warning: Sequence length is {len(sequence)}, expected 21. Skipping BLAST.")
            return "0/0"
        
        # Convert RNA sequence (U) to DNA sequence (T) for BLAST
        dna_sequence = sequence.replace('U', 'T')
        
        # Perform BLAST search
        result_handle = NCBIWWW.qblast(
            program="blastn",
            database="nr",
            sequence=dna_sequence,
            entrez_query="Drosophila melanogaster[Organism]",
            hitlist_size=50,
            expect=10,
            filter=False,
            gapcosts="5 2",
            word_size=11
        )
        
        # Parse results
        blast_record = NCBIXML.read(result_handle)
        result_handle.close()
        
        max_non_target_match = "0/0"
        current_max = 0
        current_length = 0
        
        # Iterate through alignments
        for alignment in blast_record.alignments:
            for hsp in alignment.hsps:
                # Calculate match length and identities
                match_length = hsp.align_length
                identities = hsp.identities
                
                # Check if this is not a perfect match (21/21)
                if not (match_length == 21 and identities == 21):
                    # Update max non-target match if this is higher
                    if identities > current_max or (identities == current_max and match_length > current_length):
                        current_max = identities
                        current_length = match_length
                        max_non_target_match = f"{identities}/{match_length}"
        
        return max_non_target_match
        
    except Exception as e:
        print(f"Error during BLAST: {e}")
        return "0/0"

if __name__ == "__main__":
    main()
import csv
def main():
    input_file = 'AS_results.csv'
    output_file = 'Primer_results.csv'
    output_data = []
    with open(input_file, mode='r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            if row['AS Sequence - 1']:
                # 调用 generate_primers 函数，设置 introduce_bulges 为 True
                forward_primer, reverse_primer = generate_primers(row['AS Sequence - 1'])
                # 存储原始数据和新生成的引物信息
                new_row = {
                    'Flybase ID': row['Flybase ID'],
                    'Sequence': row['Sequence'],
                    'AS Sequence - 1': row['AS Sequence - 1'],
                    'Primer-F': forward_primer,
                    'Primer-R': reverse_primer
                }
                output_data.append(new_row)
            else:
                # 对于 AS Sequence - 1 列无内容的行，直接存储原始数据
                new_row = {
                    'Flybase ID': row['Flybase ID'],
                    'Sequence': row['Sequence'],
                    'AS Sequence - 1': row['AS Sequence - 1'],
                    'Primer-F': '',
                    'Primer-R': ''
                }
                output_data.append(new_row)

    # 将结果写入输出文件
    with open(output_file, mode='w', newline='') as outfile:
        fieldnames = ['Flybase ID', 'Sequence', 'AS Sequence - 1', 'Primer-F', 'Primer-R']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in output_data:
            writer.writerow(data)

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

if __name__ == "__main__":
    main()
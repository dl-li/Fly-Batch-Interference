import os
import argparse
from pathlib import Path

# Get project root directory
project_root = os.path.dirname(os.path.abspath(__file__))

# 将多个fasta文件合并为一个文件
# 输入目录：包含多个FASTA文件的目录
directory = os.path.join(project_root, "example", "all fasta files")

# 输出文件：合并后的FASTA文件
output_file = os.path.join(project_root, "example", "merged.fasta")

# 是否合并所有序列（False=只取每个文件的第一个序列）
all_sequences = False



def join_fasta_files(directory, output_file, all_sequences=False):
    """
    Join all FASTA files in a directory into one file.
    
    Args:
        directory: Directory containing FASTA files
        output_file: Output FASTA file path
        all_sequences: If True, join all sequences; if False, only first sequence from each file
    """
    fasta_extensions = {'.fasta', '.fa', '.fas', '.fna'}
    
    with open(output_file, 'w') as outfile:
        for file_path in Path(directory).glob('*'):
            if file_path.suffix.lower() in fasta_extensions and file_path.is_file():
                with open(file_path, 'r') as infile:
                    sequences_written = 0
                    current_sequence = []
                    header = None
                    
                    for line in infile:
                        line = line.strip()
                        if line.startswith('>'):
                            # Write previous sequence if exists
                            if header and current_sequence:
                                outfile.write(f"{header}\n")
                                outfile.write(f"{''.join(current_sequence)}\n")
                                sequences_written += 1
                                
                                # If only first sequence needed, break
                                if not all_sequences:
                                    break
                            
                            # Start new sequence
                            header = line
                            current_sequence = []
                        else:
                            current_sequence.append(line)
                    
                    # Write last sequence
                    if header and current_sequence and (all_sequences or sequences_written == 0):
                        outfile.write(f"{header}\n")
                        outfile.write(f"{''.join(current_sequence)}\n")

def main():
    parser = argparse.ArgumentParser(description='Join FASTA files in a directory')
    
    # 检查目录是否存在
    if not os.path.exists(directory):
        print(f"错误: 目录 '{directory}' 不存在")
        return
    
    # 执行合并
    join_fasta_files(directory, output_file, all_sequences)
    print(f"FASTA文件合并完成。输出文件: {output_file}")
    print(f"模式: {'所有序列' if all_sequences else '仅第一个序列'}")

if __name__ == "__main__":
    main()
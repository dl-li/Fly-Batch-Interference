import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# 指定一个多个序列的fasta文件，然后使用DSIR工具来获取每个序列的AS序列，将结果保存到一个CSV文件中。
# 需要安装浏览器对应的 WebDriver，这里使用的是 Edge 浏览器，所以需要下载 Edge WebDriver。注意：WebDriver 的版本要与浏览器版本匹配。

# Input/output file paths
fasta_file = "Example.fasta"
output_csv = "AS_results.csv"

# Initialize WebDriver
options = webdriver.EdgeOptions()
driver = webdriver.Edge(options=options)

# URL of the DSIR webpage
url = "http://biodev.cea.fr/DSIR/DSIR.html"

# Function to parse the fasta file
def parse_fasta(file_path):
    sequences = []
    with open(file_path, "r") as file:
        lines = file.readlines()
        current_id = ""
        current_seq = ""
        for line in lines:
            if line.startswith(">"):
                if current_id and current_seq:
                    sequences.append((current_id, current_seq))
                current_id = line.strip().split()[0][1:]
                current_seq = ""
            else:
                current_seq += line.strip()
        if current_id and current_seq:
            sequences.append((current_id, current_seq))
    return sequences

# Function to handle each sequence
def process_sequence(seq_id, sequence):
    try:
        driver.get(url)
        
        # Fill in the seqname field
        seqname_field = driver.find_element(By.NAME, "seqname")
        seqname_field.clear()
        seqname_field.send_keys(seq_id)

        # Fill in the sequence_all field
        sequence_field = driver.find_element(By.NAME, "sequence_all")
        sequence_field.clear()
        sequence_field.send_keys(f">{seq_id}\n{sequence}")

        # Click the Run analysis button
        run_button = driver.find_element(By.XPATH, "//input[@value='Run analysis']")
        run_button.click()

        # Wait for the results page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "result")))

        # Extract the AS sequences
        table = driver.find_element(By.CLASS_NAME, "result")
        rows = table.find_elements(By.TAG_NAME, "tr")
        as_sequences = []
        for i in range(1, 6):  # Extract rows 2 to 6 (index 1 to 5)
            try:
                as_sequences.append(rows[i].find_elements(By.TAG_NAME, "td")[4].text)
            except IndexError:
                as_sequences.append("")

        print(f"AS sequence for {seq_id}: {as_sequences[0]}")  # Print only the first AS sequence
        return as_sequences
    except (TimeoutException, NoSuchElementException):
        try:
            # Click the Home page link to return to the main page
            home_button = driver.find_element(By.XPATH, "//a[@class='sidelink' and @href='DSIR.html']")
            home_button.click()
        except NoSuchElementException:
            driver.get(url)
        print(f"No AS sequences found for {seq_id}")
        return ["" for _ in range(5)]
    except Exception as e:
        print(f"Error processing {seq_id}: {e}")
        return ["" for _ in range(5)]

# Main script
sequences = parse_fasta(fasta_file)

total = len(sequences)
with open(output_csv, "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Flybase ID", "Sequence", "AS Sequence - 1", "AS Sequence - 2", "AS Sequence - 3", "AS Sequence - 4", "AS Sequence - 5"])

    for index, (seq_id, sequence) in enumerate(sequences, start=1):
        print(f"Processing {index}/{total}: {seq_id}...")
        as_sequences = process_sequence(seq_id, sequence)
        csvwriter.writerow([seq_id, sequence] + as_sequences)

# Close the WebDriver
driver.quit()

print("Script completed. Results saved to output.csv.")

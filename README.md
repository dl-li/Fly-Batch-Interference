# FBI - Fly Batch Interference: 批量设计果蝇RNAi引物

中文 | [English](/README-en.md)

该脚本操作浏览器前往[DSIR](http://biodev.cea.fr/DSIR/DSIR.html)计算靶向序列，再根据[Ni Lab's Protocol](http://www.bio-protocol.org/e3158)设计shRNA的引物。

## 准备工作
- **Python**和**selenium**包
- **WebDriver**：
    前往浏览器的开发者网站下载对应的WebDriver。此处使用Microsoft Edge浏览器的msedgedriver，**注意版本号一定与浏览器版本对应**。下载好后存放在项目根目录下。
- **Biopython**：
    用于调用NCBI BLAST API进行序列验证。可以使用`pip install biopython`或`uv add biopython`安装。
- **FASTA文件**：
    准备包含所有目标序列的单个FASTA文件。可以借助FlyBase  ID Validator批量获取FlyBase ID，然后使用FlyBase  Sequence Downloader的“Bulk ID”模式获取符合要求的FASTA文件。如果有多个FASTA文件，可以使用`join_fasta_files.py`脚本合并。

## join_fasta_files.py：合并多个FASTA文件
```python
# 输入目录：包含多个FASTA文件的目录
directory = os.path.join(project_root, "example", "all fasta files")

# 输出文件：合并后的FASTA文件
output_file = os.path.join(project_root, "example", "merged.fasta")

# 是否合并所有序列（False=只取每个文件的第一个序列）
all_sequences = False
```

## get_AS_seq.py: 根据靶向序列获取AS Sequence
确保msedgedriver放置在项目根目录下后，填写输入输出路径
```python
fasta_file = os.path.join(project_root, "example", "Example.fasta")
output_csv = os.path.join(project_root, "example", "AS_results.csv")
```
运行脚本，静待操作完成。（观察到如果DSIR返回无结果，会等待一段时间再操作下一个序列，请耐心等待）
输出的cvs文件包含输入的被靶向序列和DSIR计算输出的前五个AS Sequence。

## get_primers.py：根据AS Sequence设计引物并进行BLAST验证
填写输入输出路径
```python
def main():
    input_file = os.path.join(project_root, 'example', 'AS_results.csv')
    output_file = os.path.join(project_root, 'example', 'Primer_results.csv')
```
可选输出带有隆起(bulge)的引物，沉默效果更好。
```python
def main():
    ...
    forward_primer, reverse_primer = generate_primers(as_sequence, introduce_bulges=True)
```
运行脚本，得到包含以下信息的csv文件：
- Flybase ID
- AS Sequence
- AS Sequence Number
- Primer-F（正向引物）
- Primer-R（反向引物）
- Max Non-Target Match（非靶向位点最大配对数）

**注意**：脚本会自动对每个AS Sequence进行BLAST验证，需要网络连接。验证过程可能需要较长时间完成。
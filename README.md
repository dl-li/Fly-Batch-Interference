# FBI - Fly Batch Interference: 批量设计果蝇RNAi引物

中文 | [English](/README-en.md)

该脚本操作浏览器前往[DSIR](http://biodev.cea.fr/DSIR/DSIR.html)计算靶向序列，再根据[Ni Lab's Protocol](http://www.bio-protocol.org/e3158)设计shRNA的引物。**注意：生成的引物特异性未经[BLAST](https://flybase.org/blast/)验证**，请在使用前自行验证。

## 准备工作
- **Python**和**selenium**包
- **WebDriver**：
    前往浏览器的开发者网站下载对应的WebDriver。此处使用Microsoft Edge浏览器的msedgedriver，**注意版本号一定与浏览器版本对应**。下载好后存放在项目根目录下。
- **FASTA文件**：
    准备包含所有目标序列的单个FASTA文件。可以借助FlyBase  ID Validator批量获取FlyBase ID，然后使用FlyBase  Sequence Downloader的“Bulk ID”模式获取符合要求的FASTA文件。如果有多个FASTA文件，可以使用`join_fasta_files.py`脚本合并。

## join_fasta_files.py：合并多个FASTA文件
```python
directory = "all fasta files"  # 修改这里为你的目录路径
output_file = "merged.fasta"  # 输出文件名
all_sequences = False  # True=合并所有序列, False=只要每个文件的第一个序列
```

## get_AS_seq.py: 根据靶向序列获取AS Sequence
确保msedgedriver放置在项目根目录下后，填写输入输出路径
```python
fasta_file = "Example.fasta"
output_csv = "AS_results.csv"
```
运行脚本，静待操作完成。（观察到如果DSIR返回无结果，会等待一段时间再操作下一个序列，请耐心等待）
输出的cvs文件包含输入的被靶向序列和DSIR计算输出的前五个AS Sequence。

## get_primers.py：根据AS Sequence设计引物
填写输入输出路径
```python
def main():
    input_file = 'AS_results.csv'
    output_file = 'Primer_results.csv'
```
可选输出带有隆起(bulge)的引物，沉默效果更好。
```python
def main():
    ...
    generate_primers(row['AS Sequence - 1'], introduce_bulges=True)
```
运行脚本，得到含有引物序列的csv文件。
# Notion_douban

从豆瓣获取书籍信息并保存到Notion的脚本

## 使用方法



1. 获取脚本

   ```python
   git clone git@github.com:lyh081/Notion_douban.git
   ```

   

2. 替换token和database_id

   ```python
   def main():
       token = ' ' # 在这里填写token
       database_id = ' ' # 在这里填写database_id
       if token == ' ' or database_id == ' ':
           print("请在代码中的填写token和database_id")
           return 0
   ```

   

3. 使用

   ```bash
   python doubanBook.py -u 'https://book.douban.com/subject/35325887/' -t "非虚构"
   cd Notion_Douban
   pip install -r requirements.txt
   ```

   命令行参数:

   ```bash
   python doubanBook.py -h
   /***
   usage: doubanBook.py [-h] [--url URL] [--tag TAG] [--status STATUS]
   
   Notion-doubanBook
   
   optional arguments:
     -h, --help            show this help message and exit
     --url URL, -u URL     豆瓣读书链接
     --tag TAG, -t TAG     自定义标签，默认为空
     --status STATUS, -s STATUS
                           阅读状态（未读，在读，读完），默认为未读
   ***/
   ```

   

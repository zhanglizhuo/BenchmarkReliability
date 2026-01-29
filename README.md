# ResearchBuddy
Find research buddy / 查找科研合作伙伴

## 功能 (Features)

从大学网站自动查找适合的科研合作人选，筛选条件包括：
- 讲师 + 博士学历 + 有科研论文（优先）
- 副教授（备选）

Automatically find suitable research collaborators from university websites, filtering for:
- Lecturers with PhD and research papers (priority)
- Associate professors (fallback)

## 安装 (Installation)

```bash
pip install -r requirements.txt
```

## 使用方法 (Usage)

### 基本用法 (Basic Usage)

使用默认URL:
```bash
python find_collaborator.py
```

使用自定义URL:
```bash
python find_collaborator.py https://nxy.hunau.edu.cn/xygk/szdw_9365/
```

### 示例输出 (Example Output)

```
正在访问: https://nxy.hunau.edu.cn/xygk/szdw_9365/
正在解析教师信息...
共找到 50 位教师信息

正在筛选合适的合作候选人...

优先推荐 (讲师 + 博士 + 科研论文):
================================================================================

1. 姓名: 张伟
   职称: 讲师
   学历: 博士
   有科研成果: 是
   简介: 张伟，讲师，博士，研究方向：人工智能与机器学习，发表SCI论文10余篇...
```

## 依赖 (Dependencies)

- Python 3.6+
- requests
- beautifulsoup4
- lxml

## 说明 (Notes)

该工具会自动解析网页中的教师信息，提取职称、学历和科研情况。由于不同网站的HTML结构可能不同，可能需要根据实际情况调整解析逻辑。

This tool automatically parses faculty information from web pages. Since different websites have different HTML structures, you may need to adjust the parsing logic accordingly.

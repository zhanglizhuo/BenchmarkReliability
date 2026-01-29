# ResearchBuddy - 教师信息分析工具

## 项目说明

ResearchBuddy 是一个用于抓取和分析大学教师个人主页的工具，帮助您快速找到符合要求的研究导师或合作者。

## 主要功能

1. **自动抓取教师信息**
   - 从教师列表页面获取所有教师链接
   - 自动访问每位教师的个人主页
   - 提取关键信息：姓名、职称、系别、研究方向、教育背景、联系方式等

2. **智能筛选**
   - 按职称筛选（教授、副教授、研究员等）
   - 按研究关键词筛选（作物、育种、遗传等）
   - 按学历要求筛选（博士、硕士等）

3. **结果导出**
   - 控制台显示匹配的教师信息
   - JSON 格式保存完整数据，便于进一步分析

## 使用方法

### 1. 演示模式（推荐先尝试）

```bash
python demo.py
```

演示模式使用示例数据，展示工具的完整功能：
- 5位示例教师的完整信息
- 按条件筛选的演示
- 输出格式展示

### 2. 实际使用

```bash
python research_buddy.py
```

工具已预配置为抓取湖南农业大学农学院的教师信息：
https://nxy.hunau.edu.cn/xygk/szdw_9365/

## 自定义筛选条件

编辑 `research_buddy.py` 文件中的 `criteria` 字典（约第253行）：

```python
criteria = {
    'required_titles': ['教授', '副教授'],           # 需要的职称
    'research_keywords': ['作物', '育种', '遗传'],  # 研究关键词
    'required_degree': '博士'                       # 学历要求
}
```

## 输出示例

### 控制台输出
```
Teachers matching criteria: 3 out of 5
================================================================================

1. 张教授 ✓
   Title: 教授
   Department: 作物遗传育种系
   Research Areas: 水稻分子育种, 作物遗传改良, 功能基因组学
   Email: zhangprof@hunau.edu.cn
   Phone: 0731-12345678
   URL: https://...
```

### JSON 输出
保存在 `teacher_profiles.json` 文件中，包含所有匹配教师的详细信息。

## 使用场景

### 1. 找研究生导师
```python
criteria = {
    'required_titles': ['教授', '副教授', '研究员'],
    'research_keywords': ['作物', '遗传', '育种'],
    'required_degree': '博士'
}
```

### 2. 找特定研究方向的老师
```python
criteria = {
    'research_keywords': ['植物病理', '病害防治', '生物农药']
}
```

### 3. 找高级职称教师
```python
criteria = {
    'required_titles': ['教授', '研究员']
}
```

## 工作原理

1. **页面抓取**：使用 requests 库获取网页内容
2. **内容解析**：使用 BeautifulSoup 解析 HTML
3. **信息提取**：使用正则表达式提取结构化信息
4. **条件匹配**：根据设定的条件筛选教师
5. **结果输出**：格式化显示并保存为 JSON

## 技术特性

- **速度控制**：自动添加请求延迟，避免对服务器造成压力
- **错误处理**：网络错误自动处理，继续处理其他教师
- **编码支持**：自动检测中文编码，正确显示中文内容
- **安全检查**：验证URL域名，防止恶意重定向
- **类型提示**：完整的类型注解，代码更易维护

## 注意事项

1. 需要网络连接访问目标网站
2. 某些网络环境可能限制网页抓取
3. 只抓取公开可访问的信息
4. 使用合理的延迟，尊重目标服务器

## 安装依赖

```bash
pip install -r requirements.txt
```

需要的包：
- requests：HTTP 请求
- beautifulsoup4：HTML 解析
- lxml：XML/HTML 解析器

## 更多信息

详细使用说明请参考 [USAGE.md](USAGE.md)

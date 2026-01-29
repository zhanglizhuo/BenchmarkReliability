# 使用示例 / Usage Examples

## 示例1：运行主程序（需要网络访问）

```bash
# 使用默认URL
python find_collaborator.py

# 使用自定义URL
python find_collaborator.py https://your-university.edu/faculty/
```

## 示例2：测试模式（使用模拟数据）

```bash
# 测试正常情况（找到讲师+博士）
python test_mock.py

# 测试备选方案（只有副教授）
python test_fallback.py
```

## 输出说明

### 优先推荐
程序会首先查找：
- 职称：讲师
- 学历：博士
- 有科研论文发表

### 备选推荐
如果没有找到符合优先条件的候选人，程序会显示：
- 职称：副教授
- 任意学历

## 自定义解析规则

如果目标网站的HTML结构不同，可以修改 `find_collaborator.py` 中的以下方法：
- `parse_faculty_info()`: 调整HTML元素选择器
- `extract_info()`: 修改信息提取规则

## 注意事项

1. 确保安装了所需的依赖：`pip install -r requirements.txt`
2. 某些网站可能需要特殊的请求头或登录
3. 建议先使用测试脚本验证功能

# ResearchBuddy Usage Guide

## Quick Start

### 1. Demo Mode (Recommended for Testing)
Try the demo first to see how the tool works:

```bash
python demo.py
```

This will:
- Use sample teacher data
- Show all extracted profiles
- Demonstrate filtering by criteria
- Save results to `demo_results.json`

### 2. Production Mode
To scrape real data from the target website:

```bash
python research_buddy.py
```

**Note:** This requires internet access to https://nxy.hunau.edu.cn/

## Customizing Search Criteria

Edit the `criteria` dictionary in `research_buddy.py` (around line 253):

```python
criteria = {
    'required_titles': ['教授', '副教授', 'Professor'],
    'research_keywords': ['作物', '育种', '遗传', '分子生物学'],
    'required_degree': '博士'
}
```

### Criteria Options

- **required_titles**: List of acceptable academic titles (e.g., '教授', '副教授', '研究员')
- **research_keywords**: Keywords to match in research areas (e.g., '遗传', '育种', '基因')
- **required_degree**: Required education level (e.g., '博士', 'PhD')

## Understanding the Output

### Console Output

The tool displays:
1. Progress as it fetches each teacher profile
2. Total number of profiles found
3. List of teachers matching your criteria with key information

### JSON Output

Results are saved to `teacher_profiles.json` (or `demo_results.json` in demo mode) with:

```json
{
  "total_profiles": 5,
  "matched_profiles": 3,
  "criteria": { ... },
  "profiles": [
    {
      "name": "张教授",
      "title": "教授",
      "department": "作物遗传育种系",
      "research_areas": ["水稻分子育种", "作物遗传改良"],
      "education": ["..."],
      "contact": {
        "email": "example@university.edu",
        "phone": "..."
      },
      "url": "..."
    }
  ]
}
```

## Advanced Usage

### Changing the Target URL

Edit `research_buddy.py` (line 252):

```python
url = "https://your-target-university.edu/faculty-list/"
```

### Adjusting Rate Limiting

When initializing the scraper (line 258):

```python
scraper = TeacherProfileScraper(url, timeout=30, delay=1.0)
```

- `timeout`: Maximum seconds to wait for each page (default: 30)
- `delay`: Seconds to wait between requests (default: 0.5)

Increase `delay` if you're getting blocked or want to be more polite to the server.

## Troubleshooting

### Network Errors
If you get connection errors:
1. Check your internet connection
2. Verify the URL is accessible in a browser
3. Some networks may block web scraping - try from a different network

### No Teachers Found
If no teachers are matched:
1. Run demo mode to verify the tool works
2. Check your criteria aren't too restrictive
3. The website structure may be different than expected - you may need to customize the parsing logic

### Parsing Issues
The tool is designed for standard Chinese university websites. If the target site has a different structure:
1. Check the HTML source of the page
2. Modify the parsing logic in `parse_teacher_list()` and `parse_teacher_profile()`

## Example Workflows

### Finding Crop Genetics Professors

```python
criteria = {
    'required_titles': ['教授', '副教授'],
    'research_keywords': ['作物', '遗传', '育种', '基因']
}
```

### Finding Senior Researchers in Plant Protection

```python
criteria = {
    'required_titles': ['教授', '研究员'],
    'research_keywords': ['植物保护', '病理', '害虫']
}
```

### Finding PhD Holders in Any Field

```python
criteria = {
    'required_degree': '博士'
}
# Don't specify required_titles or research_keywords to match all PhDs
```

## Tips

1. **Start with demo mode** to understand the output format
2. **Be patient** - scraping many profiles takes time
3. **Adjust criteria** iteratively to refine results
4. **Respect the target server** - use appropriate delays
5. **Check output JSON** for detailed profile information

## Legal and Ethical Considerations

- Only scrape publicly accessible information
- Respect robots.txt and terms of service
- Use reasonable rate limiting to avoid overloading servers
- Don't use scraped data for spam or harassment
- Consider privacy implications of data collection

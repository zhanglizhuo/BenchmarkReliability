# ResearchBuddy

Find research advisors and collaborators by scraping and analyzing university teacher profiles.

## Features

- Scrape teacher profile listings from university websites
- Extract detailed information including:
  - Name, title, and department
  - Research areas and interests
  - Education background
  - Contact information (email, phone)
- Filter teachers based on customizable criteria:
  - Academic titles (教授, 副教授, etc.)
  - Research keywords and areas
  - Education requirements
- Export results to JSON format

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the script to scrape teacher profiles from the configured URL:

```bash
python research_buddy.py
```

The script will:
1. Fetch the teacher list page
2. Extract links to individual teacher profiles
3. Scrape each teacher's profile page
4. Filter teachers based on predefined criteria
5. Display matching teachers and save results to `teacher_profiles.json`

## Configuration

Edit the `criteria` dictionary in `research_buddy.py` to customize filtering:

```python
criteria = {
    'required_titles': ['教授', '副教授', 'Professor'],
    'research_keywords': ['作物', '育种', '遗传', '分子生物学'],
    'required_degree': '博士'
}
```

## Example

The tool is pre-configured to scrape from:
https://nxy.hunau.edu.cn/xygk/szdw_9365/

This URL lists teachers from the College of Agriculture at Hunan Agricultural University.

## Output

The script outputs:
- Console display of matching teachers with key information
- JSON file (`teacher_profiles.json`) with complete profile data

## Requirements

- Python 3.6+
- requests
- beautifulsoup4
- lxml

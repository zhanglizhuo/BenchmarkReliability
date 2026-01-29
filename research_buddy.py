#!/usr/bin/env python3
"""
ResearchBuddy - A tool to find research advisors/collaborators
Scrapes teacher profiles from university websites and filters based on criteria
"""

import requests
from bs4 import BeautifulSoup
import re
import json
import sys
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse


class TeacherProfileScraper:
    """Scraper for teacher profile pages"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_page(self, url: str) -> Optional[str]:
        """Fetch HTML content from a URL"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            response.encoding = response.apparent_encoding  # Handle Chinese encoding
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {e}", file=sys.stderr)
            return None
    
    def parse_teacher_list(self, html: str) -> List[Dict[str, str]]:
        """Parse the teacher list page to extract teacher information"""
        soup = BeautifulSoup(html, 'lxml')
        teachers = []
        
        # Look for links to teacher profile pages
        # Common patterns: links with names, profile pages, etc.
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            text = link.get_text(strip=True)
            
            # Skip empty links or navigation links
            if not text or len(text) < 2:
                continue
            
            # Build full URL
            full_url = urljoin(self.base_url, href)
            
            # Filter for likely teacher profile pages
            # Skip obvious non-profile links
            skip_keywords = ['首页', '返回', '更多', '下一页', '上一页', 'home', 'index', 'list']
            if any(keyword in text.lower() for keyword in skip_keywords):
                continue
            
            # Check if it looks like a profile link
            if 'info' in href or 'teacher' in href or '_' in href or text:
                teachers.append({
                    'name': text,
                    'url': full_url,
                    'link_href': href
                })
        
        return teachers
    
    def parse_teacher_profile(self, html: str, url: str) -> Dict[str, any]:
        """Parse individual teacher profile page"""
        soup = BeautifulSoup(html, 'lxml')
        profile = {
            'url': url,
            'name': '',
            'title': '',
            'department': '',
            'research_areas': [],
            'education': [],
            'contact': {},
            'raw_text': ''
        }
        
        # Extract page title
        title_tag = soup.find('title')
        if title_tag:
            profile['name'] = title_tag.get_text(strip=True).split('-')[0].strip()
        
        # Extract main content
        content_areas = soup.find_all(['div', 'article', 'section'], 
                                      class_=re.compile('content|main|article', re.I))
        
        if not content_areas:
            content_areas = [soup.find('body')]
        
        for content in content_areas:
            if not content:
                continue
                
            text = content.get_text(separator='\n', strip=True)
            profile['raw_text'] += text + '\n'
            
            # Extract specific information
            # Title/Position (职称, 职务)
            title_match = re.search(r'职称[：:]\s*([^\n]+)', text)
            if title_match:
                profile['title'] = title_match.group(1).strip()
            
            # Department (部门, 院系)
            dept_match = re.search(r'(?:部门|院系|单位)[：:]\s*([^\n]+)', text)
            if dept_match:
                profile['department'] = dept_match.group(1).strip()
            
            # Research areas (研究方向, 研究领域)
            research_match = re.search(r'(?:研究方向|研究领域|研究兴趣)[：:]\s*([^\n]+)', text)
            if research_match:
                research_text = research_match.group(1).strip()
                profile['research_areas'] = [r.strip() for r in re.split('[，,;；]', research_text)]
            
            # Education (学历, 教育背景)
            edu_pattern = re.compile(r'(?:学历|教育背景|学习经历)[：:]([^]+?)(?=\n\n|\n[一-龥]{2,}[：:]|$)', re.DOTALL)
            edu_match = edu_pattern.search(text)
            if edu_match:
                edu_text = edu_match.group(1).strip()
                profile['education'] = [e.strip() for e in edu_text.split('\n') if e.strip()]
            
            # Email
            email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', text)
            if email_match:
                profile['contact']['email'] = email_match.group(1)
            
            # Phone
            phone_match = re.search(r'(?:电话|手机|联系方式)[：:]\s*([0-9\-\s]+)', text)
            if phone_match:
                profile['contact']['phone'] = phone_match.group(1).strip()
        
        return profile
    
    def scrape_all_teachers(self, list_url: str) -> List[Dict[str, any]]:
        """Scrape all teacher profiles from a teacher list page"""
        print(f"Fetching teacher list from: {list_url}")
        html = self.fetch_page(list_url)
        
        if not html:
            print("Failed to fetch teacher list page")
            return []
        
        teachers_list = self.parse_teacher_list(html)
        print(f"Found {len(teachers_list)} potential teacher profile links")
        
        profiles = []
        for i, teacher_info in enumerate(teachers_list, 1):
            print(f"\n[{i}/{len(teachers_list)}] Fetching profile: {teacher_info['name']}")
            print(f"  URL: {teacher_info['url']}")
            
            profile_html = self.fetch_page(teacher_info['url'])
            if profile_html:
                profile = self.parse_teacher_profile(profile_html, teacher_info['url'])
                profile['name'] = teacher_info['name']  # Use name from list if not found in profile
                profiles.append(profile)
            else:
                print(f"  Failed to fetch profile")
        
        return profiles


class TeacherMatcher:
    """Filter and match teachers based on criteria"""
    
    def __init__(self, criteria: Dict[str, any] = None):
        self.criteria = criteria or {}
    
    def matches(self, profile: Dict[str, any]) -> bool:
        """Check if a teacher profile matches the criteria"""
        
        # Check title requirements
        if 'required_titles' in self.criteria:
            required_titles = self.criteria['required_titles']
            title = profile.get('title', '').lower()
            if not any(req.lower() in title for req in required_titles):
                return False
        
        # Check research area requirements
        if 'research_keywords' in self.criteria:
            keywords = self.criteria['research_keywords']
            research_text = ' '.join(profile.get('research_areas', [])).lower()
            raw_text = profile.get('raw_text', '').lower()
            
            if not any(keyword.lower() in research_text or keyword.lower() in raw_text 
                      for keyword in keywords):
                return False
        
        # Check education requirements
        if 'required_degree' in self.criteria:
            required_degree = self.criteria['required_degree']
            education = ' '.join(profile.get('education', [])).lower()
            if required_degree.lower() not in education:
                return False
        
        return True
    
    def filter_teachers(self, profiles: List[Dict[str, any]]) -> List[Dict[str, any]]:
        """Filter teachers based on criteria"""
        return [p for p in profiles if self.matches(p)]


def main():
    """Main function"""
    # URL from the problem statement
    url = "https://nxy.hunau.edu.cn/xygk/szdw_9365/"
    
    print("=" * 80)
    print("ResearchBuddy - Teacher Profile Scraper")
    print("=" * 80)
    print()
    
    # Initialize scraper
    scraper = TeacherProfileScraper(url)
    
    # Scrape all teacher profiles
    profiles = scraper.scrape_all_teachers(url)
    
    print(f"\n{'=' * 80}")
    print(f"Successfully scraped {len(profiles)} teacher profiles")
    print(f"{'=' * 80}\n")
    
    # Example filtering criteria - customize based on requirements
    criteria = {
        'required_titles': ['教授', '副教授', 'Professor', 'Associate Professor'],
        'research_keywords': ['作物', '育种', '遗传', '分子生物学', '基因', '植物', '农学']
    }
    
    # Filter teachers
    matcher = TeacherMatcher(criteria)
    matched_profiles = matcher.filter_teachers(profiles)
    
    print(f"Teachers matching criteria: {len(matched_profiles)}")
    print(f"{'=' * 80}\n")
    
    # Display results
    for i, profile in enumerate(matched_profiles, 1):
        print(f"\n{i}. {profile.get('name', 'Unknown')}")
        print(f"   Title: {profile.get('title', 'N/A')}")
        print(f"   Department: {profile.get('department', 'N/A')}")
        if profile.get('research_areas'):
            print(f"   Research Areas: {', '.join(profile['research_areas'])}")
        if profile.get('contact'):
            if 'email' in profile['contact']:
                print(f"   Email: {profile['contact']['email']}")
            if 'phone' in profile['contact']:
                print(f"   Phone: {profile['contact']['phone']}")
        print(f"   URL: {profile['url']}")
        print(f"   {'-' * 76}")
    
    # Save results to JSON file
    output_file = 'teacher_profiles.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'total_profiles': len(profiles),
            'matched_profiles': len(matched_profiles),
            'criteria': criteria,
            'profiles': matched_profiles
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n\nResults saved to: {output_file}")
    print(f"All profiles ({len(profiles)} total) are available in the script output.")


if __name__ == '__main__':
    main()

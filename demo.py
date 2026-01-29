#!/usr/bin/env python3
"""
ResearchBuddy Demo - Demonstrates functionality with sample data
"""

import json
import sys
from typing import Optional
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from research_buddy import TeacherProfileScraper, TeacherMatcher
from sample_data import SAMPLE_LIST_HTML, SAMPLE_PROFILES


class DemoScraper(TeacherProfileScraper):
    """Demo scraper that uses sample data instead of real HTTP requests"""
    
    def __init__(self):
        # Initialize parent class with demo URL
        super().__init__("https://nxy.hunau.edu.cn/xygk/szdw_9365/", timeout=30, delay=0)
        self.sample_profiles = SAMPLE_PROFILES
    
    def fetch_page(self, url: str) -> Optional[str]:
        """Fetch HTML from sample data"""
        if url == self.base_url:
            return SAMPLE_LIST_HTML
        
        # Extract the path from the URL
        for path, html in self.sample_profiles.items():
            if path in url or url.endswith(path):
                return html
        
        print(f"  Warning: No sample data for {url}", file=sys.stderr)
        return None


def main():
    """Main demo function"""
    print("=" * 80)
    print("ResearchBuddy - DEMO MODE (Using Sample Data)")
    print("=" * 80)
    print()
    print("This demo shows how ResearchBuddy works using sample teacher profiles.")
    print("In production, it would scrape: https://nxy.hunau.edu.cn/xygk/szdw_9365/")
    print()
    
    # Initialize demo scraper
    scraper = DemoScraper()
    
    # Scrape all teacher profiles
    profiles = scraper.scrape_all_teachers(scraper.base_url)
    
    print(f"\n{'=' * 80}")
    print(f"Successfully scraped {len(profiles)} teacher profiles")
    print(f"{'=' * 80}\n")
    
    # Display all profiles first
    print("ALL TEACHER PROFILES:")
    print("=" * 80)
    for i, profile in enumerate(profiles, 1):
        print(f"\n{i}. {profile.get('name', 'Unknown')}")
        print(f"   Title: {profile.get('title', 'N/A')}")
        print(f"   Department: {profile.get('department', 'N/A')}")
        if profile.get('research_areas'):
            print(f"   Research Areas: {', '.join(profile['research_areas'])}")
        if profile.get('education'):
            print(f"   Education: {profile['education'][0]}")
        if profile.get('contact'):
            if 'email' in profile['contact']:
                print(f"   Email: {profile['contact']['email']}")
        print(f"   {'-' * 76}")
    
    # Example filtering criteria
    print("\n\n" + "=" * 80)
    print("FILTERING WITH CRITERIA")
    print("=" * 80)
    
    criteria = {
        'required_titles': ['教授', '副教授', 'Professor', 'Associate Professor'],
        'research_keywords': ['作物', '育种', '遗传', '分子生物学', '基因', '植物']
    }
    
    print(f"\nCriteria:")
    print(f"  - Required titles: {', '.join(criteria['required_titles'])}")
    print(f"  - Research keywords: {', '.join(criteria['research_keywords'])}")
    print()
    
    # Filter teachers
    matcher = TeacherMatcher(criteria)
    matched_profiles = matcher.filter_teachers(profiles)
    
    print(f"Teachers matching criteria: {len(matched_profiles)} out of {len(profiles)}")
    print(f"{'=' * 80}\n")
    
    # Display filtered results
    if matched_profiles:
        print("MATCHING TEACHERS:")
        for i, profile in enumerate(matched_profiles, 1):
            print(f"\n{i}. {profile.get('name', 'Unknown')} ✓")
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
    else:
        print("No teachers matched the criteria.")
    
    # Save results to JSON file
    output_file = 'demo_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'mode': 'demo',
            'total_profiles': len(profiles),
            'matched_profiles': len(matched_profiles),
            'criteria': criteria,
            'all_profiles': profiles,
            'matched': matched_profiles
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n\nDemo results saved to: {output_file}")
    print("\nTo use with real data, ensure you have network access and run:")
    print("  python research_buddy.py")


if __name__ == '__main__':
    main()

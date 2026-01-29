#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Research Collaborator Finder
从大学网站查找适合的科研合作人选
"""

import requests
from bs4 import BeautifulSoup
import re
import sys


class CollaboratorFinder:
    """查找科研合作人选的类"""
    
    def __init__(self, url):
        self.url = url
        self.faculty_list = []
        
    def fetch_page(self):
        """获取网页内容"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(self.url, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            if response.status_code == 200:
                return response.text
            else:
                print(f"错误: 无法访问网页，状态码: {response.status_code}")
                return None
        except Exception as e:
            print(f"错误: 获取网页失败 - {str(e)}")
            return None
    
    def parse_faculty_info(self, html_content):
        """解析教师信息"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 查找所有包含教师信息的元素
        # 这需要根据实际网页结构调整
        faculty_items = soup.find_all(['div', 'li', 'tr'], class_=re.compile(r'teacher|faculty|staff|person', re.I))
        
        # 如果找不到特定class，尝试查找包含特定关键词的内容
        if not faculty_items:
            faculty_items = soup.find_all(['div', 'li', 'article'])
        
        for item in faculty_items:
            text = item.get_text(separator=' ', strip=True)
            
            # 提取教师信息
            faculty_info = self.extract_info(text, item)
            if faculty_info and faculty_info.get('name'):
                self.faculty_list.append(faculty_info)
        
        return self.faculty_list
    
    def extract_info(self, text, element):
        """从文本中提取教师信息"""
        info = {
            'name': '',
            'title': '',
            'education': '',
            'research': '',
            'has_papers': False,
            'raw_text': text
        }
        
        # 提取姓名（通常在开头，2-4个中文字符）
        name_match = re.search(r'^[\u4e00-\u9fa5]{2,4}', text)
        if name_match:
            info['name'] = name_match.group()
        
        # 提取职称（注意顺序，长的先匹配）
        titles = ['副教授', '教授', '副研究员', '研究员', '助理研究员', '讲师', '助教']
        for title in titles:
            if title in text:
                info['title'] = title
                break
        
        # 提取学历
        if '博士' in text:
            info['education'] = '博士'
        elif '硕士' in text:
            info['education'] = '硕士'
        elif '学士' in text:
            info['education'] = '学士'
        
        # 检查是否有科研论文
        research_keywords = ['论文', '期刊', 'SCI', 'EI', 'CSSCI', '发表', '研究方向', '科研']
        for keyword in research_keywords:
            if keyword in text:
                info['has_papers'] = True
                break
        
        # 查找链接
        link = element.find('a')
        if link and link.get('href'):
            info['link'] = link.get('href')
        
        return info
    
    def filter_candidates(self, prefer_lecturer=True):
        """筛选合适的候选人"""
        # 优先条件：讲师 + 博士 + 有科研论文
        priority_candidates = []
        # 备选条件：副教授
        fallback_candidates = []
        
        for faculty in self.faculty_list:
            # 优先级1: 讲师 + 博士 + 有研究
            if (faculty['title'] == '讲师' and 
                faculty['education'] == '博士' and 
                faculty['has_papers']):
                priority_candidates.append(faculty)
            # 优先级2: 讲师 + 博士（即使没有明确论文信息）
            elif faculty['title'] == '讲师' and faculty['education'] == '博士':
                priority_candidates.append(faculty)
            # 备选: 副教授
            elif faculty['title'] == '副教授':
                fallback_candidates.append(faculty)
        
        return priority_candidates, fallback_candidates
    
    def display_results(self, candidates, title):
        """显示结果"""
        if not candidates:
            print(f"\n{title}: 未找到符合条件的候选人")
            return
        
        print(f"\n{title}:")
        print("=" * 80)
        for i, candidate in enumerate(candidates, 1):
            print(f"\n{i}. 姓名: {candidate['name']}")
            print(f"   职称: {candidate['title']}")
            print(f"   学历: {candidate['education']}")
            print(f"   有科研成果: {'是' if candidate['has_papers'] else '信息不明确'}")
            if candidate.get('link'):
                print(f"   链接: {candidate['link']}")
            # 显示部分原始文本以供参考
            if len(candidate['raw_text']) > 100:
                print(f"   简介: {candidate['raw_text'][:100]}...")
            else:
                print(f"   简介: {candidate['raw_text']}")
    
    def run(self):
        """运行完整流程"""
        print(f"正在访问: {self.url}")
        print("-" * 80)
        
        html_content = self.fetch_page()
        if not html_content:
            return
        
        print("正在解析教师信息...")
        self.parse_faculty_info(html_content)
        print(f"共找到 {len(self.faculty_list)} 位教师信息")
        
        print("\n正在筛选合适的合作候选人...")
        priority_candidates, fallback_candidates = self.filter_candidates()
        
        # 显示优先候选人
        self.display_results(priority_candidates, "优先推荐 (讲师 + 博士 + 科研论文)")
        
        # 如果没有优先候选人，显示备选
        if not priority_candidates:
            print("\n未找到讲师+博士的候选人，显示副教授作为备选:")
            self.display_results(fallback_candidates, "备选推荐 (副教授)")
        else:
            print(f"\n另有 {len(fallback_candidates)} 位副教授可作为备选")


def main():
    """主函数"""
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        # 默认URL
        url = "https://nxy.hunau.edu.cn/xygk/szdw_9365/"
    
    print("=" * 80)
    print("科研合作人选查找工具")
    print("Research Collaborator Finder")
    print("=" * 80)
    
    finder = CollaboratorFinder(url)
    finder.run()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本 - 使用模拟数据演示功能
Test script with mock data
"""

from find_collaborator import CollaboratorFinder


def create_mock_html():
    """创建模拟的HTML内容"""
    return """
    <html>
    <body>
        <div class="teacher-list">
            <div class="teacher-item">
                <h3>张伟</h3>
                <p>讲师，博士，研究方向：人工智能与机器学习。发表SCI论文10余篇，主持国家自然科学基金项目1项。</p>
            </div>
            <div class="teacher-item">
                <h3>李明</h3>
                <p>讲师，博士，主要从事计算机视觉研究，在国际会议和期刊上发表多篇学术论文。</p>
            </div>
            <div class="teacher-item">
                <h3>王芳</h3>
                <p>副教授，硕士，研究方向：数据挖掘，发表CSSCI论文多篇。</p>
            </div>
            <div class="teacher-item">
                <h3>刘强</h3>
                <p>讲师，硕士，教学经验丰富。</p>
            </div>
            <div class="teacher-item">
                <h3>陈红</h3>
                <p>副教授，博士，研究方向：自然语言处理，主持多项科研项目，发表高水平论文20余篇。</p>
            </div>
            <div class="teacher-item">
                <h3>赵军</h3>
                <p>教授，博士，博士生导师，在机器学习领域有深入研究。</p>
            </div>
            <div class="teacher-item">
                <h3>孙丽</h3>
                <p>讲师，博士，毕业于清华大学，研究兴趣包括深度学习和计算机视觉，已发表EI论文多篇。</p>
            </div>
        </div>
    </body>
    </html>
    """


def test_collaborator_finder():
    """测试功能"""
    print("=" * 80)
    print("测试模式 - 使用模拟数据")
    print("Test Mode - Using Mock Data")
    print("=" * 80)
    
    # 创建finder实例
    finder = CollaboratorFinder("mock://test")
    
    # 使用模拟HTML
    mock_html = create_mock_html()
    print("\n正在解析教师信息...")
    finder.parse_faculty_info(mock_html)
    print(f"共找到 {len(finder.faculty_list)} 位教师信息")
    
    # 显示所有解析的信息
    print("\n所有解析的教师信息:")
    print("-" * 80)
    for faculty in finder.faculty_list:
        print(f"姓名: {faculty['name']}, 职称: {faculty['title']}, "
              f"学历: {faculty['education']}, 有科研: {faculty['has_papers']}")
    
    # 筛选候选人
    print("\n正在筛选合适的合作候选人...")
    priority_candidates, fallback_candidates = finder.filter_candidates()
    
    # 显示结果
    finder.display_results(priority_candidates, "优先推荐 (讲师 + 博士 + 科研论文)")
    
    if not priority_candidates:
        finder.display_results(fallback_candidates, "备选推荐 (副教授)")
    else:
        print(f"\n另有 {len(fallback_candidates)} 位副教授可作为备选")
        if fallback_candidates:
            print("\n副教授名单:")
            for candidate in fallback_candidates:
                print(f"  - {candidate['name']} ({candidate['education']})")


if __name__ == "__main__":
    test_collaborator_finder()

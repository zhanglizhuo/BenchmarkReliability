#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本 - 测试备选方案（副教授）
Test script for fallback scenario (Associate Professors)
"""

from find_collaborator import CollaboratorFinder


def create_fallback_mock_html():
    """创建只有副教授的模拟HTML内容"""
    return """
    <html>
    <body>
        <div class="teacher-list">
            <div class="teacher-item">
                <h3>张教授</h3>
                <p>教授，博士，博士生导师，在机器学习领域有深入研究，发表SCI论文50余篇。</p>
            </div>
            <div class="teacher-item">
                <h3>李副教授</h3>
                <p>副教授，博士，研究方向：数据挖掘与大数据分析，主持多项国家级科研项目。</p>
            </div>
            <div class="teacher-item">
                <h3>王讲师</h3>
                <p>讲师，硕士，主要负责本科教学工作。</p>
            </div>
            <div class="teacher-item">
                <h3>刘副教授</h3>
                <p>副教授，博士，从事人工智能研究，在顶级会议发表论文多篇。</p>
            </div>
        </div>
    </body>
    </html>
    """


def test_fallback_scenario():
    """测试备选方案（当没有符合条件的讲师时）"""
    print("=" * 80)
    print("测试备选方案 - 没有符合条件的讲师+博士时")
    print("Test Fallback Scenario - No qualified lecturers with PhD")
    print("=" * 80)
    
    finder = CollaboratorFinder("mock://fallback")
    
    mock_html = create_fallback_mock_html()
    print("\n正在解析教师信息...")
    finder.parse_faculty_info(mock_html)
    print(f"共找到 {len(finder.faculty_list)} 位教师信息")
    
    print("\n所有解析的教师信息:")
    print("-" * 80)
    for faculty in finder.faculty_list:
        print(f"姓名: {faculty['name']}, 职称: {faculty['title']}, "
              f"学历: {faculty['education']}, 有科研: {faculty['has_papers']}")
    
    print("\n正在筛选合适的合作候选人...")
    priority_candidates, fallback_candidates = finder.filter_candidates()
    
    finder.display_results(priority_candidates, "优先推荐 (讲师 + 博士 + 科研论文)")
    
    if not priority_candidates:
        print("\n>>> 未找到讲师+博士的候选人，显示副教授作为备选:")
        finder.display_results(fallback_candidates, "备选推荐 (副教授)")


if __name__ == "__main__":
    test_fallback_scenario()

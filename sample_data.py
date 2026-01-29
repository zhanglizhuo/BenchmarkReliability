"""
Sample HTML data for testing ResearchBuddy
"""

# Sample teacher list page HTML
SAMPLE_LIST_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>农学院师资队伍</title>
</head>
<body>
    <div class="content">
        <h1>农学院师资队伍</h1>
        <div class="teacher-list">
            <ul>
                <li><a href="/info/1001.html">张教授</a></li>
                <li><a href="/info/1002.html">李副教授</a></li>
                <li><a href="/info/1003.html">王研究员</a></li>
                <li><a href="/info/1004.html">刘讲师</a></li>
                <li><a href="/info/1005.html">陈教授</a></li>
            </ul>
        </div>
    </div>
</body>
</html>
"""

# Sample teacher profile pages
SAMPLE_PROFILES = {
    "/info/1001.html": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>张教授-个人主页</title>
</head>
<body>
    <div class="profile">
        <h1>张教授</h1>
        <div class="info">
            <p>职称：教授</p>
            <p>部门：作物遗传育种系</p>
            <p>研究方向：水稻分子育种，作物遗传改良，功能基因组学</p>
            <p>教育背景：</p>
            <ul>
                <li>2005-2008 中国农业大学 作物遗传育种 博士</li>
                <li>2002-2005 华中农业大学 作物遗传育种 硕士</li>
                <li>1998-2002 湖南农业大学 农学 学士</li>
            </ul>
            <p>联系方式：</p>
            <p>电话：0731-12345678</p>
            <p>邮箱：zhangprof@hunau.edu.cn</p>
        </div>
    </div>
</body>
</html>
""",
    "/info/1002.html": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>李副教授-个人主页</title>
</head>
<body>
    <div class="profile">
        <h1>李副教授</h1>
        <div class="info">
            <p>职称：副教授</p>
            <p>部门：植物保护系</p>
            <p>研究方向：植物病理学，病害防治，生物农药</p>
            <p>教育背景：</p>
            <ul>
                <li>2010-2014 南京农业大学 植物病理学 博士</li>
                <li>2008-2010 湖南农业大学 植物保护 硕士</li>
            </ul>
            <p>邮箱：liassoc@hunau.edu.cn</p>
        </div>
    </div>
</body>
</html>
""",
    "/info/1003.html": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>王研究员-个人主页</title>
</head>
<body>
    <div class="profile">
        <h1>王研究员</h1>
        <div class="info">
            <p>职称：研究员</p>
            <p>部门：农业资源与环境系</p>
            <p>研究方向：土壤肥料，养分管理，可持续农业</p>
            <p>教育背景：</p>
            <ul>
                <li>2008-2012 中国农业科学院 土壤学 博士</li>
            </ul>
            <p>邮箱：wangres@hunau.edu.cn</p>
        </div>
    </div>
</body>
</html>
""",
    "/info/1004.html": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>刘讲师-个人主页</title>
</head>
<body>
    <div class="profile">
        <h1>刘讲师</h1>
        <div class="info">
            <p>职称：讲师</p>
            <p>部门：园艺系</p>
            <p>研究方向：蔬菜栽培，设施农业</p>
            <p>教育背景：</p>
            <ul>
                <li>2015-2018 湖南农业大学 园艺学 硕士</li>
            </ul>
            <p>邮箱：liulect@hunau.edu.cn</p>
        </div>
    </div>
</body>
</html>
""",
    "/info/1005.html": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>陈教授-个人主页</title>
</head>
<body>
    <div class="profile">
        <h1>陈教授</h1>
        <div class="info">
            <p>职称：教授</p>
            <p>部门：作物遗传育种系</p>
            <p>研究方向：玉米遗传育种，基因编辑，分子标记辅助育种</p>
            <p>教育背景：</p>
            <ul>
                <li>2000-2004 浙江大学 作物遗传育种 博士</li>
                <li>1997-2000 湖南农业大学 作物遗传育种 硕士</li>
            </ul>
            <p>电话：0731-87654321</p>
            <p>邮箱：chenprof@hunau.edu.cn</p>
        </div>
    </div>
</body>
</html>
"""
}

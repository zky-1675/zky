豆瓣电影 Top 30 数据爬取与可视化项目项目说明本项目旨在通过自动化手段爬取豆瓣电影 Top 30 的相关信息，并以可视化的方式展示这些电影的评分。
通过 Selenium 模拟浏览器操作，爬取电影标题、评分、短评和链接等数据，并利用 HTML/CSS 创建一个简单的可视化网页，直观展示电影评分信息。
环境配置依赖库:
在运行本项目之前，
请确保已安装以下 Python 依赖库：• Selenium• Pandas• Matplotlib可以通过以下命令安装所需的依赖库：bashpip install selenium pandas matplotlib
浏览器驱动本项目使用 Selenium 模拟浏览器操作，需要安装对应的浏览器驱动程序。根据代码中的设置，项目使用的是 Edge 浏览器驱动（  webdriver.Edge()  ）。
请根据您的浏览器版本下载并安装对应的 Edge WebDriver：• 下载地址：Microsoft Edge WebDriver下载完成后，将   msedgedriver.exe   
放置在系统的 PATH 中，或者在代码中指定其路径。其他环境• Python 版本：建议使用 Python 3.8 及以上版本。• 浏览器：Microsoft Edge（Chromium 版本）
运行方式1. 准备工作1. 安装所需的 Python 依赖库（如上所述）。2. 下载并安装对应的 Edge WebDriver，并确保其路径正确。3. 确保您的网络可以正常访问 豆瓣电影 Top 250 页面。
2. 运行代码将以下代码保存为   douban_top30.py   文件，并在终端或命令行中运行：python
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

# 初始化 WebDriver
driver = webdriver.Edge()
url = "https://movie.douban.com/top250"
driver.get(url)
result_list = []

# 爬取前30部电影
for i in range(2):  # 前30部电影分布在前两页
    element_hds = driver.find_elements(By.CLASS_NAME, "hd")

    for element_hd in element_hds[:15]:  # 每页取前15部电影
        data_dict = {
            "title": "",
            "short": "",
            "rating_num": "",
            "url": ""  # 新增字段，用于存储电影的豆瓣链接
        }

        # 获取电影链接
        element_a = element_hd.find_element(By.TAG_NAME, "a")
        href = element_a.get_attribute("href")
        data_dict["url"] = href  # 保存电影链接

        # 打开电影链接
        driver.execute_script("window.open('')")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(href)
        # 等待电影标题加载
        title = driver.find_element(By.TAG_NAME, "h1").text
        data_dict["title"] = title

        # 获取电影评分
        try:
            rating_num = driver.find_element(By.CLASS_NAME, "rating_num").text
            data_dict["rating_num"] = rating_num
        except Exception as e:
            print(f"Error retrieving rating number: {e}")
            data_dict["rating_num"] = "Not found"

        # 获取电影短评
        try:
            short = driver.find_element(By.CLASS_NAME, "short").text
            data_dict["short"] = short
        except Exception as e:
            print(f"Error retrieving short description: {e}")
            data_dict["short"] = "No short description available."

        result_list.append(data_dict)

        # 返回到主页面
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    # 点击下一页
    try:
        next_element = driver.find_element(By.CLASS_NAME, "next")
        next_two = next_element.find_element(By.TAG_NAME, "a")
        next_two.click()
    except Exception as e:
        print("No more pages or error occurred:", e)
        break

# 关闭浏览器
driver.quit()

# 将数据保存为 DataFrame
df = pd.DataFrame(result_list)

# 提取电影标题、评分和链接
titles = df['title']
ratings = df['rating_num'].astype(float)
urls = df['url']

# 创建 HTML 内容
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>豆瓣电影 Top 30 评分</title>
    <style>
        .chart {
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
        }
        .chart-bar {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
        .chart-bar .title {
            margin-right: 10px;
            font-size: 14px;
        }
        .chart-bar .rating {
            width: 100px;
            height: 20px;
            background-color: skyblue;
            text-align: center;
            line-height: 20px;
            font-size: 12px;
            color: white;
        }
    </style>
</head>
<body>
    <div class="chart">
        <h1>豆瓣电影 Top 30 评分</h1>
"""

# 添加条形图数据到 HTML
for title, rating, url in zip(titles, ratings, urls):
    html_content += f"""
        <div class="chart-bar">
            <a href="{url}" target="_blank" class="title">{title}</a>
            <div class="rating" style="width: {rating * 10}px;">{rating}</div>
        </div>
    """

html_content += """
    </div>
</body>
</html>
"""

# 保存 HTML 文件
with open("douban_top30.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("HTML 文件已生成：douban_top30.html")
3. 查看结果运行代码后，程序会生成一个名为   douban_top30.html   的文件。您可以通过浏览器打开该文件，查看豆瓣电影 Top 30 的评分可视化结果。注意事项1. 豆瓣网站可能有反爬虫机制，请合理使用爬虫，避免频繁访问导致 IP 被封。2. 如果在运行过程中遇到问题，请检查网络连接、浏览器驱动版本以及代码中的 URL 是否正确。3. 本项目仅供学习和研究使用，请遵守相关法律法规和网站的使用条款。项目结构豆瓣电影 Top 30 爬虫项目/
│
├── douban_top30.py          # 主程序代码
├── douban_top30.html        # 生成的可视化网页文件
└── README.md                # 项目说明文档

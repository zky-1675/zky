import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from IPython.display import IFrame

# 设置中文字体
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用于显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用于显示负号

# 初始化WebDriver
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

# 将数据保存为DataFrame
df = pd.DataFrame(result_list)

# 提取电影标题、评分和链接
titles = df['title']
ratings = df['rating_num'].astype(float)
urls = df['url']

# 创建HTML内容
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>豆瓣电影Top30评分</title>
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
        <h1>豆瓣电影Top30评分</h1>
"""

# 添加条形图数据到HTML
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

# 保存HTML文件
with open("douban_top30.html", "w", encoding="utf-8") as file:
    file.write(html_content)

# 显示HTML文件
IFrame("douban_top30.html", width="100%", height="600")

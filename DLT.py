import time
import bs4
import sqlite3
import os
import easygui
from selenium import webdriver

print(time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime(time.time())), "正在加载页面请稍后...")
# 浏览器选项：忽略证书错误；不下载图片；无界面
opts = webdriver.ChromeOptions()
opts.add_argument("--ignore-certificate-errors")
opts.add_argument('blink-settings=imagesEnabled=false')
opts.add_argument("--headless")
# 500彩票网
url = "http://datachart.500.com/dlt/history/history.shtml"  # history url
browser = webdriver.Chrome(options=opts)
browser.get(url)

print(time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime(time.time())), "正在查询结果请稍后...")
# 查询第一期到最后一期的所有数据
browser.find_element_by_xpath("//input[@id='start']").clear()
browser.find_element_by_xpath("//input[@id='start']").send_keys("1")
browser.find_element_by_xpath("//div[@class='tubiao_box_t']/table/tbody/tr/td[2]/img").click()

# 使用BeautifulSoup解析
soup = bs4.BeautifulSoup(browser.page_source, features="html.parser")
dlts = soup.select("#tdata > tr")
browser.quit()

# 生成器表达式，每期结果组成一个元组，所有元祖组成一个列表
dat = ((dlt.contents[1].contents[0],
        dlt.contents[2].contents[0],
        dlt.contents[3].contents[0],
        dlt.contents[4].contents[0],
        dlt.contents[5].contents[0],
        dlt.contents[6].contents[0],
        dlt.contents[7].contents[0],
        dlt.contents[8].contents[0],
        dlt.contents[9].contents[0].replace(",", ""),
        dlt.contents[10].contents[0],
        dlt.contents[11].contents[0].replace(",", ""),
        dlt.contents[12].contents[0],
        dlt.contents[13].contents[0].replace(",", ""),
        dlt.contents[14].contents[0].replace(",", ""),
        dlt.contents[15].contents[0].replace("-", "")
        ) for dlt in dlts)

# 选择数据库文件
file = easygui.filesavebox(msg="请指定数据文件保存位置",
                           title=None,
                           default=os.path.join(os.getcwd(), "lottry_history.db"),
                           filetypes=[["*.db", "*.db3", "*.sqlite", "*.sqlite3", "SQLite database file"],
                                      ["*.*", "All files"]]
                           ) or os.path.join(os.getcwd(), "lottry_history.db")
print(time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime(time.time())), "正在保存数据...")

# 新建数据库表dlt_history，并写入数据
with sqlite3.connect(file) as con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS 'dlt_history'")
    cur.execute('CREATE TABLE "dlt_history" ('
                '"qi" TEXT NOT NULL,'           # 期号
                '"q1" integer NOT NULL,'        # 前区—1
                '"q2" integer NOT NULL,'        # 前区-2
                '"q3" integer NOT NULL,'        # 前区-3
                '"q4" integer NOT NULL,'        # 前区-4
                '"q5" integer NOT NULL,'        # 前区-5
                '"h1" integer NOT NULL,'        # 后区-1
                '"h2" integer NOT NULL,'        # 后区-2
                '"all_bonus" text NOT NULL,'    # 总奖池
                '"fst_num" integer NOT NULL,'   # 一等奖注数
                '"fst_bonus" text NOT NULL,'    # 一等奖奖金
                '"snd_num" integer NOT NULL,'   # 二等奖注数
                '"snd_bonus" text NOT NULL,'    # 二等奖奖金
                '"total_bet" text NOT NULL,'    # 总投注金额
                '"date" text NOT NULL,'         # 开奖日期
                'PRIMARY KEY ("qi"))'
                )
    cur.executemany('REPLACE INTO dlt_history VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', dat)
    con.commit()

print(time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime(time.time())), "已完成，数据保存在：", file)

# lottry_history
通过Python脚本提取福彩双色球和体彩大乐透的全部历史数据，保存在名为lottry_history的SQLite数据库文件中。数据库中的ssq_history和dlt_history两张表对应相应数据。
## 注意
运行脚本需要安装Chrome浏览器，并且下载相应的Chrome Driver。Chrom Driver下载地址：[Chromedriver](http://npm.taobao.org/mirrors/chromedriver/)。  
请将ChromDriver放在脚本所在目录或者其他可以通过环境变量查找的目录。否则请修改代码，直接写明对应路径。
## 运行
每次运行会重建所有数据，请注意。双色球和大乐透单独脚本，可以使用同一个数据库文件，不会影响已经存在的表。
## 查看SQLite数据库文件
[DB Browser for SQLite](https://sqlitebrowser.org/)  
此外也可以自行选择其他工具，如Navicat。
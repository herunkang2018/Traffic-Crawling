
import sys
from selenium import webdriver
# from tbselenium.tbdriver import TorBrowserDriver
import time
import random
from lxml import etree
import urllib.request
import traceback

##通过搜狗top热搜榜单收集热搜词
def getKeywords():
    url = "http://top.sogou.com/"
    webPage=urllib.request.urlopen(url)
    html = webPage.read().decode('utf-8')
    # print("html:" + html)
    html = etree.HTML(html)
    script = html.xpath("//a[@href]/text()")
    print(script)
    print(type(script))
    # global keywords
    # keywords.append(script)
    return script


## 通过filetype高级搜索相关关键词的文件 默认没有filetype 也即查看普通网页
##  对于百度：
#       ppt doc pdf没有问题 但zip rar gz格式被百度禁止了
##  对于谷歌：
#       全格式支持 需要注意的是 对于tar系列格式 比如tar.gz 只使用gz作为filetype即可 使用tar.gz反而不行

def getFile(driver, keyword, engine, filetype=0):
    start1 = time.time()
    if engine == "baidu":
        se_url = "http://baidu.com"
        if filetype != 0:
            keyword = "filetype:" + filetype + " " + keyword
        try:
            ##debug
            driver.get(se_url)
            driver.find_element_by_id("kw").send_keys(keyword)
            driver.find_element_by_id("su").click()
            # time.sleep(2)
            rand_num = random.randrange(1, 11) # 1 - 10
            print("randnum is: " + str(rand_num))
            sreach_window=driver.current_window_handle
            print(driver.current_window_handle)
            print("//div[@id='content_left']//div[@id='" +  str(rand_num) + "']/h3/a")
            time.sleep(2) ##依据网速调整

            ##模拟随机点击搜索结果
            driver.find_element_by_xpath("//div[@id='content_left']//div[@id='" +  str(rand_num) + "']/h3/a").click()

            driver.back()

        except Exception as e:
            print("[ERROR] +++some error in getFile Function\n\n\n")
            print(e)
            traceback.print_exc()

    elif engine == "google":
        se_url = "https://www.google.com.hk"
        #lst-ib id
        #btnK name
        if filetype != 0:
            keyword = "filetype:" + filetype + " " + keyword
        try:
            driver.get(se_url)
            driver.find_element_by_id("lst-ib").send_keys(keyword)
            driver.find_element_by_name("btnK").click()

            time.sleep(2)

            ##随机点击结果
            rand_num = random.randrange(1, 11) # 1 - 10
            driver.find_element_by_xpath("//div[@class='srg']/div[" +  str(rand_num) + "]//h3/a").click()
            driver.back()

            time.sleep(2)
        except Exception as e:
            print("[ERROR] +++some error in getFile Function\n\n\n")
            print(e)
            traceback.print_exc()


    else:
        print("[ERROR] 请选择正确的搜索引擎")
        return

if __name__ == "__main__":

    if len(sys.argv) == 1:
        engine = "baidu"
        filetype = 0
    elif len(sys.argv) == 2:
        engine = sys.argv[1]
        filetype = 0
    elif len(sys.argv) == 3:
        engine = sys.argv[1]
        filetype = sys.argv[2]
    else:
        print("[ERROR] 命令行参数错误")
        sys.exit()


    ##获取通用文件:
    #   参数格式: webdriver keyword 搜索引擎名称 文件类型
    # 通过filetype高级搜索相关关键词的文件 默认没有filetype 也即查看普通网页
    ##  对于百度：
    #       ppt doc pdf等没有问题 但zip rar gz格式被百度禁止了
    ##  对于谷歌：
    #       全格式支持 需要注意的是 对于tar系列格式 比如tar.gz 只使用gz作为filetype即可 使用tar.gz反而不行

    loop_times = 10
    for i in range(loop_times):
        driver = webdriver.Chrome(executable_path=r"D:\chromeDriver\chromedriver.exe")
        keywords = getKeywords()
        print(keywords)
        print(len(keywords))
        ##热搜词大约150个
        for keyword in keywords:
            getFile(driver, keyword, engine, filetype)

        ##允许下载5秒
        time.sleep(5)
        driver.quit()
        rand_time = random.randrange(3, 6)
        ##浏览器随机一段时间重新打开
        time.sleep(rand_time)
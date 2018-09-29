# coding=utf-8
import time

'''
 多行注释写法
 打开百度并进行搜索
'''


class test:
    def run(self, http, database):
        browser = http.get_browser()

        http.get('https://baidu.com')
        http.get_dom('//*[@id="kw"]').send_keys('selenium python')
        http.get_dom('//*[@id="su"]').click()
        time.sleep(0)
        http.get_dom('//*[@id="2"]/h3/a').click()
        time.sleep(0)

        browser.switch_to_window(browser.window_handles[-1])
        browser.close()

        browser.switch_to_window(browser.window_handles[-1])
        http.get_dom('//*[@id="kw"]').clear()
        http.get_dom('//*[@id="kw"]').send_keys('others')
        time.sleep(0)
        print(browser.title)
        database.execute(
            "insert into logTable (logMessage) values ('测试添加执行成功')")

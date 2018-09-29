# -*-coding:utf-8 -*-
from lib import DataBaseHelper, HttpHelper


class AutoTest:
    # 注入测试脚本
    def __init__(self, options, browser_type, path):
        self.database = DataBaseHelper.DataBaseHelper()
        self.http = HttpHelper.HttpHelper(options, browser_type, path)

    # 运行测试脚本
    def run(self, test_script):
        try:
            if hasattr(test_script, 'run'):
                if test_script.run.__code__.co_argcount == 2:
                    test_script.run(self.http)
                else:
                    test_script.run(self.http, self.database)
            else:
                raise Exception('没有找到启动方法"run"')
        except Exception as e:
            print(e)

    # 结束测试
    def close(self):
        self.http.quit()
        self.database.close()

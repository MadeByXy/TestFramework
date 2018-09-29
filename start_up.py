# -*-coding:utf-8 -*-
import importlib
import io
import json
import os
import sys
import threading

from lib import AutoTest


def load_python(dir_path, deep_search):
    # 读取python脚本文件方法
    py_scripts = []
    if not os.path.isabs(dir_path):
        dir_path = os.path.abspath(dir_path)
    for dir in os.listdir(dir_path):
        dir = dir_path + '/' + dir
        if os.path.isfile(dir):
            # 如果是python文件, 加入到列表中
            if dir.endswith('.py'):
                py_scripts.append(os.path.normcase(dir))
        elif deep_search:
            # 如果是文件夹并且开启深层遍历, 递归
            py_scripts.extend(load_python(dir, deep_search))
    return py_scripts


def import_source(module_name, module_file_path):
    # 动态加载模块
    module_spec = importlib.util.spec_from_file_location(
        module_name, module_file_path
    )
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)

    # 默认读取test类
    return module.test()


def begin_test(name, options, script_path, browser_type, path):
    # 开始测试
    environment = AutoTest.AutoTest(options, browser_type, path)
    try:
        python = import_source(name, script_path)
        environment.run(python)
    except Exception as e:
        print(e)
    finally:
        environment.close()
        print('{name}测试完成'.format(name=name))


with open("config.json", 'r', encoding='UTF-8') as config:
    # 读取配置文件
    json = json.load(config)
    print('开始执行脚本')
    thread_list = []
    for item_config in json['test_script_dir']:
        py_scripts = load_python(
            item_config['path'], item_config['deep_search'])
        for script_path in py_scripts:
            name = os.path.basename(script_path).split('.')[0]
            for index in range(item_config['run_times']):
                for browser_type in json['browser_type']:
                    if json['browser_type'][browser_type]:
                        thread = threading.Thread(target=begin_test, args=(
                            name, json['options'], script_path, browser_type, json['path']))
                        thread.start()
                        thread_list.append(thread)
    for thread in thread_list:
        thread.join()
    print('全部执行完成')

# -*- coding: UTF-8 -*-
import os

from jproperties import Properties

configs = Properties()
default_setting = {
    "sqlalchemy_db_string": "sqlite:///tmp/kupy_sqlite.db",
    "log_level": "INFO",
    "data_folder": "/tmp/",
}
# 设置默认值
for (key, value) in default_setting.items():
    configs.setdefault(key, value)

# 获取谁调用了你的信息. 因为改成了直接把配置文件放在项目根，免去了查询谁调用了你的信息
# pid=os.getpid()
# print(psutil.Process(pid).cmdline())
# print(os.getcwd())
# print(psutil.Process(pid).)


config_path = "resources/app-config.properties"
if os.path.exists(config_path):
    with open(config_path, "rb") as config_file:
        configs.load(config_file)
        if configs.get("data_folder") is not None:
            cache_folder = configs["data_folder"].data + "cache/"
            if not os.path.exists(cache_folder):
                os.makedirs(name=cache_folder, mode=0o777, exist_ok=True)

        if configs.get("log_output_path") is not None:
            log_file_path = configs["log_output_path"].data
            log_filename = os.path.basename(log_file_path)
            log_folder = log_file_path.replace(log_filename, "")
            if not os.path.exists(log_folder):
                os.makedirs(name=log_folder, mode=0o777, exist_ok=True)

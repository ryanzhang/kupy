# -*- coding: UTF-8 -*-
import os

from jproperties import Properties

configs = Properties()
default_setting = {
    "postgres_host": "",
    "postgres_port": "5432",
    "postgres_user": "",
    "postgres_password": "",
    "postgres_database": "",
    "log_level": "INFO",
    "log_output_path": "",
    "data_folder": "/tmp/",
}
# 设置默认值
for (key, value) in default_setting.items():
    configs.setdefault(key, value)

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
                os.makedirs(cache_folder, 755)

if not configs["log_output_path"]:
    log_file_path = configs["log_output_path"].data
    log_filename = os.path.basename(log_file_path)
    log_folder = log_file_path.replace(log_filename, "")
    if not os.path.exists(log_folder):
        os.makedirs(log_folder, 755)

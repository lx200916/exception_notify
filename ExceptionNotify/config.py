import tomli
import os

Config: dict = {"Enabled": True}


def load_config(path="~/.exception_notify.toml"):
    path = os.path.expanduser(path)
    if os.path.exists(path):
        with open(path, "rb") as f:
            Config.update(tomli.load(f))
            if not validate_config():
                Config["Enabled"] = False
                print("Config file is invalid.ExceptionNotify will not function.")
    else:
        if not validate_config():
            Config["Enabled"] = False
            print("Config file not found.ExceptionNotify will not function.")


def validate_config():
    # print(Config)
    if "feishu" not in Config or "webhook" not in Config["feishu"]:
        print("Feishu Webhook not found.ExceptionNotify will not function.")
        return False
    return True

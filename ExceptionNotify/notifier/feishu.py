import requests
from ..config import Config

class Feishu:
    def notify(self,message:str, meta: dict = None):
        if not Config["Enabled"]:
            return
        if "feishu" not in Config or "webhook" not in Config["feishu"]:
            return
        conf: dict = Config["feishu"]
        pre_str = conf.get("pre_str", "")
        at_list = conf.get("at", [])
        for at in at_list:
            pre_str += f'<at user_id="{at}"></at>'
        if pre_str != "":
            pre_str += "\n"
        requests.post(
            Config["feishu"]["webhook"],
            json={"msg_type": "text", "content": {"text": pre_str + message}},
        )
        # If failed, Do nothing.


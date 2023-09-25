import requests
from ..config import Config


class Telegram:
    def __HTML_escape(self, s):
        s = s.replace("&", "&amp;")
        s = s.replace("<", "&lt;")
        s = s.replace(">", "&gt;")
        s = s.replace(" ", "&nbsp;")
        s = s.replace("\n", "<br/>")
        return s

    def notify(self, message: str, meta: dict = None):
        if not Config["Enabled"]:
            return
        if "telegram" not in Config or "bot_token" not in Config["telegram"]:
            return
        conf: dict = Config["telegram"]
        chat_id = conf.get("chat_id", -1)
        at_list = conf.get("at", [])
        message = self.__HTML_escape(message)
        for at in at_list:
            message += f'<a href="tg://user?id={at}"> \u200b</a>'
        if chat_id == -1:
            return
        requests.post(
            f"https://api.telegram.org/bot{conf['bot_token']}/sendMessage",
            json={"chat_id": chat_id, "text": message, "parse_mode": "HTML"},
        )

from .feishu import Feishu
from .telegram import Telegram

notifiers = [Feishu(), Telegram()]


def notify(message):
    for notifier in notifiers:
        notifier.notify(message=message)

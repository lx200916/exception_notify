from .feishu import Feishu

notifiers = []
notifiers.append(Feishu)


def notify(message):
    for notifier in notifiers:
        notifier.notify(message)

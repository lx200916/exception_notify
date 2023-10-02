import datetime
import re
import signal
import subprocess
import sys
import time
import traceback
import atexit

from . import notifier
from .config import Config as __Config, load_config as __load_config

# I don't think two Instance of ExceptionNotify may appear in one process.So global variable is ok.
infos = {}
_hook = sys.excepthook
_exception=False
__w_re = re.compile(r"^(\S+)\s+(\S+)\s+(\S+)")
def __is_notebook() -> bool:
    try:
        import IPython

        shell = IPython.get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":
            return True  # Jupyter notebook or qtconsole
        elif shell == "TerminalInteractiveShell":
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except Exception as e:
        return False  # Probably standard Python interpreter


def update_info(info: dict = None):
    global infos
    if info is not None:
        infos.update(info)
        # print(f"ExceptionNotify: Updated info: {infos}")


def __except_hook(exc_type, value, tb):
    global _exception
    _exception=True
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, value, tb)
        return
    start_time = datetime.datetime.now()
    message = f"❎ {start_time.strftime('%Y-%m-%d %H:%M:%S')}ExceptionNotify: {exc_type.__name__}: {value}\n"
    for line in traceback.extract_tb(tb, limit=10):
        message += f'File "{line.filename}", line {line.lineno}, in {line.name}\n'
        message += f"    {line.line}\n"
    message += f"🕐 Time: {datetime.datetime.now()}"
    if len(infos) > 0:
        message += "\n🍣 Infos:" + ", ".join(
            [f"{key}: {val}" for key, val in infos.items()]
        )
    notifier.notify(message)
    while 1:
        if not tb.tb_next:
            break
        tb = tb.tb_next
    stack = []
    f = tb.tb_frame
    while f:
        stack.append(f)
        f = f.f_back
    stack.reverse()
    message += "\n\nLocalvars:"
    for frame in stack:
        # if len(message) > 120:
        #     break
        if (
            # frame.f_code.co_name == "<module>"
            # or
            frame.f_code.co_name == "__exceptionhook__"
        ):
            continue
        message += "\nFrame %s in `%s` at `line %s`" % (
            frame.f_code.co_name,
            frame.f_code.co_filename,
            frame.f_lineno,
        )
        for key, val in frame.f_locals.items():
            if key.startswith("__") or str(val).startswith("<module") or str(val).startswith("<function") or str(val).startswith("<class"):
                continue
            message += "\n\t%20s = " % key
            try:
                val = str(val)
                if len(val) > 20:
                    val = val[:20] + "..."
                message += val
            except:
                message += "<ERROR WHILE PRINTING VALUE>"
    time.sleep(0.1)
    notifier.notify(message)
    _hook(exc_type, value, tb)



def install(
    conf=None,
    config_path="~/.exception_notify.toml",
    register_done_handler=False,
    register_kill_handler=False,
):
    if __is_notebook():
        print("ExceptionNotify is not supported in Jupyter Notebook.")
    if conf is not None:
        __Config.update(conf)
    __load_config(config_path)
    if __Config["Enabled"]:
        _hook = sys.excepthook
        # sys.excepthook
        sys.excepthook = __except_hook
        if register_done_handler:
            atexit.register(__exit_hook)
        if register_kill_handler:
            import signal

            signal.signal(signal.SIGTERM, __kill_handler)
            # signal.signal(signal.SIGINT, __kill_handler)
        print("ExceptionNotify installed.")

def __kill_handler(signum, frame):
    global _exception
    _exception=True
    if signum == signal.SIGTERM:
        print("SIGTERM received.")
        message = f"🛑 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ExceptionNotify: SIGTERM received.\n"
        message += f"⌨️ Command: {' '.join(sys.argv)}"
        output = subprocess.getoutput("w|grep -v `whoami`")
        # Parse output and extract USER TTY FROM
        if len(output) > 0:
            lines = output.split("\n")
            message += "\n👥 Users:"
            for line in lines:
                if line.startswith("USER") or "load average" in line:
                    continue
                m = __w_re.match(line)
                if m:
                    message += f"\n{m.group(1)} {m.group(2)} {m.group(3)}"
        if len(infos) > 0:
            message += "\n🍣 Infos:"
            for key, val in infos.items():
                message += f"{key}: {val},"
        notifier.notify(message)
        sys.exit(-1)



def __exit_hook():
    if not _exception:
        __successfully_done()

def Done():
    __successfully_done()


def __successfully_done():
    args = sys.argv
    message = f"✅ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ExceptionNotify: {args[0]} Done."
    message += f"\n⌨️ Command: {' '.join(args)}"
    if len(infos) > 0:
        message += "\n🍣 Infos:"
        for key, val in infos.items():
            message += f"{key}: {val},"
    notifier.notify(message)

def notify(message):
    notifier.notify(message)

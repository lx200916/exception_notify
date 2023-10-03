import atexit
import datetime
import os
import re
import signal
import subprocess
import sys
import time
import traceback

from . import notifier
from .config import Config as __Config, load_config as __load_config

# I don't think two Instance of ExceptionNotify may appear in one process.So global variable is ok.
infos = {}
_hook = sys.excepthook
_exception = False
__w_re = re.compile(r"^(\S+)\s+(\S+)\s+(\S+)")
__re_raise = False

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


def __filter_locals(key,val,max_len=50)->tuple[bool,str]:
    if key.startswith("__") or __to_str(val).startswith("<module") or __to_str(val).startswith("<function") or __to_str(val).startswith("<class"):
        return False,""
    return True, f"{__to_str(key)}: {__to_str(val)[:max_len]}"


def __to_str(obj):
    try:
        if type(obj).__module__ == "builtins":
            if type(obj) == list:
                if len(obj) > 5:
                    return f"<list len:{len(obj)}>"
                else:
                    return "<list " + ", ".join([__to_str(i) for i in obj]) + ">"
            if type(obj) == dict:
                if len(obj) > 5:
                    return f"<dict len:{len(obj)}>"
                else:
                    return "<dict " + ", \n".join(
                        [f"{__to_str(key)}: {__to_str(val)}" for key, val in obj.items()]
                    ) + ">"
            return str(obj)
        if type(obj).__module__ == "numpy":
            try:
                import numpy
                if isinstance(obj, numpy.ndarray):
                    if obj.ndim >5 or obj.size >= 20:
                        return f"<ndarray {obj.shape} {obj.dtype}>"
                    else:
                        return str(obj)
                else:
                    if len(obj) > 30:
                        return f"<{type(obj).__name__} len:{len(obj)}>"
                    else:
                        return str(obj)
            except:
                print(type(obj))
                return "<ERROR WHILE PRINTING Numpy VALUE>"
        return str(obj)
    except:
        print(type(obj))

        return "<ERROR WHILE PRINTING VALUE>"


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

    def suicide():
        print("ExceptionNotify: Suicide in 3 seconds.")
        time.sleep(3)
        _hook(exc_type, value, tb)
        time.sleep(3)
        # print("ExceptionNotify: Suicide.")
        os.kill(os.getpid(), signal.SIGINT)
        os.kill(os.getpid(), signal.SIGINT)
        os.kill(os.getpid(), signal.SIGINT)
        os.kill(os.getpid(), signal.SIGINT)
        time.sleep(3)
        os.kill(os.getpid(), signal.SIGTERM)
    import threading
    threading.Thread(target=suicide,daemon=True).start()
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
        if (
            frame.f_code.co_name == "__exceptionhook__"
        ):
            continue
        message += "\nFrame %s in `%s` at `line %s`" % (
            frame.f_code.co_name,
            frame.f_code.co_filename,
            frame.f_lineno,
        )
        for key, val in frame.f_locals.items():
            should_add , val = __filter_locals(key,val)
            if should_add:
                message += f"\n\t{val}"
    time.sleep(0.1)
    notifier.notify(message)
    if __re_raise:
        raise exc_type(value).with_traceback(tb)
    else:
        _hook(exc_type, value, tb)


def install(
    conf=None,
    config_path="~/.exception_notify.toml",
    register_done_handler=False,
    register_kill_handler=False,
        re_raise=False
):
    global _hook
    global __re_raise
    __re_raise=re_raise
    if __is_notebook():
        print("ExceptionNotify is not supported in Jupyter Notebook.")
    if conf is not None:
        __Config.update(conf)
    __load_config(config_path)
    if __Config["Enabled"]:
        _hook = sys.excepthook
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
    if _exception:
        return
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

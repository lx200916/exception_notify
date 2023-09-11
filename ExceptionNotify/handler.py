import datetime
import sys
import time
import traceback

from . import notifier
from .config import Config, load_config

def is_notebook() -> bool:
    try:
        from IPython import get_ipython
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter

def excepthook(exc_type, value, tb):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, value, tb)
        return
    start_time = datetime.datetime.now()
    message = f"❎ {start_time.strftime('%Y-%m-%d %H:%M:%S')}ExceptionNotify: {exc_type.__name__}: {value}\n"
    for line in traceback.extract_tb(tb,limit=10):
        message+=f"File \"{line.filename}\", line {line.lineno}, in {line.name}\n"
        message+=f"    {line.line}\n"
    message+=f"🕐 Time: {datetime.datetime.now()}"
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
        if len(message) > 512:
            break
        if frame.f_code.co_name == "<module>" or frame.f_code.co_name == "__exceptionhook__":
            continue
        message += "\nFrame %s in `%s` at `line %s`" % (
            frame.f_code.co_name,
            frame.f_code.co_filename,
            frame.f_lineno,
        )
        for key, val in frame.f_locals.items():
            message += "\n\t%20s = " % key
            try:
                message += str(val)
            except:
                message += "<ERROR WHILE PRINTING VALUE>"
    time.sleep(0.1)
    notifier.notify(message)



def install(conf=None, config_path="~/.exception_notify.toml", ):
    if is_notebook():
        print("ExceptionNotify is not supported in Jupyter Notebook.")
    if conf is not None:
        Config.update(conf)
    load_config(config_path)
    if Config["Enabled"]:
        # sys.excepthook
        sys.excepthook = excepthook
        print("ExceptionNotify installed.")
def Done():
    sucessfully_done()
def sucessfully_done():
    args = sys.argv
    message = f"✅ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ExceptionNotify: {args[0]} Done."
    message+= f"\n⌨️ Command: {' '.join(args)}"
    notifier.notify(message)
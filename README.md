<div align="center">

# ExceptionNotify

Notify You Timely when Python Script crash.

</div>

## Installation
```
# Clone & Install
pip install git+https://github.com/lx200916/exception_notify
# or
git clone https://github.com/lx200916/exception_notify &&cd exception_notify
pip install -e .
```
## Supported Methods
* Feishu(Lark)
## Usage
1. Provide Config.
   * Store Config in `~/.exception_notify.toml`.
   * Pass the config dict in `install` function.
     Config Example:
   ```toml
   [feishu]
   webhook = "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
   pre_str = "Notify ⚠️"
   at = ["MY_FEISHU_OPEN_ID"]
   ```
2. Import the Lib in the Script then `install()`.
3. (Optional) Setup Done Notify.
   ```python
   import ExceptionNotify
   ExceptionNotify.install(conf={"feishu":{"webhook":"xxx"}})
   do_awsome_things()
   ExceptionNotify.Done()
   
   ```

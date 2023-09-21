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
    Two ways:
   * Store Config in `~/.exception_notify.toml`.
     
> Config Example:
> ```toml
>   [feishu]
>   webhook = "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
>   # pre_str = "Notify ⚠️" # Optional
>   # at = ["MY_FEISHU_OPEN_ID"] # Optional
>   ```
   
   * Or Pass the config dict in `install` function.
   
  
2. Import the Lib in the Script then `install()`.
3. (Optional) Setup Done Notify.

### Quick Start
Code Example: 
```python
   import ExceptionNotify

   ExceptionNotify.install()
   do_awsome_things()
   # Notify When Done
   ExceptionNotify.Done()
   ```

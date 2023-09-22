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
3. (Optional) Add Additional Info to the Notification Message Body.
    * Call `ExceptionNotify.add_info({"key":"value"})` to add additional info.(for example: `Model Best Acc.`, `HyperParameter`).
4. (Optional) Setup Done Notify.
 * Call `Done()` Manually when the script is done.
 * Pass `register_done_handler=True` in `install()` function, then you will get notified when the script is done.
5. (Optional) Manually Send Any Text Message. Call `ExceptionNotify.send_message("Message")` to send message.
### Quick Start
Code Example: 
```python
import ExceptionNotify
ExceptionNotify.install(register_done_handler=True)
do_awsome_things()
ExceptionNotify.update_info({"Best Acc.":0.99})   
# Get Notified when the script is done.
 ```

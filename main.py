# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import ExceptionNotify
ExceptionNotify.install(config_path="./test.toml")


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.
    print(462//0)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ExceptionNotify.update_info({"Arg1": "V1"})
    print_hi('PyCharm')
    ExceptionNotify.Done()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

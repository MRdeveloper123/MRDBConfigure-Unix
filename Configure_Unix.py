"""
由于使用了TUI界面，只能用于Unix(未测试)及类Unix系统
提供给用户修改配置文件的工具
"""
import os
import sys
from MR.Kernel import Loading, Error
from prompt_toolkit.shortcuts import radiolist_dialog, message_dialog, input_dialog, yes_no_dialog

# 声明变量
is_saved = True  # 是否保存
# ------------------------------------

# region TUI界面只适用于Unix(未测试)及类Unix系统
if sys.platform == "win32":
    print("Configure_Unix tool only supports Unix or Unix-like OS")
    sys.exit(0)
# endregion

# region 如果配置文件存在则读取，不存在则创建配置文件
if not os.path.exists("mrdb.conf"):
    # 配置文件不存在
    message_dialog(
        title="Warning",
        text="Configuration file not found.\n"
             "We are going to create a new one using default values.").run()
    Loading.init_config()
# endregion

# region 读取配置文件
try:
    # 尝试读取配置文件
    config = Loading.read_config()
except Error.ConfigFileBroken:
    # 读取出错，配置文件遭到破坏
    message_dialog(
        title="Warning",
        text="Configuration file is broken. Please delete it anyway.").run()
    sys.exit(0)
# endregion


# 哈哈，鸟枪换炮，改用TUI界面了，向完全的命令行界面说Goodbye
while True:
    option = radiolist_dialog(
        title="Thanks for choosing MRDB. This is MRDB configuration tool.",
        text="Choose one to re-configure",
        values=[
            ("Address", "Address  -->  %s" % config["Address"]),
            ("Port", "Port  -->  %s" % config["Port"]),
            ("RunningMode", "RunningMode  -->  %s" % config["RunningMode"])
        ],
        ok_text="Choose it",
        cancel_text="Exit"
    ).run()

    if not option:
        # option的值为None，则说明选择的是要退出
        if not is_saved:
            # 先看看是否已经保存，如果未保存，询问用户是否要先保存
            leave_without_saving = yes_no_dialog(
                title="Warning",
                text="Leave without saving ?",
                yes_text="Do not save",
                no_text="Save changes").run()
            if leave_without_saving:
                # 离开不保存
                pass
            else:
                # 离开要保存，执行保存操作
                Loading.save_config(config)
                message_dialog(
                    title="Thanks for using MRDB configuration tool.",
                    text="The changes have been saved to the configuration file.").run()
        sys.exit(0)

    elif option == "Address":
        # 修改绑定的地址
        new_address = input_dialog(
                    title="Configure binding address",
                    text="Please type the address you want").run()
        if not new_address or new_address.strip() == "":
            # new_address的值为None或者strip后为空，则说明未修改，则不做任何操作
            pass
        else:
            config["Address"] = new_address
            is_saved = False

    elif option == "Port":
        # 修改绑定的端口
        new_port = input_dialog(
                    title="Configure binding port",
                    text="Please type the port you want").run()
        try:
            new_port = int(new_port)
        except ValueError:
            # 输入的不是整数
            message_dialog(
                title="Warning",
                text="An int is required.").run()
        except TypeError:
            # 抛出TypeError，则传入的是None，未做任何操作
            pass
        else:
            # 未抛出异常，先判断数字范围
            if not 1 <= new_port <= 65535:
                message_dialog(
                    title="Warning",
                    text="Port must between 1 and 65535( 1 <= port <= 65535 )").run()
            else:
                config["Port"] = new_port
                is_saved = False

    elif option == "RunningMode":
        # 修改绑定的运行模式
        # 修改的配置项为RunningMode(运行模式)，则对其进行校验
        # MRDB一共有三种运行模式
        # 塑料记忆模式，单文件模式，多文件模式
        # 塑料记忆模式则是每次都是reZero，不会保存任何曾经存储过的任何数据
        # 单文件模式则是将所有数据库都存储在一个文件中
        # 多文件模式则是将每个数据库分别存储，在database文件夹中
        new_running_mode = radiolist_dialog(
                    title="Select",
                    text="Which RunningMode do you want ?",
                    values=[
                        ("PlasticMemories", "PlasticMemories"),
                        ("SingleFile", "SingleFile"),
                        ("MultiFile", "MultiFile")
                        ]).run()
        if not new_running_mode:
            # 值为None，说明未做任何改动
            pass
        elif new_running_mode == "PlasticMemories":
            config["RunningMode"] = "PlasticMemories"
            is_saved = False
        elif new_running_mode == "SingleFile":
            config["RunningMode"] = "SingleFile"
            is_saved = False
        elif new_running_mode == "MultiFile":
            config["RunningMode"] = "MultiFile"
            is_saved = False


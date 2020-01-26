"""
定义了MRDB所有的异常
"""


class IllegalCommand(Exception):
    """
    非法命令，一般为命令不存在或者有语法错误
    """
    def __init__(self):
        super().__init__()
        self.error = ""


class IllegalCommandArgument(Exception):
    """
    命令参数错误
    """
    def __init__(self):
        super().__init__()
        self.error = ""


class DatabaseAlreadyExists(Exception):
    """
    数据库已经存在了
    """
    def __init__(self):
        super().__init__()
        self.error = ""


class DatabasesNotFound(Exception):
    """
    数据库不存在
    """
    def __init__(self):
        super().__init__()
        self.error = ""


class KeyNotFound(Exception):
    """
    键未找到
    """
    def __init__(self):
        super().__init__()
        self.error = ""


class ServerStopped(Exception):
    """
    服务器已停止
    """
    def __init__(self):
        super().__init__()
        self.error = ""


class ConfigFileBroken(Exception):
    """
    配置文件损坏
    """
    def __init__(self):
        super().__init__()
        self.error = ""


class DatabaseFileBroken(Exception):
    """
    数据库文件损坏
    """
    def __init__(self):
        super().__init__()
        self.error = ""

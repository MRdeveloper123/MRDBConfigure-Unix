"""
加载/读取配置文件/数据库
"""
import hashlib
import umsgpack
from MR.Kernel import Error


def generate_sha512(raw_data: bytes):
    """
    生成SHA512，但是要进行6次运算
    """
    hasher = hashlib.sha512()
    for i in range(6):
        hasher.update(raw_data)
    return hasher.hexdigest()


def init_config():
    """
    初始化配置文件，具体步骤：
        ①定义初始配置dict
        ②计算序列化后的dict(bytes类型)的SHA512
        ③将计算得到的SHA512和初始配置dict合为list( [sha512, dict] )，序列化后写入文件
    """
    # 定义初始配置
    # 默认为仅限本机访问，端口9600，运行模式为PlasticMemories(塑料记忆，可塑性记忆:-)
    original_config = {
        "Address": "localhost",
        "Port": 9600,
        "RunningMode": "PlasticMemories"  # :-)
    }
    # 计算序列化后的配置dict的SHA512
    original_sha512 = generate_sha512(umsgpack.packb(original_config))
    with open("mrdb.conf", "wb") as config:
        # 将计算得到的SHA512和初始配置dict合为list( [sha512, dict] )，序列化后写入文件
        config.write(umsgpack.packb([original_sha512, original_config]))


def read_config():
    """
    读取配置文件，记得先判断配置文件是否存在，不存在的话先调用init_config()。具体步骤：
        ①读取配置文件中的所有内容
        ②将内容反序列化，设置异常捕获
        ③反序列化后应该得到一个list，为计算得到的SHA512和配置dict( [sha512, dict] )
        ④计算配置dict的SHA512与读取的SHA512进行对比校验
            不符合则抛出异常，符合则返回配置内容
    """
    with open("mrdb.conf", "rb") as config:
        data = config.read()
    try:
        config = umsgpack.unpackb(data)
    except umsgpack.ExtraData:
        # 反序列化出错，表示文件一定遭过损毁，抛出异常
        raise Error.ConfigFileBroken
    except ValueError:
        # 反序列化出错，表示文件一定遭过损毁，抛出异常
        raise Error.ConfigFileBroken
    except UnicodeDecodeError:
        # 反序列化出错，表示文件一定遭过损毁，抛出异常
        raise Error.ConfigFileBroken
    # 读取保存的SHA512和配置内容
    config_sha512 = config[0]
    config_config = config[1]
    # 计算配置内容的SHA512和保存的SHA512是否一致，不一致则抛出异常，一致则返回配置内容
    if not generate_sha512(umsgpack.packb(config_config)) == config_sha512:
        raise Error.ConfigFileBroken
    else:
        return config_config


def save_config(config_dict: dict):
    """
    保存配置文件，具体步骤：
        ①计算序列化后的配置dict(bytes类型)的SHA512
        ②将计算得到的SHA512和配置dict合为list( [sha512, dict] )，序列化后写入文件
    """
    # 计算序列化后的配置dict的SHA512
    sha512 = generate_sha512(umsgpack.packb(config_dict))
    with open("mrdb.conf", "wb") as config:
        # 将计算得到的SHA512和配置dict合为list( [sha512, dict] )，序列化后写入文件
        config.write(umsgpack.packb([sha512, config_dict]))


def read_db_single():
    """
    单文件模式下读取数据库，具体步骤：
    ①读取数据库文件中的所有内容
    ②将内容反序列化，设置异常捕获
    ③反序列化后应该得到一个list，为计算得到的SHA512和数据库dict( [sha512, dict] )
    ④计算数据库dict的SHA512与读取的SHA512进行对比校验
        不符合则抛出异常，符合则返回数据库dict
    """
    with open("database.mrdb", "rb") as db:
        data = db.read()
    try:
        data = umsgpack.unpackb(data)
    except umsgpack.ExtraData:
        raise Error.DatabaseFileBroken
    else:
        data_sha512 = data[0]
        data_db = data[1]
        if not generate_sha512(umsgpack.packb(data_db)) == data_sha512:
            raise Error.DatabaseFileBroken
        else:
            return data_db


def save_db_single(db_dict: dict):
    """
    单文件模式下保存数据库，具体步骤：
        ①计算序列化后的数据库dict(bytes类型)的SHA512
        ②将计算得到的SHA512和数据库dict合为list( [sha512, dict] )，序列化后写入文件
    """
    # 计算序列化后的数据库dict(bytes类型)的SHA512
    sha512 = generate_sha512(umsgpack.packb(db_dict))
    with open("database.mrdb", "wb") as db:
        # 将计算得到的SHA512和数据库dict合为list( [sha512, dict] )，序列化后写入文件
        db.write(umsgpack.packb([sha512, db_dict]))


def read_db_multi():
    """
    多文件模式下读取数据库
    """
    # TODO
    pass


def save_db_multi(db_dict: dict):
    """
    多文件模式下保存数据库
    """
    # TODO
    pass

import configparser  #导入configparser库，读取配置文件
import os

#路径获取方法
# print(os.path.join(os.getcwd(),'conf.ini'))
# print(os.path.abspath(__file__))
# print(os.path.dirname(os.path.abspath(__file__)))

class Config():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'conf.ini')    #获取制定配置文件所在路径
        self.config.read(self.conf_path, encoding='utf-8-sig')     #读取配置文件，编码格式为utf-8-sig

        self.conf = {
            'host': '', 'user': '', 'password': '', 'db_test_buyer': '', 'email': '', 'upassword': '', 'user_url': '', 'success': '', 'TrackNoIsExist ': '', 'TrackNoInvalid ': ''
                        }
    def get_conf(self):
        """
        配置文件读取，并赋值给全局参数
        :return:
        """
        self.conf['host'] = self.config.get("test_db", 'host')
        self.conf['user'] = self.config.get("test_db", "user")
        self.conf['password'] = self.config.get("test_db", "password")
        self.conf['db_test_buyer'] = self.config.get("test_db", "db_test_buyer")

        return self.conf

if __name__ == '__main__':
    a=Config()
    print(a.get_conf())



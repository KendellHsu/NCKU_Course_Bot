"""
环境配置模块
用于管理OpenAI API密钥和其他敏感信息
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class EnvConfig:
    """环境配置类"""
    
    @staticmethod
    def get_openai_api_key():
        """获取OpenAI API密钥"""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("请在环境变量中设置 OPENAI_API_KEY")
        return api_key
    
    @staticmethod
    def get_ncku_credentials():
        """获取成功大学登录凭据"""
        username = os.getenv('NCKU_USERNAME')
        password = os.getenv('NCKU_PASSWORD')
        
        if not username or not password:
            raise ValueError("请在环境变量中设置 NCKU_USERNAME 和 NCKU_PASSWORD")
        
        return username, password
    
    @staticmethod
    def is_auto_captcha_enabled():
        """检查是否启用自动验证码识别"""
        return os.getenv('AUTO_CAPTCHA', 'true').lower() == 'true'

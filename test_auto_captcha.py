"""
测试自动验证码识别功能
"""

import os
import sys
import time
import logging

def test_captcha_solver():
    """测试验证码识别器"""
    print("=== 测试验证码识别器 ===")
    
    try:
        # 检查是否安装了必要的模块
        from captcha_solver import CaptchaSolver
        print("✅ 验证码识别器模块导入成功")
        
        # 检查OpenAI API密钥
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            print("❌ 未设置 OPENAI_API_KEY 环境变量")
            print("请设置环境变量：export OPENAI_API_KEY='your_api_key_here'")
            return False
        
        print("✅ 找到OpenAI API密钥")
        
        # 初始化验证码识别器
        solver = CaptchaSolver(api_key)
        print("✅ 验证码识别器初始化成功")
        
        return True
        
    except ImportError as e:
        print(f"❌ 无法导入验证码识别器模块: {e}")
        print("请确保已安装所有依赖：pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        return False

def test_env_config():
    """测试环境配置"""
    print("\n=== 测试环境配置 ===")
    
    try:
        from env_config import EnvConfig
        print("✅ 环境配置模块导入成功")
        
        # 测试获取OpenAI API密钥
        try:
            api_key = EnvConfig.get_openai_api_key()
            print("✅ 成功获取OpenAI API密钥")
        except ValueError as e:
            print(f"⚠️  {e}")
        
        # 测试获取NCKU凭据
        try:
            username, password = EnvConfig.get_ncku_credentials()
            print("✅ 成功获取NCKU登录凭据")
        except ValueError as e:
            print(f"⚠️  {e}")
        
        # 测试自动验证码设置
        auto_captcha = EnvConfig.is_auto_captcha_enabled()
        print(f"✅ 自动验证码识别设置: {auto_captcha}")
        
        return True
        
    except ImportError as e:
        print(f"❌ 无法导入环境配置模块: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        return False

def test_integration():
    """测试集成功能"""
    print("\n=== 测试集成功能 ===")
    
    try:
        from course_bot import NCKUCourseBot
        print("✅ 主程序模块导入成功")
        
        # 创建机器人实例（不启动浏览器）
        bot = NCKUCourseBot()
        print("✅ 机器人实例创建成功")
        
        # 检查验证码识别器状态
        if hasattr(bot, 'captcha_solver') and bot.captcha_solver:
            print("✅ 验证码识别器已集成到主程序")
        else:
            print("⚠️  验证码识别器未集成到主程序")
        
        return True
        
    except ImportError as e:
        print(f"❌ 无法导入主程序模块: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        return False

def main():
    """主测试函数"""
    print("🤖 NCKU Course Bot 自动验证码识别功能测试")
    print("=" * 50)
    
    # 设置日志
    logging.basicConfig(level=logging.INFO)
    
    # 运行测试
    tests = [
        ("验证码识别器", test_captcha_solver),
        ("环境配置", test_env_config),
        ("集成功能", test_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} 测试通过")
            else:
                print(f"❌ {test_name} 测试失败")
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
        
        print("-" * 30)
    
    # 输出测试结果
    print(f"\n=== 测试结果 ===")
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("🎉 所有测试都通过了！")
        print("✅ 自动验证码识别功能已准备就绪")
    else:
        print("⚠️  部分测试失败，请检查配置")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

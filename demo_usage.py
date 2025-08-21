"""
NCKU Course Bot 使用演示
展示如何使用自动验证码识别功能
"""

import os
import sys
from course_bot import NCKUCourseBot

def demo_basic_usage():
    """演示基本使用方法"""
    print("=== NCKU Course Bot 基本使用演示 ===")
    
    try:
        # 创建机器人实例
        print("1. 创建机器人实例...")
        bot = NCKUCourseBot()
        print("✅ 机器人实例创建成功")
        
        # 检查验证码识别器状态
        if hasattr(bot, 'captcha_solver') and bot.captcha_solver:
            print("✅ 自动验证码识别功能已启用")
            print(f"   使用模型: {bot.captcha_solver.model}")
        else:
            print("⚠️  自动验证码识别功能未启用")
            print("   请设置 OPENAI_API_KEY 环境变量")
        
        print("\n2. 机器人配置信息:")
        print(f"   选课系统URL: {bot.config.get('course_selection_url', '未设置')}")
        print(f"   课程数量: {len(bot.config.get('courses', []))}")
        print(f"   自动验证码: {bot.config.get('verification', {}).get('auto_captcha', False)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 演示过程中发生错误: {e}")
        return False

def demo_with_api_key():
    """演示配置API密钥后的使用"""
    print("\n=== 配置API密钥后的使用演示 ===")
    
    # 检查是否有API密钥
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("⚠️  未设置 OPENAI_API_KEY 环境变量")
        print("请按以下步骤设置：")
        print("1. 获取OpenAI API密钥: https://platform.openai.com/api-keys")
        print("2. 设置环境变量: export OPENAI_API_KEY='your_key_here'")
        print("3. 重新运行此脚本")
        return False
    
    print("✅ 找到OpenAI API密钥")
    
    try:
        # 创建机器人实例
        bot = NCKUCourseBot()
        
        if bot.captcha_solver:
            print("✅ 自动验证码识别器已初始化")
            print(f"   模型: {bot.captcha_solver.model}")
            print(f"   重试次数: {bot.config.get('verification', {}).get('captcha_retry_count', 3)}")
            
            print("\n🎯 现在你可以使用以下功能：")
            print("   - bot.auto_login()          # 自动登录（包含AI验证码识别）")
            print("   - bot.select_all_courses()  # 自动选课（包含AI验证码识别）")
            print("   - bot.check_all_courses()   # 检查课程状态")
            
            return True
        else:
            print("❌ 验证码识别器初始化失败")
            return False
            
    except Exception as e:
        print(f"❌ 演示过程中发生错误: {e}")
        return False

def demo_configuration():
    """演示配置选项"""
    print("\n=== 配置选项演示 ===")
    
    print("1. 环境变量配置（推荐）:")
    print("   export OPENAI_API_KEY='your_api_key'")
    print("   export NCKU_USERNAME='your_username'")
    print("   export NCKU_PASSWORD='your_password'")
    print("   export AUTO_CAPTCHA='true'")
    
    print("\n2. 配置文件配置:")
    print("   复制 config_example.json 为 config.json")
    print("   修改其中的配置信息")
    
    print("\n3. 主要配置选项:")
    print("   - openai_config.api_key: OpenAI API密钥")
    print("   - openai_config.model: 使用的模型（当前: gpt-5-fast）")
    print("   - verification.auto_captcha: 是否启用自动验证码识别")
    print("   - verification.captcha_retry_count: 验证码识别重试次数")
    
    return True

def main():
    """主演示函数"""
    print("🤖 NCKU Course Bot 使用演示")
    print("=" * 50)
    
    # 运行演示
    demos = [
        ("基本使用", demo_basic_usage),
        ("API密钥配置", demo_with_api_key),
        ("配置选项", demo_configuration)
    ]
    
    for demo_name, demo_func in demos:
        try:
            demo_func()
        except Exception as e:
            print(f"❌ {demo_name} 演示失败: {e}")
        
        print("-" * 30)
    
    print("\n=== 下一步操作 ===")
    print("1. 设置 OpenAI API 密钥")
    print("2. 配置课程信息")
    print("3. 运行测试: python test_auto_captcha.py")
    print("4. 开始使用: python course_bot.py")

if __name__ == "__main__":
    main()

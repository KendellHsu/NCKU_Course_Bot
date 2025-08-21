#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
十六进制验证码识别测试工具
专门针对4位十六进制验证码（0-F）进行优化测试
"""

import json
import time
import logging
import os
import sys
from pathlib import Path

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_hex_captcha_simulation():
    """测试十六进制验证码识别的模拟场景"""
    print("=== 十六进制验证码识别模拟测试 ===")
    
    try:
        from captcha_solver import CaptchaSolver
        
        # 创建测试实例（不需要真实的API密钥）
        solver = CaptchaSolver("test_key", "gpt-5-mini")
        
        # 模拟OpenAI API返回的各种情况
        simulation_cases = [
            {
                "name": "标准4位十六进制",
                "api_response": "验证码是1A2B",
                "expected": "1A2B"
            },
            {
                "name": "带空格和标点",
                "api_response": "这是 3C-4D 验证码",
                "expected": "3C4D"
            },
            {
                "name": "小写字母",
                "api_response": "验证码：a1b2",
                "expected": "A1B2"
            },
            {
                "name": "混合格式",
                "api_response": "验证码包含数字和字母：5E6F",
                "expected": "5E6F"
            },
            {
                "name": "超过4位",
                "api_response": "验证码是7A8B9C",
                "expected": "7A8B"
            },
            {
                "name": "少于4位",
                "api_response": "验证码是12",
                "expected": None
            },
            {
                "name": "包含无效字符",
                "api_response": "验证码是G1H2（G和H不是十六进制）",
                "expected": "1H2"  # 提取有效的部分
            },
            {
                "name": "空响应",
                "api_response": "",
                "expected": None
            }
        ]
        
        print("\n模拟测试结果:")
        successful_tests = 0
        
        for i, case in enumerate(simulation_cases, 1):
            result = solver._clean_hex_captcha(case["api_response"])
            status = "✅" if result == case["expected"] else "❌"
            print(f"{i:2d}. {status} {case['name']}")
            print(f"    输入: '{case['api_response']}'")
            print(f"    输出: '{result}' (期望: '{case['expected']}')")
            
            if result == case["expected"]:
                successful_tests += 1
            print()
        
        accuracy = (successful_tests / len(simulation_cases)) * 100
        print(f"模拟测试准确度: {accuracy:.1f}% ({successful_tests}/{len(simulation_cases)})")
        
        return successful_tests == len(simulation_cases)
        
    except Exception as e:
        print(f"❌ 模拟测试失败: {e}")
        return False

def test_real_image_recognition():
    """测试真实图片的十六进制验证码识别"""
    print("\n=== 真实图片十六进制验证码识别测试 ===")
    
    # 检查配置文件
    if not os.path.exists('config.json'):
        print("❌ 找不到配置文件 config.json")
        print("请确保配置文件存在并包含 OpenAI API 密钥")
        return False
    
    # 检查验证码识别器
    try:
        from captcha_solver import CaptchaSolver
        print("✅ 验证码识别器模块可用")
    except ImportError as e:
        print(f"❌ 无法导入验证码识别器: {e}")
        return False
    
    # 读取配置
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        api_key = config.get('openai_config', {}).get('api_key')
        if not api_key:
            print("❌ 配置文件中未找到 OpenAI API 密钥")
            return False
        
        print(f"✅ 找到API密钥: {api_key[:20]}...")
    except Exception as e:
        print(f"❌ 读取配置文件失败: {e}")
        return False
    
    # 查找当前目录下的图片文件
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp')
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(Path('.').glob(f'*{ext}'))
        image_files.extend(Path('.').glob(f'*{ext.upper()}'))
    
    # 过滤掉已处理的图片
    image_files = [f for f in image_files if not f.name.startswith(('processed_', 'test_'))]
    
    if not image_files:
        print("❌ 当前目录下没有找到图片文件")
        print("请将验证码图片放在当前目录下，支持的格式: PNG, JPG, JPEG, GIF, WEBP")
        return False
    
    print(f"🔍 找到 {len(image_files)} 张图片:")
    for i, img_file in enumerate(image_files, 1):
        print(f"   {i}. {img_file.name}")
    
    # 询问用户选择测试方式
    print("\n📋 请选择测试方式:")
    print("   1. 测试所有图片")
    print("   2. 选择特定图片")
    print("   3. 退出")
    
    choice = input("请输入选择 (1-3): ").strip()
    
    if choice == '1':
        return test_all_images(image_files, api_key)
    elif choice == '2':
        return test_specific_image(image_files, api_key)
    elif choice == '3':
        print("👋 退出测试")
        return True
    else:
        print("❌ 无效的选择")
        return False

def test_all_images(image_files, api_key):
    """测试所有图片"""
    print(f"\n🚀 开始测试所有 {len(image_files)} 张图片...")
    successful_tests = 0
    
    for i, img_file in enumerate(image_files, 1):
        print(f"\n--- 进度: {i}/{len(image_files)} ---")
        if test_single_hex_image(str(img_file), api_key):
            successful_tests += 1
        
        # 避免API调用过于频繁
        if i < len(image_files):
            print("⏳ 等待2秒后继续...")
            time.sleep(2)
    
    # 显示测试结果
    accuracy = (successful_tests / len(image_files)) * 100
    print(f"\n=== 批量测试结果 ===")
    print(f"总测试数量: {len(image_files)}")
    print(f"成功识别数量: {successful_tests}")
    print(f"识别准确度: {accuracy:.2f}%")
    
    if accuracy >= 80:
        print("🎉 优秀！十六进制验证码识别准确度很高")
    elif accuracy >= 60:
        print("👍 良好！十六进制验证码识别准确度不错")
    elif accuracy >= 40:
        print("⚠️  一般！十六进制验证码识别准确度有待提高")
    else:
        print("❌ 较差！十六进制验证码识别准确度需要大幅改进")
    
    return True

def test_specific_image(image_files, api_key):
    """测试特定图片"""
    print("\n📝 请输入要测试的图片编号:")
    try:
        img_index = int(input("图片编号: ")) - 1
        if 0 <= img_index < len(image_files):
            return test_single_hex_image(str(image_files[img_index]), api_key)
        else:
            print("❌ 无效的图片编号")
            return False
    except ValueError:
        print("❌ 请输入有效的数字")
        return False

def test_single_hex_image(image_path, api_key):
    """测试单张十六进制验证码图片"""
    try:
        print(f"\n=== 测试十六进制验证码图片: {image_path} ===")
        
        # 检查文件是否存在
        if not os.path.exists(image_path):
            print(f"❌ 图片文件不存在: {image_path}")
            return False
        
        # 检查文件格式
        if not image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            print(f"❌ 不支持的图片格式: {image_path}")
            print("支持的格式: PNG, JPG, JPEG, GIF, WEBP")
            return False
        
        # 初始化验证码识别器
        from captcha_solver import CaptchaSolver
        solver = CaptchaSolver(api_key, "gpt-4o-mini")
        print("✅ 验证码识别器初始化成功")
        
        # 加载图片
        from PIL import Image
        try:
            image = Image.open(image_path)
            print(f"✅ 成功加载图片: {image.size} × {image.mode}")
        except Exception as e:
            print(f"❌ 加载图片失败: {e}")
            return False
        
        # 跳过图像预处理，直接使用原图
        print("\n🔧 跳过图像预处理，使用原始图片...")
        processed_image = image  # 直接使用原图
        print("✅ 使用原始图片进行识别")
        
        # 测试十六进制验证码识别
        print("\n🤖 开始识别十六进制验证码...")
        start_time = time.time()
        
        try:
            # 使用原始图片识别
            result = solver.solve_captcha(processed_image, max_retries=3)
            
            recognition_time = time.time() - start_time
            
            if result:
                print(f"✅ 识别成功: '{result}' (耗时: {recognition_time:.2f}秒)")
                
                # 验证是否为有效的4位十六进制
                if len(result) == 4 and all(c in '0123456789ABCDEF' for c in result):
                    print("✅ 验证码格式正确：4位十六进制")
                else:
                    print("⚠️  验证码格式异常")
                
                # 询问用户识别结果是否正确
                print("\n📝 请确认识别结果:")
                print(f"   识别结果: {result}")
                print(f"   格式: 4位十六进制 (0-F)")
                user_input = input("   这个结果正确吗？(y/n): ").strip().lower()
                
                if user_input in ['y', 'yes', '是', '对']:
                    print("🎯 用户确认识别结果正确！")
                    return True
                else:
                    print("⚠️  用户认为识别结果不正确")
                    return False
            else:
                print("❌ 识别失败")
                return False
                
        except Exception as e:
            print(f"❌ 识别过程中发生错误: {e}")
            return False
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        return False

def main():
    """主函数"""
    print("🚀 十六进制验证码识别测试工具")
    print("=" * 50)
    print("专门针对4位十六进制验证码（0-F）进行优化")
    
    # 主菜单
    while True:
        print("\n📋 主菜单:")
        print("   1. 模拟测试（无需API）")
        print("   2. 真实图片测试")
        print("   3. 退出")
        
        choice = input("请输入选择 (1-3): ").strip()
        
        if choice == '1':
            # 模拟测试
            test_hex_captcha_simulation()
        
        elif choice == '2':
            # 真实图片测试
            test_real_image_recognition()
        
        elif choice == '3':
            print("👋 感谢使用！")
            break
        
        else:
            print("❌ 无效的选择")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 程序被用户中断")
    except Exception as e:
        print(f"\n❌ 程序执行错误: {e}")
        sys.exit(1)

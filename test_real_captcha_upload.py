#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
真实验证码图片上传测试功能
支持拖拽图片或选择图片文件进行验证码识别测试
"""

import json
import time
import logging
import os
import sys
from pathlib import Path

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_single_captcha_image(image_path):
    """
    测试单张验证码图片的识别
    
    Args:
        image_path (str): 图片文件路径
        
    Returns:
        bool: 测试是否成功
    """
    try:
        print(f"\n=== 测试验证码图片: {image_path} ===")
        
        # 检查文件是否存在
        if not os.path.exists(image_path):
            print(f"❌ 图片文件不存在: {image_path}")
            return False
        
        # 检查文件格式
        if not image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            print(f"❌ 不支持的图片格式: {image_path}")
            print("支持的格式: PNG, JPG, JPEG, GIF, WEBP")
            return False
        
        # 导入验证码识别器
        from captcha_solver import CaptchaSolver
        print("✅ 成功导入 CaptchaSolver")
        
        # 读取配置
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        api_key = config.get('openai_config', {}).get('api_key')
        if not api_key:
            print("❌ 配置文件中未找到 OpenAI API 密钥")
            return False
        
        print(f"✅ 找到API密钥: {api_key[:20]}...")
        
        # 初始化验证码识别器
        solver = CaptchaSolver(api_key, "gpt-5-mini")
        print("✅ 验证码识别器初始化成功")
        
        # 加载图片
        from PIL import Image
        try:
            image = Image.open(image_path)
            print(f"✅ 成功加载图片: {image.size} × {image.mode}")
        except Exception as e:
            print(f"❌ 加载图片失败: {e}")
            return False
        
        # 测试图像预处理
        print("\n🔧 测试图像预处理...")
        try:
            processed_image = solver.preprocess_image(image)
            if processed_image:
                print("✅ 图像预处理成功")
                
                # 保存预处理后的图片
                processed_path = f"processed_{os.path.basename(image_path)}"
                processed_image.save(processed_path)
                print(f"📸 预处理图片已保存: {processed_path}")
            else:
                print("❌ 图像预处理失败")
                processed_image = image  # 使用原图
        except Exception as e:
            print(f"⚠️  图像预处理出错: {e}")
            processed_image = image  # 使用原图
        
        # 测试验证码识别
        print("\n🤖 开始识别验证码...")
        start_time = time.time()
        
        try:
            # 使用预处理后的图片识别
            result = solver.solve_captcha(processed_image, max_retries=3)
            
            recognition_time = time.time() - start_time
            
            if result:
                print(f"✅ 识别成功: '{result}' (耗时: {recognition_time:.2f}秒)")
                
                # 询问用户识别结果是否正确
                print("\n📝 请确认识别结果:")
                print(f"   识别结果: {result}")
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

def test_multiple_images():
    """测试多张图片"""
    print("=== 批量验证码图片测试 ===")
    
    # 获取当前目录下的所有图片文件
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
        # 测试所有图片
        print(f"\n🚀 开始测试所有 {len(image_files)} 张图片...")
        successful_tests = 0
        
        for i, img_file in enumerate(image_files, 1):
            print(f"\n--- 进度: {i}/{len(image_files)} ---")
            if test_single_captcha_image(str(img_file)):
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
            print("🎉 优秀！识别准确度很高")
        elif accuracy >= 60:
            print("👍 良好！识别准确度不错")
        elif accuracy >= 40:
            print("⚠️  一般！识别准确度有待提高")
        else:
            print("❌ 较差！识别准确度需要大幅改进")
        
        return True
        
    elif choice == '2':
        # 选择特定图片
        print("\n📝 请输入要测试的图片编号:")
        try:
            img_index = int(input("图片编号: ")) - 1
            if 0 <= img_index < len(image_files):
                return test_single_captcha_image(str(image_files[img_index]))
            else:
                print("❌ 无效的图片编号")
                return False
        except ValueError:
            print("❌ 请输入有效的数字")
            return False
    
    elif choice == '3':
        print("👋 退出测试")
        return True
    
    else:
        print("❌ 无效的选择")
        return False

def interactive_upload():
    """交互式图片上传测试"""
    print("=== 交互式验证码图片测试 ===")
    
    while True:
        print("\n📋 请选择操作:")
        print("   1. 输入图片文件路径")
        print("   2. 拖拽图片到终端")
        print("   3. 查看当前目录图片")
        print("   4. 退出")
        
        choice = input("请输入选择 (1-4): ").strip()
        
        if choice == '1':
            # 输入图片路径
            image_path = input("请输入图片文件路径: ").strip()
            if image_path:
                # 去除可能的引号
                image_path = image_path.strip('"\'')
                test_single_captcha_image(image_path)
            else:
                print("❌ 路径不能为空")
        
        elif choice == '2':
            # 拖拽图片
            print("请将图片文件拖拽到终端中，然后按Enter:")
            image_path = input().strip()
            if image_path:
                # 去除可能的引号
                image_path = image_path.strip('"\'')
                test_single_captcha_image(image_path)
            else:
                print("❌ 没有接收到图片路径")
        
        elif choice == '3':
            # 查看当前目录图片
            image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp')
            image_files = []
            
            for ext in image_extensions:
                image_files.extend(Path('.').glob(f'*{ext}'))
                image_files.extend(Path('.').glob(f'*{ext.upper()}'))
            
            # 过滤掉已处理的图片
            image_files = [f for f in image_files if not f.name.startswith(('processed_', 'test_'))]
            
            if image_files:
                print(f"\n🔍 当前目录下的图片文件 ({len(image_files)} 张):")
                for i, img_file in enumerate(image_files, 1):
                    print(f"   {i}. {img_file.name}")
            else:
                print("\n❌ 当前目录下没有找到图片文件")
        
        elif choice == '4':
            print("👋 退出测试")
            break
        
        else:
            print("❌ 无效的选择")

def main():
    """主函数"""
    print("🚀 真实验证码图片识别测试工具")
    print("=" * 50)
    
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
    
    # 主菜单
    while True:
        print("\n📋 主菜单:")
        print("   1. 单张图片测试")
        print("   2. 批量图片测试")
        print("   3. 交互式测试")
        print("   4. 退出")
        
        choice = input("请输入选择 (1-4): ").strip()
        
        if choice == '1':
            # 单张图片测试
            image_path = input("请输入图片文件路径: ").strip()
            if image_path:
                image_path = image_path.strip('"\'')
                test_single_captcha_image(image_path)
            else:
                print("❌ 路径不能为空")
        
        elif choice == '2':
            # 批量图片测试
            test_multiple_images()
        
        elif choice == '3':
            # 交互式测试
            interactive_upload()
        
        elif choice == '4':
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
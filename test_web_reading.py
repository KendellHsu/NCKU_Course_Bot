#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試腳本：測試 course_bot.py 的網頁讀取功能
"""

import sys
import time
from course_bot import NCKUCourseBot

def test_web_reading():
    """測試網頁讀取功能"""
    print("=== 測試 NCKU Course Bot 網頁讀取功能 ===")
    print("\n請選擇測試方式：")
    print("1. 連接到現有的 Arc 瀏覽器（需要先手動登入選課系統）")
    print("2. 開啟新的 Arc 瀏覽器（會自動開啟新視窗）")
    print("3. 只測試配置載入（不開啟瀏覽器）")
    print("4. 退出")
    
    while True:
        try:
            choice = input("\n請輸入選項 (1-4): ").strip()
            
            if choice == "1":
                return test_existing_browser()
            elif choice == "2":
                return test_new_browser()
            elif choice == "3":
                return test_config_only()
            elif choice == "4":
                print("退出測試")
                return True
            else:
                print("❌ 無效選項，請重新輸入")
                
        except KeyboardInterrupt:
            print("\n\n測試被中斷")
            return False
        except Exception as e:
            print(f"❌ 發生錯誤: {e}")
            return False

def test_existing_browser():
    """測試連接到現有瀏覽器"""
    print("\n=== 測試連接到現有 Arc 瀏覽器 ===")
    print("⚠️  請確保你已經在 Arc 瀏覽器中登入選課系統")
    print("⚠️  如果沒有登入，程式會提示你手動登入")
    
    input("準備好後按 Enter 繼續...")
    
    try:
        bot = NCKUCourseBot()
        print("✅ 成功建立機器人實例")
        
        # 嘗試連接到現有瀏覽器
        if bot.connect_to_existing_browser():
            print("✅ 成功連接到現有瀏覽器")
            
            # 檢查登入狀態
            if bot.check_login_status():
                print("✅ 登入狀態檢查通過")
                
                # 檢查課程
                bot.check_all_courses()
                
                # 保持瀏覽器開啟
                input("\n按 Enter 關閉瀏覽器連接...")
                bot.driver.quit()
                return True
            else:
                print("❌ 登入狀態檢查失敗")
                print("請手動登入選課系統後再試")
                return False
        else:
            print("❌ 無法連接到現有瀏覽器")
            print("請確保 Arc 瀏覽器正在運行")
            return False
            
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")
        return False

def test_new_browser():
    """測試開啟新瀏覽器"""
    print("\n=== 測試開啟新的 Arc 瀏覽器 ===")
    print("⚠️  這會開啟一個新的 Arc 瀏覽器視窗")
    print("⚠️  你需要手動登入選課系統")
    
    input("準備好後按 Enter 繼續...")
    
    try:
        bot = NCKUCourseBot()
        print("✅ 成功建立機器人實例")
        
        # 開啟新瀏覽器
        if bot.start_new_browser():
            print("✅ 成功開啟新瀏覽器")
            
            # 導航到選課頁面
            print(f"正在導航到選課頁面: {bot.config['course_selection_url']}")
            bot.driver.get(bot.config['course_selection_url'])
            
            print("✅ 已導航到選課頁面")
            print("請在瀏覽器中手動登入選課系統")
            
            # 等待用戶登入
            input("登入完成後按 Enter 繼續測試...")
            
            # 檢查登入狀態
            if bot.check_login_status():
                print("✅ 登入狀態檢查通過")
                
                # 檢查課程
                bot.check_all_courses()
                
                # 保持瀏覽器開啟
                input("\n按 Enter 關閉瀏覽器...")
                bot.driver.quit()
                return True
            else:
                print("❌ 登入狀態檢查失敗")
                bot.driver.quit()
                return False
        else:
            print("❌ 無法開啟新瀏覽器")
            return False
            
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")
        return False

def test_config_only():
    """只測試配置載入"""
    print("\n=== 測試配置載入 ===")
    
    try:
        bot = NCKUCourseBot()
        print("✅ 成功建立機器人實例")
        
        # 顯示配置資訊
        print(f"\n📋 配置資訊:")
        print(f"選課系統 URL: {bot.config['course_selection_url']}")
        print(f"課程數量: {len(bot.config['courses'])}")
        
        print(f"\n📚 課程列表:")
        for i, course in enumerate(bot.config['courses'], 1):
            print(f"\n課程 {i}:")
            print(f"  系所代碼: {course['department_code']}")
            print(f"  課程編號: {course['course_number']}")
            print(f"  課程名稱: {course['course_name']}")
        
        print("\n✅ 配置載入測試完成")
        return True
        
    except Exception as e:
        print(f"❌ 配置載入測試失敗: {e}")
        return False

def main():
    """主函數"""
    print("🚀 NCKU Course Bot 網頁讀取功能測試")
    print("=" * 50)
    
    try:
        success = test_web_reading()
        
        if success:
            print("\n🎉 測試完成！")
        else:
            print("\n⚠️  測試過程中遇到問題")
            
    except KeyboardInterrupt:
        print("\n\n測試被使用者中斷")
    except Exception as e:
        print(f"\n❌ 測試過程中發生未預期的錯誤: {e}")

if __name__ == "__main__":
    main()

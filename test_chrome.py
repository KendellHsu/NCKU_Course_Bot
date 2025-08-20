#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chrome 瀏覽器測試：測試 course_bot.py 的網頁讀取功能
"""

from course_bot import NCKUCourseBot
import time

def test_chrome_browser():
    """測試 Chrome 瀏覽器功能"""
    print("=== 測試 Chrome 瀏覽器網頁讀取功能 ===")
    print("\n請選擇測試方式：")
    print("1. 連接到現有的 Chrome 瀏覽器（需要先手動登入選課系統）")
    print("2. 開啟新的 Chrome 瀏覽器（會自動開啟新視窗）")
    print("3. 只測試配置載入（不開啟瀏覽器）")
    print("4. 測試選課功能（需要先登入選課系統）")
    print("5. 退出")
    
    while True:
        try:
            choice = input("\n請輸入選項 (1-4): ").strip()
            
            if choice == "1":
                return test_existing_chrome()
            elif choice == "2":
                return test_new_chrome()
            elif choice == "3":
                return test_config_only()
            elif choice == "4":
                return test_course_selection()
            elif choice == "5":
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

def test_existing_chrome():
    """測試連接到現有 Chrome 瀏覽器"""
    print("\n=== 測試連接到現有 Chrome 瀏覽器 ===")
    print("⚠️  請按照以下步驟操作：")
    print("1. 關閉所有 Chrome 瀏覽器視窗")
    print("2. 在終端機中執行：")
    print("   /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222")
    print("3. 在新開啟的 Chrome 中登入選課系統")
    print("4. 導航到選課頁面：https://course.ncku.edu.tw/index.php?c=cos21322")
    
    input("完成上述步驟後按 Enter 繼續...")
    
    try:
        bot = NCKUCourseBot()
        print("✅ 成功建立機器人實例")
        
        # 嘗試連接到現有瀏覽器
        print("正在嘗試連接到現有 Chrome 瀏覽器...")
        if bot.connect_to_existing_browser():
            print("✅ 成功連接到現有 Chrome 瀏覽器")
            
            # 顯示當前頁面資訊
            current_url = bot.driver.current_url
            page_title = bot.driver.title
            print(f"當前頁面 URL: {current_url}")
            print(f"頁面標題: {page_title}")
            
            # 檢查登入狀態
            print("\n正在檢查登入狀態...")
            if bot.check_login_status():
                print("✅ 登入狀態檢查通過")
                
                # 檢查課程
                print("\n正在檢查課程...")
                bot.check_all_courses()
                
                # 保持瀏覽器開啟
                input("\n按 Enter 關閉瀏覽器連接...")
                bot.driver.quit()
                return True
            else:
                print("❌ 登入狀態檢查失敗")
                print("請確保你已經登入選課系統")
                return False
        else:
            print("❌ 無法連接到現有 Chrome 瀏覽器")
            print("請確保 Chrome 已開啟調試模式（端口 9222）")
            return False
            
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")
        return False

def test_new_chrome():
    """測試開啟新 Chrome 瀏覽器"""
    print("\n=== 測試開啟新的 Chrome 瀏覽器 ===")
    print("⚠️  這會開啟一個新的 Chrome 瀏覽器視窗")
    print("⚠️  你需要手動登入選課系統")
    
    input("準備好後按 Enter 繼續...")
    
    try:
        bot = NCKUCourseBot()
        print("✅ 成功建立機器人實例")
        
        # 開啟新瀏覽器
        if bot.start_new_browser():
            print("✅ 成功開啟新 Chrome 瀏覽器")
            
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
            print("❌ 無法開啟新 Chrome 瀏覽器")
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

def test_course_selection():
    """測試選課功能"""
    print("\n=== 測試選課功能 ===")
    print("⚠️  這會開啟一個新的 Chrome 瀏覽器視窗")
    print("⚠️  你需要手動登入選課系統")
    print("⚠️  程式會自動點擊選課按鈕並等待你輸入驗證碼")
    
    input("準備好後按 Enter 繼續...")
    
    try:
        bot = NCKUCourseBot()
        print("✅ 成功建立機器人實例")
        
        # 開啟新瀏覽器
        if bot.start_new_browser():
            print("✅ 成功開啟新 Chrome 瀏覽器")
            
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
                print("\n正在檢查課程...")
                bot.check_all_courses()
                
                # 開始選課
                print("\n開始測試選課功能...")
                bot.select_all_courses()
                
                # 保持瀏覽器開啟
                input("\n按 Enter 關閉瀏覽器...")
                bot.driver.quit()
                return True
            else:
                print("❌ 登入狀態檢查失敗")
                bot.driver.quit()
                return False
        else:
            print("❌ 無法開啟新 Chrome 瀏覽器")
            return False
            
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")
        return False

def main():
    """主函數"""
    print("🚀 Chrome 瀏覽器網頁讀取功能測試")
    print("=" * 50)
    
    try:
        success = test_chrome_browser()
        
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試按鈕檢測功能
"""

from course_bot import NCKUCourseBot
from selenium.webdriver.common.by import By
import time

def test_button_detection():
    """測試確認按鈕的檢測功能"""
    print("=== 測試確認按鈕檢測功能 ===")
    print("此測試將：")
    print("1. 開啟瀏覽器並導航到選課頁面")
    print("2. 等待你登入")
    print("3. 點擊選課按鈕")
    print("4. 檢測是否能找到確認按鈕")
    
    input("\n準備好後按 Enter 繼續...")
    
    try:
        bot = NCKUCourseBot()
        print("✅ 成功建立機器人實例")
        
        # 開啟瀏覽器
        if bot.start_new_browser():
            print("✅ 成功開啟 Chrome 瀏覽器")
            
            # 導航到選課頁面
            bot.driver.get(bot.config['course_selection_url'])
            print("✅ 已導航到選課頁面")
            
            # 等待登入
            input("請在瀏覽器中登入，然後按 Enter 繼續...")
            
            # 檢查登入狀態
            if bot.check_login_status():
                print("✅ 登入狀態檢查通過")
                
                # 檢查課程
                bot.check_all_courses()
                
                # 只測試第一個課程的按鈕檢測
                if bot.config['courses']:
                    course = bot.config['courses'][0]
                    print(f"\n🔍 測試課程: {course['course_name']}")
                    
                    if 'select_button' in course:
                        print("✅ 找到選課按鈕，準備點擊...")
                        
                        # 點擊選課按鈕
                        course['select_button'].click()
                        print("✅ 已點擊選課按鈕")
                        
                        # 等待頁面變化
                        time.sleep(2)
                        
                        # 嘗試檢測確認按鈕
                        print("\n🔍 開始檢測確認按鈕...")
                        
                        confirm_button = None
                        
                        # 測試所有可能的按鈕定位方式
                        methods = [
                            ("特定class: addcourse_confirm_save_button", "//button[contains(@class, 'addcourse_confirm_save_button')]"),
                            ("文字內容: 確定", "//button[contains(text(), '確定')]"),
                            ("通用class: confirm/save", "//button[contains(@class, 'confirm') or contains(@class, 'save')]"),
                            ("按鈕樣式: btn-danger", "//button[@type='button' and contains(@class, 'btn-danger')]"),
                            ("modal屬性", "//button[@data-dismiss='modal' and contains(text(), '確定')]"),
                        ]
                        
                        for method_name, xpath in methods:
                            try:
                                button = bot.driver.find_element(By.XPATH, xpath)
                                if button:
                                    print(f"✅ 方法成功: {method_name}")
                                    print(f"   按鈕文字: {button.text}")
                                    print(f"   按鈕類別: {button.get_attribute('class')}")
                                    print(f"   是否可用: {button.is_enabled()}")
                                    confirm_button = button
                                    break
                            except Exception as e:
                                print(f"❌ 方法失敗: {method_name}")
                        
                        if confirm_button:
                            print(f"\n🎉 成功找到確認按鈕！")
                            choice = input("是否要點擊確認按鈕進行測試？(y/N): ").strip().lower()
                            if choice == 'y':
                                print("點擊確認按鈕...")
                                confirm_button.click()
                                print("✅ 已點擊確認按鈕")
                        else:
                            print("\n❌ 無法找到確認按鈕")
                            print("讓我們檢查頁面上所有的按鈕...")
                            
                            # 列出所有按鈕供參考
                            all_buttons = bot.driver.find_elements(By.TAG_NAME, "button")
                            print(f"\n頁面上共有 {len(all_buttons)} 個按鈕：")
                            for i, btn in enumerate(all_buttons):
                                print(f"{i+1}. 文字: '{btn.text}' | 類別: '{btn.get_attribute('class')}'")
                    else:
                        print("❌ 未找到選課按鈕")
                else:
                    print("❌ 配置中沒有課程")
            else:
                print("❌ 登入狀態檢查失敗")
            
            # 保持瀏覽器開啟
            input("\n按 Enter 關閉瀏覽器...")
            bot.driver.quit()
            
        else:
            print("❌ 無法開啟瀏覽器")
            
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")

def main():
    print("🔍 確認按鈕檢測測試")
    print("=" * 50)
    test_button_detection()

if __name__ == "__main__":
    main()

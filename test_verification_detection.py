#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
專門測試驗證碼輸入框檢測功能
"""

from course_bot import NCKUCourseBot
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_verification_detection():
    """測試驗證碼輸入框檢測功能"""
    print("=== 測試驗證碼輸入框檢測功能 ===")
    print("此測試將：")
    print("1. 開啟瀏覽器並導航到選課頁面")
    print("2. 等待你登入")
    print("3. 點擊選課按鈕")
    print("4. 檢測是否能找到驗證碼輸入框")
    print("5. 等待你輸入驗證碼")
    print("6. 檢測確認按鈕")
    
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
                
                # 只測試第一個課程
                if bot.config['courses']:
                    course = bot.config['courses'][0]
                    print(f"\n🔍 測試課程: {course['course_name']}")
                    
                    if 'select_button' in course:
                        print("✅ 找到選課按鈕，準備點擊...")
                        
                        # 點擊選課按鈕
                        course['select_button'].click()
                        print("✅ 已點擊選課按鈕")
                        
                        # 等待頁面變化
                        print("⏳ 等待驗證碼輸入框出現...")
                        time.sleep(2)
                        
                        # 開始檢測驗證碼輸入框
                        print("\n🔍 開始檢測驗證碼輸入框...")
                        
                        verification_input = None
                        verification_found = False
                        
                        # 測試所有可能的驗證碼輸入框定位方式
                        methods = [
                            ("確切name: cos_qry_confirm_validation_code", "//input[@name='cos_qry_confirm_validation_code']"),
                            ("確切id: cos_qry_confirm_validation_code", "//input[@id='cos_qry_confirm_validation_code']"),
                            ("placeholder: 請輸入驗證碼", "//input[contains(@placeholder, '請輸入驗證碼')]"),
                            ("class+maxlength: form-control+4", "//input[@class='form-control' and @maxlength='4']"),
                            ("文字標籤", "//input[preceding-sibling::*[contains(text(), '驗證碼')] or following-sibling::*[contains(text(), '驗證碼')]]"),
                            ("4位數輸入框", "//input[@type='text' and @maxlength='4']"),
                            ("modal輸入框", "//div[contains(@class, 'modal')]//input[@type='text']"),
                            ("modal body輸入框", "//div[contains(@class, 'modal-body')]//input[@type='text']"),
                        ]
                        
                        for method_name, xpath in methods:
                            try:
                                input_element = bot.driver.find_element(By.XPATH, xpath)
                                if input_element:
                                    print(f"✅ 方法成功: {method_name}")
                                    print(f"   輸入框類型: {input_element.get_attribute('type')}")
                                    print(f"   輸入框類別: {input_element.get_attribute('class')}")
                                    print(f"   輸入框名稱: {input_element.get_attribute('name')}")
                                    print(f"   輸入框ID: {input_element.get_attribute('id')}")
                                    print(f"   最大長度: {input_element.get_attribute('maxlength')}")
                                    print(f"   佔位符: {input_element.get_attribute('placeholder')}")
                                    print(f"   是否可見: {input_element.is_displayed()}")
                                    print(f"   是否可用: {input_element.is_enabled()}")
                                    verification_input = input_element
                                    verification_found = True
                                    break
                            except Exception as e:
                                print(f"❌ 方法失敗: {method_name}")
                        
                        if verification_input:
                            print(f"\n🎉 成功找到驗證碼輸入框！")
                            print("📝 請在瀏覽器中輸入驗證碼...")
                            print("⏰ 程式會等待 2 秒...")
                            
                            # 等待用戶輸入驗證碼
                            time.sleep(2)
                            
                            print("⏱️  時間到！開始檢測確認按鈕...")
                            
                            # 檢測確認按鈕
                            confirm_button = None
                            confirm_methods = [
                                ("特定class: addcourse_confirm_save_button", "//button[contains(@class, 'addcourse_confirm_save_button')]"),
                                ("文字內容: 確定", "//button[contains(text(), '確定')]"),
                                ("通用class: confirm/save", "//button[contains(@class, 'confirm') or contains(@class, 'save')]"),
                                ("按鈕樣式: btn-danger", "//button[@type='button' and contains(@class, 'btn-danger')]"),
                                ("modal屬性", "//button[@data-dismiss='modal' and contains(text(), '確定')]"),
                            ]
                            
                            for method_name, xpath in confirm_methods:
                                try:
                                    button = bot.driver.find_element(By.XPATH, xpath)
                                    if button:
                                        print(f"✅ 確認按鈕檢測成功: {method_name}")
                                        print(f"   按鈕文字: {button.text}")
                                        print(f"   按鈕類別: {button.get_attribute('class')}")
                                        print(f"   是否可用: {button.is_enabled()}")
                                        confirm_button = button
                                        break
                                except Exception as e:
                                    print(f"❌ 確認按鈕檢測失敗: {method_name}")
                            
                            if confirm_button:
                                print(f"\n🎉 成功找到確認按鈕！")
                                choice = input("是否要點擊確認按鈕完成選課？(y/N): ").strip().lower()
                                if choice == 'y':
                                    print("點擊確認按鈕...")
                                    confirm_button.click()
                                    print("✅ 已點擊確認按鈕")
                                    print("🎉 選課流程完成！")
                                else:
                                    print("選課已取消")
                            else:
                                print("\n❌ 無法找到確認按鈕")
                                print("請檢查頁面上是否有確認按鈕")
                        else:
                            print("\n❌ 無法找到驗證碼輸入框")
                            print("讓我們檢查頁面上所有的輸入框...")
                            
                            # 列出所有輸入框供參考
                            all_inputs = bot.driver.find_elements(By.TAG_NAME, "input")
                            print(f"\n頁面上共有 {len(all_inputs)} 個輸入框：")
                            for i, inp in enumerate(all_inputs):
                                input_type = inp.get_attribute('type')
                                input_class = inp.get_attribute('class')
                                input_name = inp.get_attribute('name')
                                input_id = inp.get_attribute('id')
                                input_placeholder = inp.get_attribute('placeholder')
                                print(f"{i+1}. 類型: {input_type} | 類別: {input_class} | 名稱: {input_name} | ID: {input_id} | 佔位符: {input_placeholder}")
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
    print("🔍 驗證碼輸入框檢測測試")
    print("=" * 50)
    test_verification_detection()

if __name__ == "__main__":
    main()

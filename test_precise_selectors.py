#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試精確選擇器功能
"""

from course_bot import NCKUCourseBot
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_precise_selectors():
    """測試精確選擇器功能"""
    print("=== 測試精確選擇器功能 ===")
    print("此測試將：")
    print("1. 開啟瀏覽器並導航到登入頁面")
    print("2. 使用精確選擇器查找登入元素")
    print("3. 自動填入帳號密碼")
    print("4. 等待你輸入登入驗證碼")
    print("5. 自動點擊登入按鈕")
    
    input("\n準備好後按 Enter 繼續...")
    
    try:
        bot = NCKUCourseBot()
        print("✅ 成功建立機器人實例")
        
        # 顯示配置資訊
        print(f"\n📋 配置資訊:")
        print(f"登入頁面: {bot.config['course_selection_url']}")
        print(f"帳號: {bot.config['login_info']['username']}")
        print(f"密碼: {'*' * len(bot.config['login_info']['password'])}")
        
        # 開啟瀏覽器
        if bot.start_new_browser():
            print("✅ 成功開啟 Chrome 瀏覽器")
            
            # 導航到登入頁面
            print(f"\n🌐 導航到登入頁面: {bot.config['course_selection_url']}")
            bot.driver.get(bot.config['course_selection_url'])
            
            # 等待頁面載入
            time.sleep(3)
            
            print("✅ 已導航到登入頁面")
            print("\n🔍 開始測試精確選擇器...")
            
            # 測試帳號輸入框選擇器
            print("\n📝 測試帳號輸入框選擇器...")
            username_input = None
            username_selectors = [
                ("最精確: name='user_id'", "//input[@name='user_id']"),
                ("備用: id='user_id'", "//input[@id='user_id']"),
                ("備用: placeholder", "//input[@placeholder='學號/識別證號']"),
                ("備用: class+type", "//input[@class='form-control acpwd_input rwd_input1_3'][@type='text']"),
                ("備用: type+maxlength", "//input[@type='text'][@maxlength='9']"),
                ("最後備用: 第一個文字輸入框", "//input[@type='text'][1]")
            ]
            
            for method_name, xpath in username_selectors:
                try:
                    element = bot.driver.find_element(By.XPATH, xpath)
                    if element:
                        print(f"✅ {method_name}")
                        print(f"   元素類型: {element.tag_name}")
                        print(f"   元素類別: {element.get_attribute('class')}")
                        print(f"   元素名稱: {element.get_attribute('name')}")
                        print(f"   元素ID: {element.get_attribute('id')}")
                        print(f"   佔位符: {element.get_attribute('placeholder')}")
                        print(f"   是否可見: {element.is_displayed()}")
                        print(f"   是否可用: {element.is_enabled()}")
                        username_input = element
                        break
                except Exception as e:
                    print(f"❌ {method_name}: {e}")
            
            if not username_input:
                print("❌ 無法找到帳號輸入框")
                return False
            
            # 測試密碼輸入框選擇器
            print("\n🔒 測試密碼輸入框選擇器...")
            password_input = None
            password_selectors = [
                ("最精確: name='passwd'", "//input[@name='passwd']"),
                ("備用: id='passwd'", "//input[@id='passwd']"),
                ("備用: placeholder", "//input[@placeholder='同成功入口']"),
                ("備用: class+type", "//input[@class='form-control acpwd_input rwd_input1_3'][@type='password']"),
                ("最後備用: 密碼類型", "//input[@type='password']")
            ]
            
            for method_name, xpath in password_selectors:
                try:
                    element = bot.driver.find_element(By.XPATH, xpath)
                    if element:
                        print(f"✅ {method_name}")
                        print(f"   元素類型: {element.tag_name}")
                        print(f"   元素類別: {element.get_attribute('class')}")
                        print(f"   元素名稱: {element.get_attribute('name')}")
                        print(f"   元素ID: {element.get_attribute('id')}")
                        print(f"   佔位符: {element.get_attribute('placeholder')}")
                        print(f"   是否可見: {element.is_displayed()}")
                        print(f"   是否可用: {element.is_enabled()}")
                        password_input = element
                        break
                except Exception as e:
                    print(f"❌ {method_name}: {e}")
            
            if not password_input:
                print("❌ 無法找到密碼輸入框")
                return False
            
            # 測試登入按鈕選擇器
            print("\n🔘 測試登入按鈕選擇器...")
            login_button = None
            login_selectors = [
                ("最精確: id='submit_by_acpw'", "//button[@id='submit_by_acpw']"),
                ("備用: type+class", "//button[@type='submit'][@class='btn btn-default']"),
                ("備用: class", "//button[contains(@class, 'btn-default')]"),
                ("備用: type", "//button[@type='submit']"),
                ("備用: 文字內容", "//button[contains(text(), '登入')]"),
                ("最後備用: 英文文字", "//button[contains(text(), 'Login')]")
            ]
            
            for method_name, xpath in login_selectors:
                try:
                    element = bot.driver.find_element(By.XPATH, xpath)
                    if element:
                        print(f"✅ {method_name}")
                        print(f"   元素類型: {element.tag_name}")
                        print(f"   元素類別: {element.get_attribute('class')}")
                        print(f"   元素ID: {element.get_attribute('id')}")
                        print(f"   按鈕文字: {element.text}")
                        print(f"   是否可見: {element.is_displayed()}")
                        print(f"   是否可用: {element.is_enabled()}")
                        login_button = element
                        break
                except Exception as e:
                    print(f"❌ {method_name}: {e}")
            
            if not login_button:
                print("❌ 無法找到登入按鈕")
                return False
            
            # 所有元素都找到了，開始自動登入流程
            print(f"\n🎉 所有登入元素都找到了！")
            print("📝 開始自動填入帳號密碼...")
            
            # 填入帳號密碼
            username_input.clear()
            username_input.send_keys(bot.config['login_info']['username'])
            password_input.clear()
            password_input.send_keys(bot.config['login_info']['password'])
            
            print(f"✅ 帳號密碼已填入")
            print(f"   帳號: {bot.config['login_info']['username']}")
            print(f"   密碼: {'*' * len(bot.config['login_info']['password'])}")
            print(f"⏰ 請在瀏覽器中輸入登入驗證碼，然後按 Enter 繼續...")
            
            # 等待用戶輸入驗證碼
            input()
            
            # 點擊登入按鈕
            print("🔘 點擊登入按鈕...")
            login_button.click()
            
            # 等待登入完成
            print("⏳ 等待登入完成...")
            time.sleep(3)
            
            # 檢查登入狀態
            if bot.check_login_status():
                print("✅ 登入成功！")
                
                # 檢查課程
                print("\n📚 檢查課程...")
                bot.check_all_courses()
                
                # 保持瀏覽器開啟
                input("\n按 Enter 關閉瀏覽器...")
                bot.driver.quit()
                return True
            else:
                print("❌ 登入失敗或仍在登入頁面")
                bot.driver.quit()
                return False
                
        else:
            print("❌ 無法開啟瀏覽器")
            return False
            
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")
        return False

def main():
    print("🔍 精確選擇器測試")
    print("=" * 50)
    
    try:
        success = test_precise_selectors()
        
        if success:
            print("\n🎉 測試完成！")
            print("精確選擇器功能運作正常")
        else:
            print("\n⚠️  測試過程中遇到問題")
            
    except KeyboardInterrupt:
        print("\n\n測試被使用者中斷")
    except Exception as e:
        print(f"\n❌ 測試過程中發生未預期的錯誤: {e}")

if __name__ == "__main__":
    main()

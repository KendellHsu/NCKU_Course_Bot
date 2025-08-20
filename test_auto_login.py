#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試自動登入功能
"""

from course_bot import NCKUCourseBot
import time

def test_auto_login():
    """測試自動登入功能"""
    print("=== 測試自動登入功能 ===")
    print("此測試將：")
    print("1. 開啟瀏覽器")
    print("2. 自動填入帳號密碼")
    print("3. 等待你輸入登入驗證碼")
    print("4. 自動點擊登入按鈕")
    print("5. 檢查登入狀態")
    print("6. 測試選課功能")
    
    input("\n準備好後按 Enter 繼續...")
    
    try:
        bot = NCKUCourseBot()
        print("✅ 成功建立機器人實例")
        
        # 顯示配置資訊
        print(f"\n📋 配置資訊:")
        print(f"選課系統 URL: {bot.config['course_selection_url']}")
        print(f"帳號: {bot.config['login_info']['username']}")
        print(f"密碼: {'*' * len(bot.config['login_info']['password'])}")
        print(f"課程數量: {len(bot.config['courses'])}")
        
        # 開啟瀏覽器
        if bot.start_new_browser():
            print("✅ 成功開啟 Chrome 瀏覽器")
            
            # 開始自動登入
            print("\n🚀 開始自動登入流程...")
            if bot.auto_login():
                print("✅ 自動登入成功！")
                
                # 檢查課程
                print("\n📚 檢查課程...")
                bot.check_all_courses()
                
                # 詢問是否要測試選課
                choice = input("\n是否要測試選課功能？(y/N): ").strip().lower()
                if choice == 'y':
                    print("\n🚀 開始測試選課功能...")
                    bot.select_all_courses()
                else:
                    print("選課測試已跳過")
                
                # 保持瀏覽器開啟
                input("\n按 Enter 關閉瀏覽器...")
                bot.driver.quit()
                return True
            else:
                print("❌ 自動登入失敗")
                bot.driver.quit()
                return False
        else:
            print("❌ 無法開啟瀏覽器")
            return False
            
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")
        return False

def main():
    print("🚀 自動登入功能測試")
    print("=" * 50)
    
    try:
        success = test_auto_login()
        
        if success:
            print("\n🎉 測試完成！")
            print("自動登入功能運作正常")
        else:
            print("\n⚠️  測試過程中遇到問題")
            
    except KeyboardInterrupt:
        print("\n\n測試被使用者中斷")
    except Exception as e:
        print(f"\n❌ 測試過程中發生未預期的錯誤: {e}")

if __name__ == "__main__":
    main()

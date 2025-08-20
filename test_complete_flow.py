#!/usr/bin/env python3
"""
完整流程測試 - 自動登入 + 課程檢查 + 選課
"""

import sys
import time
from course_bot import NCKUCourseBot

def main():
    print("🚀 完整流程測試")
    print("=" * 50)
    print("=== 完整自動化選課流程 ===")
    print("此測試將：")
    print("1. 開啟瀏覽器")
    print("2. 自動填入帳號密碼")
    print("3. 等待你輸入登入驗證碼")
    print("4. 自動登入並導向選課頁面")
    print("5. 檢查設定的課程")
    print("6. 自動選課（需要你輸入選課驗證碼）")
    print()
    
    input("準備好後按 Enter 繼續...")
    
    try:
        # 建立機器人實例
        print("✅ 成功建立機器人實例")
        bot = NCKUCourseBot()
        
        # 顯示配置資訊
        print("\n📋 配置資訊:")
        print(f"選課頁面: {bot.config['course_selection_url']}")
        print(f"帳號: {bot.config['login_info']['username']}")
        print(f"密碼: {'*' * len(bot.config['login_info']['password'])}")
        print(f"課程數量: {len(bot.config['courses'])}")
        
        # 開啟瀏覽器
        if bot.start_new_browser():
            print("✅ 成功開啟瀏覽器")
        else:
            print("❌ 無法開啟瀏覽器")
            return False
        
        # 自動登入
        print("\n🔐 開始自動登入流程...")
        if bot.auto_login():
            print("✅ 自動登入成功，已導向選課頁面")
        else:
            print("❌ 自動登入失敗")
            input("按 Enter 關閉瀏覽器...")
            bot.close()
            return False
        
        # 檢查課程
        print("\n📚 檢查課程...")
        bot.check_all_courses()
        
        # 詢問是否要進行選課
        print("\n🎯 選課選項:")
        print("1. 自動選課（推薦）")
        print("2. 只檢查，不選課")
        print("3. 結束測試")
        
        choice = input("請選擇 (1/2/3): ").strip()
        
        if choice == "1":
            print("\n🎯 開始自動選課...")
            bot.select_all_courses()
            print("✅ 選課流程完成")
        elif choice == "2":
            print("✅ 僅檢查課程，未進行選課")
        else:
            print("✅ 測試結束")
        
        input("\n按 Enter 關閉瀏覽器...")
        bot.close()
        
        print("🎉 完整流程測試完成！")
        return True
        
    except Exception as e:
        print(f"⚠️  測試過程中遇到問題: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)

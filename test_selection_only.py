#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
專門測試選課功能的腳本
"""

from course_bot import NCKUCourseBot
import time

def test_course_selection_only():
    """專門測試選課功能"""
    print("=== 專門測試選課功能 ===")
    print("⚠️  請確保你已經：")
    print("   1. 在瀏覽器中登入選課系統")
    print("   2. 導航到選課頁面")
    print("   3. 可以看到課程列表")
    print("\n此測試將：")
    print("   1. 檢查課程是否存在")
    print("   2. 點擊選課按鈕")
    print("   3. 等待你輸入驗證碼（2秒）")
    print("   4. 自動點擊確認按鈕")
    
    input("\n準備好後按 Enter 開始測試...")
    
    try:
        # 建立機器人實例
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
            input("登入完成後按 Enter 繼續...")
            
            # 檢查登入狀態和課程
            if bot.check_login_status():
                print("✅ 登入狀態檢查通過")
                
                # 檢查課程並準備選課按鈕
                bot.check_all_courses()
                
                # 詢問用戶是否要開始選課
                print("\n" + "="*50)
                print("⚠️  注意：接下來將開始實際選課流程！")
                print("⚠️  程式會點擊選課按鈕並等待你輸入驗證碼")
                choice = input("是否繼續進行選課？(y/N): ").strip().lower()
                
                if choice == 'y' or choice == 'yes':
                    print("\n🚀 開始選課流程...")
                    bot.select_all_courses()
                else:
                    print("選課已取消")
                
                # 保持瀏覽器開啟讓用戶查看結果
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
    print("🚀 選課功能專門測試")
    print("=" * 50)
    
    try:
        success = test_course_selection_only()
        
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

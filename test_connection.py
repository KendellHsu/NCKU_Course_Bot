#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡化測試：連接到現有 Arc 瀏覽器並測試網頁讀取
"""

from course_bot import NCKUCourseBot
import time

def test_existing_browser_connection():
    """測試連接到現有瀏覽器"""
    print("=== 測試連接到現有 Chrome 瀏覽器 ===")
    print("⚠️  請確保你已經在 Chrome 瀏覽器中登入選課系統")
    print("⚠️  並且已經導航到選課頁面")
    
    input("準備好後按 Enter 繼續...")
    
    try:
        # 建立機器人實例
        bot = NCKUCourseBot()
        print("✅ 成功建立機器人實例")
        
        # 嘗試連接到現有瀏覽器
        print("正在嘗試連接到現有瀏覽器...")
        if bot.connect_to_existing_browser():
            print("✅ 成功連接到現有瀏覽器")
            
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
            print("❌ 無法連接到現有瀏覽器")
            print("可能的原因：")
            print("1. Chrome 瀏覽器沒有開啟調試模式")
            print("2. 瀏覽器版本不支援遠端調試")
            print("3. 防火牆阻擋了連接")
            return False
            
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")
        return False

def main():
    """主函數"""
    print("🚀 測試連接到現有 Chrome 瀏覽器")
    print("=" * 50)
    
    try:
        success = test_existing_browser_connection()
        
        if success:
            print("\n🎉 測試完成！")
            print("程式成功連接到瀏覽器並讀取了網頁資訊")
        else:
            print("\n⚠️  測試失敗，請檢查上述錯誤訊息")
            
    except KeyboardInterrupt:
        print("\n\n測試被使用者中斷")
    except Exception as e:
        print(f"\n❌ 測試過程中發生未預期的錯誤: {e}")

if __name__ == "__main__":
    main()

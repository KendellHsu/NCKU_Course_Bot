# course_bot.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import json
import logging

class NCKUCourseBot:
    def __init__(self, config_file="config.json"):
        self.config = self.load_config(config_file)
        self.driver = None
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('course_bot.log'),
                logging.StreamHandler()
            ]
        )
        
    def load_config(self, config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                logging.info(f"成功載入配置檔案: {config}")
                return config
        except FileNotFoundError:
            logging.warning(f"找不到配置檔案 {config_file}，使用預設配置")
            return self.create_default_config()
        except Exception as e:
            logging.error(f"載入配置檔案時發生錯誤: {e}")
            return self.create_default_config()
    
    def create_default_config(self):
        default_config = {
            "course_selection_url": "https://course.ncku.edu.tw/index.php?c=cos21322",
            "courses": [
                {
                    "department_code": "M1",
                    "course_number": "023",
                    "course_name": "射頻振盪器電路設計專論"
                }
            ]
        }
        
        try:
            with open("config.json", 'w', encoding='utf-8') as f:
                json.dump(default_config, f, ensure_ascii=False, indent=2)
            logging.info("已創建預設配置檔案")
        except Exception as e:
            logging.error(f"創建配置檔案時發生錯誤: {e}")
        
        return default_config
    
    def connect_to_existing_browser(self):
        """連接到已經開啟的Arc瀏覽器"""
        try:
            logging.info("正在嘗試連接到已開啟的Arc瀏覽器...")
            
            # 設定Chrome選項以連接到現有瀏覽器
            chrome_options = Options()
            chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            
            # 嘗試連接到現有瀏覽器
            self.driver = webdriver.Chrome(options=chrome_options)
            
            # 檢查是否成功連接
            current_url = self.driver.current_url
            logging.info(f"成功連接到現有瀏覽器，當前頁面: {current_url}")
            
            return True
            
        except Exception as e:
            logging.error(f"無法連接到現有瀏覽器: {e}")
            return False
    
    def start_new_browser(self):
        """開啟新的Arc瀏覽器"""
        try:
            logging.info("正在開啟新的Arc瀏覽器...")
            
            # 設定Arc瀏覽器路徑 (macOS)
            arc_path = "/Applications/Arc.app/Contents/MacOS/Arc"
            
            chrome_options = Options()
            chrome_options.binary_location = arc_path
            
            # Arc瀏覽器特定的選項
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # 設定使用者代理
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            
            # 隱藏自動化特徵
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.driver.implicitly_wait(10)
            logging.info("✅ 新的Arc瀏覽器已開啟")
            
            return True
            
        except Exception as e:
            logging.error(f"開啟新瀏覽器時發生錯誤: {e}")
            return False
    
    def setup_driver(self):
        """設定瀏覽器驅動，優先嘗試連接現有瀏覽器"""
        # 首先嘗試連接到現有瀏覽器
        if self.connect_to_existing_browser():
            logging.info("✅ 成功連接到現有瀏覽器")
            return True
        
        # 如果無法連接，則開啟新瀏覽器
        logging.info("無法連接到現有瀏覽器，正在開啟新瀏覽器...")
        if self.start_new_browser():
            logging.info("✅ 新瀏覽器開啟成功")
            return True
        
        # 如果都失敗，拋出異常
        raise Exception("無法設定瀏覽器驅動")
        
    def check_login_status(self):
        """檢查是否已經登入"""
        try:
            logging.info(f"正在導航到選課頁面: {self.config['course_selection_url']}")
            
            # 導航到選課頁面
            self.driver.get(self.config["course_selection_url"])
            time.sleep(3)
            
            # 檢查頁面標題或特定元素來判斷是否已登入
            page_title = self.driver.title
            logging.info(f"頁面標題: {page_title}")
            
            # 如果頁面包含登入相關元素，表示未登入
            if "登入" in page_title or "login" in page_title.lower():
                logging.error("尚未登入，請先手動登入選課系統")
                return False
            
            # 檢查是否能看到課程列表
            try:
                logging.info("正在檢查課程表格...")
                # 等待課程表格出現
                course_table = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "table"))
                )
                logging.info("✅ 成功載入選課頁面，已登入")
                return True
            except Exception as e:
                logging.error(f"無法找到課程表格: {e}")
                logging.error("可能未登入或頁面結構有問題")
                return False
                
        except Exception as e:
            logging.error(f"檢查登入狀態時發生錯誤: {e}")
            return False
    
    def check_course_exists(self, course):
        """檢查特定課程是否存在於頁面中"""
        try:
            logging.info(f"正在檢查課程: {course['course_name']}")
            
            # 嘗試多種方式查找課程
            course_found = False
            
            # 方法1: 通過課程名稱查找
            try:
                course_name_xpath = f"//td[contains(text(), '{course['course_name']}')]"
                course_element = self.driver.find_element(By.XPATH, course_name_xpath)
                logging.info(f"✅ 找到課程: {course['course_name']}")
                course_found = True
                
                # 獲取該行的完整資訊
                row = course_element.find_element(By.XPATH, "./..")
                row_text = row.text
                logging.info(f"課程行資訊: {row_text}")
                
            except Exception as e:
                logging.info(f"通過課程名稱未找到: {course['course_name']}")
            
            # 方法2: 通過系所代碼和課程編號查找
            if not course_found:
                try:
                    course_code_xpath = f"//td[contains(text(), '{course['department_code']}') and contains(text(), '{course['course_number']}')]"
                    course_element = self.driver.find_element(By.XPATH, course_code_xpath)
                    logging.info(f"✅ 通過代碼找到課程: {course['department_code']}-{course['course_number']}")
                    course_found = True
                    
                    # 獲取該行的完整資訊
                    row = course_element.find_element(By.XPATH, "./..")
                    row_text = row.text
                    logging.info(f"課程行資訊: {row_text}")
                    
                except Exception as e:
                    logging.info(f"通過代碼未找到: {course['department_code']}-{course['course_number']}")
            
            # 方法3: 檢查是否有選課按鈕
            if course_found:
                try:
                    # 查找該課程行中的選課按鈕
                    select_button_xpath = f"//td[contains(text(), '{course['course_name']}')]/..//button[contains(text(), '選課')]"
                    select_button = self.driver.find_element(By.XPATH, select_button_xpath)
                    logging.info(f"✅ 找到選課按鈕: {course['course_name']}")
                    
                    # 檢查按鈕狀態
                    button_text = select_button.text
                    button_enabled = select_button.is_enabled()
                    logging.info(f"選課按鈕文字: {button_text}, 是否可用: {button_enabled}")
                    
                except Exception as e:
                    logging.warning(f"未找到選課按鈕: {course['course_name']}")
            
            return course_found
            
        except Exception as e:
            logging.error(f"檢查課程 {course['course_name']} 時發生錯誤: {e}")
            return False
    
    def check_all_courses(self):
        """檢查所有配置的課程"""
        logging.info("開始檢查所有配置的課程...")
        
        if 'courses' not in self.config or not self.config['courses']:
            logging.warning("配置檔案中沒有課程資訊")
            return
        
        total_courses = len(self.config['courses'])
        found_courses = 0
        
        print(f"\n=== 課程檢查結果 ===")
        print(f"總共需要檢查 {total_courses} 門課程")
        
        for i, course in enumerate(self.config['courses'], 1):
            print(f"\n[{i}/{total_courses}] 檢查課程: {course['course_name']}")
            print(f"系所代碼: {course['department_code']}, 課程編號: {course['course_number']}")
            
            if self.check_course_exists(course):
                found_courses += 1
                print(f"✅ 課程存在")
            else:
                print(f"❌ 課程不存在")
        
        print(f"\n=== 檢查完成 ===")
        print(f"找到 {found_courses}/{total_courses} 門課程")
        
        if found_courses == total_courses:
            print("🎉 所有課程都已找到！")
        else:
            print("⚠️  部分課程未找到，請檢查課程資訊或選課時間")
    
    def test_course_check(self):
        """測試課程檢查功能"""
        try:
            logging.info("開始測試課程檢查功能...")
            
            self.setup_driver()
            
            # 檢查登入狀態
            if not self.check_login_status():
                logging.error("登入檢查失敗，無法繼續檢查課程")
                return
            
            # 檢查所有課程
            self.check_all_courses()
            
            # 保持瀏覽器開啟一段時間，讓你可以查看結果
            print("\n按Enter鍵關閉瀏覽器...")
            input()
            
        except Exception as e:
            logging.error(f"測試過程中發生錯誤: {e}")
            print(f"\n❌ 測試過程中發生錯誤: {e}")
        finally:
            if self.driver:
                logging.info("正在關閉瀏覽器...")
                self.driver.quit()
                logging.info("瀏覽器已關閉")

def main():
    print("=== 選課系統課程檢查測試 ===")
    print("請確保你已經在Arc瀏覽器中登入選課系統")
    print("然後按Enter鍵開始測試...")
    
    try:
        input()
        print("開始執行測試...")
        
        bot = NCKUCourseBot()
        bot.test_course_check()
        
    except KeyboardInterrupt:
        print("\n程式被使用者中斷")
    except Exception as e:
        print(f"\n❌ 主程式執行錯誤: {e}")
        logging.error(f"主程式執行錯誤: {e}")

if __name__ == "__main__":
    main()
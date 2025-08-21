# course_bot.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import json
import logging
import os

# 导入自定义模块
try:
    from captcha_solver import CaptchaSolver
    from env_config import EnvConfig
    CAPTCHA_SOLVER_AVAILABLE = True
except ImportError as e:
    print(f"警告：无法导入验证码识别模块: {e}")
    print("将使用手动输入验证码模式")
    CAPTCHA_SOLVER_AVAILABLE = False

class NCKUCourseBot:
    def __init__(self, config_file="config.json"):
        self.config = self.load_config(config_file)
        self.driver = None
        self.setup_logging()
        
        # 初始化验证码识别器
        self.captcha_solver = None
        if CAPTCHA_SOLVER_AVAILABLE:
            try:
                # 优先从环境变量获取API密钥
                if 'OPENAI_API_KEY' in os.environ:
                    api_key = os.environ['OPENAI_API_KEY']
                elif 'openai_config' in self.config and self.config['openai_config'].get('api_key'):
                    api_key = self.config['openai_config']['api_key']
                else:
                    api_key = None
                
                if api_key:
                    model = self.config.get('openai_config', {}).get('model', 'gpt-5-mini')
                    self.captcha_solver = CaptchaSolver(api_key, model)
                    logging.info("✅ 验证码识别器初始化成功")
                else:
                    logging.warning("未找到OpenAI API密钥，将使用手动输入验证码模式")
            except Exception as e:
                logging.error(f"初始化验证码识别器时发生错误: {e}")
                self.captcha_solver = None
        
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
    
    def auto_login(self):
        """自動登入選課系統"""
        try:
            logging.info("開始自動登入流程...")
            
            # 檢查配置中是否有登入資訊
            if 'login_info' not in self.config:
                logging.error("配置檔案中缺少登入資訊")
                return False
            
            username = self.config['login_info'].get('username')
            password = self.config['login_info'].get('password')
            
            if not username or not password:
                logging.error("配置檔案中的登入資訊不完整")
                return False
            
            logging.info(f"使用帳號: {username}")
            
            # 導航到登入頁面
            login_url = self.config['course_selection_url']
            logging.info(f"導航到登入頁面: {login_url}")
            self.driver.get(login_url)
            
            # 等待頁面載入
            time.sleep(2)
            
            # 嘗試多種方式查找登入表單元素
            username_input = None
            password_input = None
            
            # 查找帳號輸入框（使用精確的選擇器）
            username_selectors = [
                "//input[@name='user_id']",  # 最精確：根據你提供的 HTML
                "//input[@id='user_id']",    # 備用：ID 選擇器
                "//input[@placeholder='學號/識別證號']",  # 備用：placeholder
                "//input[@class='form-control acpwd_input rwd_input1_3'][@type='text']",  # 備用：class + type
                "//input[@type='text'][@maxlength='9']",  # 備用：type + maxlength
                "//input[@type='text'][1]"  # 最後備用：第一個文字輸入框
            ]
            
            for selector in username_selectors:
                try:
                    username_input = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    logging.info(f"找到帳號輸入框: {selector}")
                    break
                except:
                    continue
            
            # 查找密碼輸入框（使用精確的選擇器）
            password_selectors = [
                "//input[@name='passwd']",  # 最精確：根據你提供的 HTML
                "//input[@id='passwd']",    # 備用：ID 選擇器
                "//input[@placeholder='同成功入口']",  # 備用：placeholder
                "//input[@class='form-control acpwd_input rwd_input1_3'][@type='password']",  # 備用：class + type
                "//input[@type='password']"  # 最後備用：密碼類型輸入框
            ]
            
            for selector in password_selectors:
                try:
                    password_input = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    logging.info(f"找到密碼輸入框: {selector}")
                    break
                except:
                    continue
            
            if not username_input or not password_input:
                logging.error("無法找到登入表單元素")
                return False
            
            # 填入帳號密碼
            logging.info("填入帳號密碼...")
            username_input.clear()
            username_input.send_keys(username)
            password_input.clear()
            password_input.send_keys(password)
            
            logging.info("帳號密碼已填入，嘗試自動識別驗證碼...")
            print(f"\n📝 帳號密碼已自動填入")
            print(f"   帳號: {username}")
            print(f"   密碼: {'*' * len(password)}")
            
            # 尝试自动识别验证码
            if self.captcha_solver and self.config.get('verification', {}).get('auto_captcha', True):
                print("🤖 正在使用AI自动识别验证码...")
                
                # 等待页面加载完成
                time.sleep(2)
                
                # 自动识别并填写验证码
                if self.captcha_solver.auto_solve_captcha(self.driver):
                    print("✅ AI成功识别并填写验证码！")
                    logging.info("AI自动识别验证码成功")
                else:
                    print("❌ AI识别验证码失败，请手动输入")
                    logging.warning("AI识别验证码失败，切换到手动模式")
                    print("⏰ 請在瀏覽器中輸入登入驗證碼，然後按 Enter 繼續...")
                    input()
            else:
                print("⏰ 請在瀏覽器中輸入登入驗證碼，然後按 Enter 繼續...")
                input()
            
            # 查找登入按鈕（使用精確的選擇器）
            login_button = None
            login_selectors = [
                "//button[@id='submit_by_acpw']",  # 最精確：根據你提供的 HTML
                "//button[@type='submit'][@class='btn btn-default']",  # 備用：type + class
                "//button[contains(@class, 'btn-default')]",  # 備用：class
                "//button[@type='submit']",  # 備用：type
                "//button[contains(text(), '登入')]",  # 備用：文字內容
                "//button[contains(text(), 'Login')]"  # 最後備用：英文文字
            ]
            
            for selector in login_selectors:
                try:
                    login_button = self.driver.find_element(By.XPATH, selector)
                    if login_button:
                        logging.info(f"找到登入按鈕: {selector}")
                        break
                except:
                    continue
            
            if not login_button:
                logging.error("無法找到登入按鈕")
                return False
            
            # 點擊登入按鈕
            logging.info("點擊登入按鈕...")
            login_button.click()
            
            # 等待登入完成
            logging.info("等待登入完成...")
            time.sleep(5)
            
            # 檢查登入狀態
            current_url = self.driver.current_url
            page_title = self.driver.title
            logging.info(f"登入後頁面標題: {page_title}")
            logging.info(f"登入後頁面URL: {current_url}")
            
            # 檢查是否還在登入頁面
            if "登入" in page_title or "login" in page_title.lower():
                logging.error("仍在登入頁面，登入可能失敗")
                return False
            
            # 登入成功，強制導向選課頁面
            logging.info("✅ 登入成功！正在導向選課頁面...")
            try:
                self.driver.get(self.config["course_selection_url"])
                time.sleep(5)  # 等待頁面載入
                
                # 確認已導向選課頁面
                final_url = self.driver.current_url
                final_title = self.driver.title
                logging.info(f"導向後頁面標題: {final_title}")
                logging.info(f"導向後頁面URL: {final_url}")
                
                if "cos21322" in final_url:
                    logging.info("✅ 成功導向選課頁面")
                    return True
                else:
                    logging.warning("導向選課頁面可能失敗")
                    return False
                    
            except Exception as e:
                logging.error(f"導向選課頁面時發生錯誤: {e}")
                return False
                
        except Exception as e:
            logging.error(f"自動登入過程中發生錯誤: {e}")
            return False
    
    def connect_to_existing_browser(self):
        """連接到已經開啟的Chrome瀏覽器"""
        try:
            logging.info("正在嘗試連接到已開啟的Chrome瀏覽器...")
            
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
            logging.info("连接失败，将返回 False 并继续执行")
            print(f"⚠️  连接现有浏览器失败: {e}")
            print("   程序将尝试开启新浏览器...")
            return False
    
    def start_new_browser(self):
        """開啟新的Chrome瀏覽器"""
        try:
            logging.info("正在開啟新的Chrome瀏覽器...")
            
            chrome_options = Options()
            
            # Chrome瀏覽器選項
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # 設定使用者代理
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # 可選：設定視窗大小
            chrome_options.add_argument("--window-size=1920,1080")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            
            # 隱藏自動化特徵
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.driver.implicitly_wait(10)
            logging.info("✅ 新的Chrome瀏覽器已開啟")
            
            return True
            
        except Exception as e:
            logging.error(f"開啟新瀏覽器時發生錯誤: {e}")
            return False
    
    def setup_driver(self):
        """設定瀏覽器驅動，直接開啟新瀏覽器"""
        logging.info("=== 开始设置浏览器驱动 ===")
        print("=== 开始设置浏览器驱动 ===")
        
        # 直接開啟新瀏覽器
        logging.info("正在開啟新的Chrome瀏覽器...")
        print("🚀 正在開啟新的Chrome瀏覽器...")
        if self.start_new_browser():
            logging.info("✅ 新瀏覽器開啟成功")
            print("✅ 新瀏覽器開啟成功")
            return True
        
        # 如果開啟失敗，拋出異常
        logging.error("無法開啟新瀏覽器")
        print("❌ 無法開啟新瀏覽器")
        raise Exception("無法設定瀏覽器驅動")
        
    def check_login_status(self):
        """檢查是否已經登入並在正確的選課頁面"""
        try:
            # 检查浏览器驱动是否设置
            if not self.driver:
                logging.error("浏览器驱动未设置，无法检查登录状态")
                return False
                
            current_url = self.driver.current_url
            page_title = self.driver.title
            logging.info(f"當前頁面標題: {page_title}")
            logging.info(f"當前頁面URL: {current_url}")
            
            # 檢查是否在登入頁面
            if "登入" in page_title or "login" in page_title.lower() or "登入" in current_url:
                logging.info("當前在登入頁面，需要登入")
                return False
            
            # 檢查是否在選課頁面（URL 包含 cos21322）
            if "cos21322" not in current_url:
                logging.info("當前不在選課頁面，需要導航")
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
    
    def check_login_status_simple(self):
        """簡化的登入狀態檢查 - 只檢查是否不在登入頁面"""
        try:
            current_url = self.driver.current_url
            page_title = self.driver.title
            logging.info(f"簡化檢查 - 頁面標題: {page_title}")
            logging.info(f"簡化檢查 - 頁面URL: {current_url}")
            
            # 簡單檢查：只要不在登入頁面就認為登入成功
            if "登入" in page_title or "login" in page_title.lower():
                logging.info("簡化檢查：仍在登入頁面")
                return False
            else:
                logging.info("簡化檢查：已離開登入頁面，可能登入成功")
                return True
                
        except Exception as e:
            logging.error(f"簡化登入狀態檢查時發生錯誤: {e}")
            return False
    
    def check_course_exists(self, course):
        """檢查特定課程是否存在於頁面中"""
        try:
            logging.info(f"正在檢查課程: {course['course_name']}")
            
            # 嘗試多種方式查找課程
            course_found = False
            course_row = None
            
            # 方法1: 通過課程名稱查找
            try:
                course_name_xpath = f"//td[contains(text(), '{course['course_name']}')]"
                course_element = self.driver.find_element(By.XPATH, course_name_xpath)
                logging.info(f"✅ 找到課程: {course['course_name']}")
                course_found = True
                
                # 獲取該行的完整資訊
                course_row = course_element.find_element(By.XPATH, "./..")
                row_text = course_row.text
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
                    course_row = course_element.find_element(By.XPATH, "./..")
                    row_text = course_row.text
                    logging.info(f"課程行資訊: {row_text}")
                    
                except Exception as e:
                    logging.info(f"通過代碼未找到: {course['department_code']}-{course['course_number']}")
            
            # 方法3: 檢查是否有選課按鈕
            if course_found and course_row:
                try:
                    # 查找該課程行中的選課按鈕
                    select_button_xpath = f".//button[contains(text(), '選課')]"
                    select_button = course_row.find_element(By.XPATH, select_button_xpath)
                    logging.info(f"✅ 找到選課按鈕: {course['course_name']}")
                    
                    # 檢查按鈕狀態
                    button_text = select_button.text
                    button_enabled = select_button.is_enabled()
                    logging.info(f"選課按鈕文字: {button_text}, 是否可用: {button_enabled}")
                    
                    # 將課程行和選課按鈕資訊保存到課程物件中
                    course['course_row'] = course_row
                    course['select_button'] = select_button
                    
                except Exception as e:
                    logging.warning(f"未找到選課按鈕: {course['course_name']}")
            
            return course_found
            
        except Exception as e:
            logging.error(f"檢查課程 {course['course_name']} 時發生錯誤: {e}")
            return False
    
    def select_course(self, course):
        """選課功能：點擊選課按鈕，等待驗證碼輸入，點擊確認"""
        try:
            logging.info(f"開始選課流程: {course['course_name']}")
            
            # 檢查是否有選課按鈕
            if 'select_button' not in course:
                logging.error(f"課程 {course['course_name']} 沒有選課按鈕")
                return False
            
            select_button = course['select_button']
            
            # 檢查按鈕是否可用
            if not select_button.is_enabled():
                logging.warning(f"選課按鈕不可用: {course['course_name']}")
                return False
            
            # 點擊選課按鈕
            logging.info(f"點擊選課按鈕: {course['course_name']}")
            select_button.click()
            
            # 等待頁面變化並尋找驗證碼相關元素
            logging.info("等待驗證碼相關元素出現...")
            try:
                # 等待一下讓頁面載入
                time.sleep(1)
                
                # 檢查是否出現了驗證碼輸入框或其他相關元素
                verification_found = False
                
                # 嘗試多種可能的驗證碼輸入框定位方式
                verification_input = None
                
                # 方法1: 通過確切的 name 屬性查找（根據提供的 HTML）
                try:
                    verification_input = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, "//input[@name='cos_qry_confirm_validation_code']"))
                    )
                    logging.info("找到驗證碼輸入框 (方法1: 確切name)")
                    verification_found = True
                except:
                    pass
                
                # 方法2: 通過確切的 id 屬性查找
                if not verification_input:
                    try:
                        verification_input = WebDriverWait(self.driver, 3).until(
                            EC.presence_of_element_located((By.XPATH, "//input[@id='cos_qry_confirm_validation_code']"))
                        )
                        logging.info("找到驗證碼輸入框 (方法2: 確切id)")
                        verification_found = True
                    except:
                        pass
                
                # 方法3: 通過 placeholder 屬性查找
                if not verification_input:
                    try:
                        verification_input = WebDriverWait(self.driver, 3).until(
                            EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, '請輸入驗證碼')]"))
                        )
                        logging.info("找到驗證碼輸入框 (方法3: placeholder)")
                        verification_found = True
                    except:
                        pass
                
                # 方法4: 通過 class 和 maxlength 屬性查找
                if not verification_input:
                    try:
                        verification_input = WebDriverWait(self.driver, 3).until(
                            EC.presence_of_element_located((By.XPATH, "//input[@class='form-control' and @maxlength='4']"))
                        )
                        logging.info("找到驗證碼輸入框 (方法4: class+maxlength)")
                        verification_found = True
                    except:
                        pass
                
                # 方法5: 通過包含驗證碼文字的標籤查找
                if not verification_input:
                    try:
                        verification_input = WebDriverWait(self.driver, 3).until(
                            EC.presence_of_element_located((By.XPATH, "//input[preceding-sibling::*[contains(text(), '驗證碼')] or following-sibling::*[contains(text(), '驗證碼')]]"))
                        )
                        logging.info("找到驗證碼輸入框 (方法5: 文字)")
                        verification_found = True
                    except:
                        pass
                
                # 方法6: 查找任何新出現的輸入框（4位數驗證碼）
                if not verification_input:
                    try:
                        verification_input = WebDriverWait(self.driver, 3).until(
                            EC.presence_of_element_located((By.XPATH, "//input[@type='text' and @maxlength='4']"))
                        )
                        logging.info("找到驗證碼輸入框 (方法6: 4位數)")
                        verification_found = True
                    except:
                        pass
                
                # 方法7: 查找 modal 中的輸入框
                if not verification_input:
                    try:
                        verification_input = WebDriverWait(self.driver, 3).until(
                            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'modal')]//input[@type='text']"))
                        )
                        logging.info("找到驗證碼輸入框 (方法7: modal)")
                        verification_found = True
                    except:
                        pass
                
                # 方法8: 查找任何新出現的文字輸入框
                if not verification_input:
                    try:
                        # 在modal框中尋找輸入框
                        modal_inputs = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'modal-body')]//input[@type='text']")
                        if modal_inputs:
                            verification_input = modal_inputs[0]  # 取第一個
                            logging.info("找到驗證碼輸入框 (方法8: modal body)")
                            verification_found = True
                    except:
                        pass
                
                # 如果沒找到驗證碼輸入框，檢查是否有其他相關元素
                if not verification_found:
                    try:
                        # 檢查是否有包含驗證碼文字的元素
                        captcha_element = self.driver.find_element(By.XPATH, "//*[contains(text(), '驗證碼') or contains(text(), 'captcha')]")
                        if captcha_element:
                            logging.info("發現驗證碼相關元素，但未找到輸入框")
                            print("⚠️  發現驗證碼相關元素，請手動處理驗證碼")
                            verification_found = True
                    except:
                        pass
                
                if not verification_found:
                    logging.warning("未找到驗證碼相關元素，可能不需要驗證碼或頁面結構不同")
                    print("⚠️  未找到驗證碼輸入框，可能不需要驗證碼")
                    # 直接嘗試尋找確認按鈕
                    input("請檢查頁面是否需要其他操作，然後按 Enter 繼續...")
                else:
                    # 尝试自动识别验证码
                    if self.captcha_solver and self.config.get('verification', {}).get('auto_captcha', True):
                        print(f"\n🤖 正在使用AI自动识别课程 '{course['course_name']}' 的验证码...")
                        
                        # 等待页面稳定
                        time.sleep(1)
                        
                        # 自动识别并填写验证码
                        if self.captcha_solver.auto_solve_captcha(self.driver):
                            print("✅ AI成功识别并填写验证码！")
                            logging.info(f"AI自动识别课程 {course['course_name']} 验证码成功")
                        else:
                            print("❌ AI识别验证码失败，请手动输入")
                            logging.warning(f"AI识别课程 {course['course_name']} 验证码失败，切换到手动模式")
                            print(f"📝 請在瀏覽器中為課程 '{course['course_name']}' 輸入驗證碼")
                            print("⏰ 程式會等待 5 秒讓你輸入驗證碼...")
                            time.sleep(5)
                    else:
                        # 如果找到驗證碼相關元素，給用戶時間輸入
                        print(f"\n📝 請在瀏覽器中為課程 '{course['course_name']}' 輸入驗證碼")
                        print("⏰ 程式會等待 2 秒讓你輸入驗證碼...")
                        print("🔍 如果看到驗證碼輸入框，請立即輸入驗證碼")
                        
                        # 等待 2 秒讓使用者輸入驗證碼
                        time.sleep(2)
                    
                    print("⏱️  時間到！程式將嘗試點擊確認按鈕...")
                
                # 查找確認按鈕
                confirm_button = None
                
                # 嘗試多種可能的確認按鈕定位方式
                try:
                    # 方法1: 通過確切的 class 名稱查找（根據提供的 HTML）
                    confirm_button = self.driver.find_element(By.XPATH, "//button[contains(@class, 'addcourse_confirm_save_button')]")
                    logging.info("找到確認按鈕 (方法1: 特定class)")
                except:
                    pass
                
                # 方法2: 通過文字內容查找
                if not confirm_button:
                    try:
                        confirm_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '確定') or contains(text(), '確認') or contains(text(), '提交')]")
                        logging.info("找到確認按鈕 (方法2: 文字)")
                    except:
                        pass
                
                # 方法3: 通過 class 包含 confirm 查找
                if not confirm_button:
                    try:
                        confirm_button = self.driver.find_element(By.XPATH, "//button[contains(@class, 'confirm') or contains(@class, 'save')]")
                        logging.info("找到確認按鈕 (方法3: 通用class)")
                    except:
                        pass
                
                # 方法4: 通過按鈕類型和樣式查找（btn btn-danger）
                if not confirm_button:
                    try:
                        confirm_button = self.driver.find_element(By.XPATH, "//button[@type='button' and contains(@class, 'btn-danger')]")
                        logging.info("找到確認按鈕 (方法4: 按鈕樣式)")
                    except:
                        pass
                
                # 方法5: 通過 data-dismiss 屬性查找
                if not confirm_button:
                    try:
                        confirm_button = self.driver.find_element(By.XPATH, "//button[@data-dismiss='modal' and contains(text(), '確定')]")
                        logging.info("找到確認按鈕 (方法5: modal)")
                    except:
                        pass
                
                if not confirm_button:
                    logging.error("無法找到確認按鈕")
                    return False
                
                # 點擊確認按鈕
                logging.info("點擊確認按鈕完成選課")
                
                # 嘗試滾動到按鈕位置
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", confirm_button)
                    time.sleep(1)
                except:
                    pass
                
                confirm_button.click()
                
                # 等待選課結果
                time.sleep(3)
                
                # 檢查並關閉可能的彈出視窗
                try:
                    # 查找並關閉可能的彈出視窗
                    close_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@class, 'close') or contains(@data-dismiss, 'modal')]")
                    for btn in close_buttons:
                        if btn.is_displayed():
                            btn.click()
                            time.sleep(1)
                            break
                except:
                    pass
                
                # 檢查選課是否成功
                try:
                    # 檢查是否有成功訊息
                    success_message = self.driver.find_element(By.XPATH, "//*[contains(text(), '成功') or contains(text(), '完成') or contains(text(), '已選')]")
                    logging.info(f"✅ 選課成功: {course['course_name']}")
                    print(f"🎉 課程 '{course['course_name']}' 選課成功！")
                    return True
                except:
                    # 檢查是否有錯誤訊息
                    try:
                        error_message = self.driver.find_element(By.XPATH, "//*[contains(text(), '失敗') or contains(text(), '錯誤') or contains(text(), '已滿')]")
                        logging.warning(f"選課失敗: {course['course_name']} - {error_message.text}")
                        print(f"❌ 課程 '{course['course_name']}' 選課失敗")
                        return False
                    except:
                        logging.info(f"選課完成，但無法確定結果: {course['course_name']}")
                        print(f"⚠️  課程 '{course['course_name']}' 選課完成，請檢查結果")
                        return True
                
            except Exception as e:
                logging.error(f"選課過程中發生錯誤: {e}")
                return False
                
        except Exception as e:
            logging.error(f"選課 {course['course_name']} 時發生錯誤: {e}")
            return False
    
    def select_all_courses(self):
        """選取所有配置的課程"""
        logging.info("開始選取所有配置的課程...")
        
        if 'courses' not in self.config or not self.config['courses']:
            logging.warning("配置檔案中沒有課程資訊")
            return
        
        total_courses = len(self.config['courses'])
        selected_courses = 0
        
        print(f"\n=== 開始選課 ===")
        print(f"總共需要選取 {total_courses} 門課程")
        
        for i, course in enumerate(self.config['courses'], 1):
            print(f"\n[{i}/{total_courses}] 選取課程: {course['course_name']}")
            print(f"系所代碼: {course['department_code']}, 課程編號: {course['course_number']}")
            
            if self.select_course(course):
                selected_courses += 1
                print(f"✅ 選課成功")
            else:
                print(f"❌ 選課失敗")
        
        print(f"\n=== 選課完成 ===")
        print(f"成功選取 {selected_courses}/{total_courses} 門課程")
        
        if selected_courses == total_courses:
            print("🎉 所有課程都已成功選取！")
        else:
            print("⚠️  部分課程選課失敗，請檢查原因")
    
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
    
    def auto_course_selection(self):
        """自動選課功能 - 完整流程"""
        try:
            logging.info("開始自動選課流程...")
            print("🤖 開始自動選課流程...")
            
            # 步骤1: 设置浏览器驱动
            try:
                self.setup_driver()
                logging.info("✅ 浏览器驱动设置成功")
                print("✅ 浏览器驱动设置成功")
            except Exception as e:
                logging.error(f"设置浏览器驱动失败: {e}")
                print(f"❌ 无法设置浏览器驱动: {e}")
                return
            
            # 检查浏览器驱动是否设置成功
            if not self.driver:
                logging.error("浏览器驱动未设置，无法继续")
                print("❌ 浏览器驱动未设置，无法继续")
                return
            
            # 步骤2: 检查是否需要登录
            print("\n📋 步骤1: 检查登录状态...")
            try:
                if self.check_login_status():
                    print("✅ 已登录，跳过登录步骤")
                    logging.info("用户已登录，跳过登录步骤")
                else:
                    print("🔐 需要登录，开始自动登录...")
                    if not self.auto_login():
                        print("❌ 自动登录失败")
                        logging.error("自动登录失败")
                        return
                    print("✅ 自动登录成功")
                    
            except Exception as e:
                print("🔐 登录状态检查失败，尝试自动登录...")
                logging.warning(f"登录状态检查失败: {e}")
                if not self.auto_login():
                    print("❌ 自动登录失败")
                    logging.error("自动登录失败")
                    return
                print("✅ 自动登录成功")
            
            # 步骤3: 检查所有课程
            print("\n📚 步骤2: 检查课程...")
            self.check_all_courses()
            
            # 步骤4: 自动选课
            print("\n🎯 步骤3: 开始自动选课...")
            self.select_all_courses()
            
            # 保持瀏覽器開啟一段時間，讓你可以查看結果
            print("\n🎉 自动选课流程完成！")
            print("按Enter鍵關閉瀏覽器...")
            input()
            
        except Exception as e:
            logging.error(f"自动选课过程中发生错误: {e}")
            print(f"\n❌ 自动选课过程中发生错误: {e}")
        finally:
            if self.driver:
                logging.info("正在關閉瀏覽器...")
                print("正在關閉瀏覽器...")
                self.driver.quit()
                logging.info("瀏覽器已關閉")
                print("瀏覽器已關閉")
                
    def test_course_check(self):
        """測試課程檢查功能"""
        try:
            logging.info("開始測試課程檢查功能...")
            
            # 尝试设置浏览器驱动
            try:
                self.setup_driver()
                logging.info("✅ 浏览器驱动设置成功")
            except Exception as e:
                logging.error(f"设置浏览器驱动失败: {e}")
                print(f"❌ 无法设置浏览器驱动: {e}")
                return
            
            # 檢查登入狀態
            try:
                if not self.check_login_status():
                    logging.error("登入檢查失敗，無法繼續檢查課程")
                    print("⚠️  登录检查失败，但程序将继续执行...")
                    # 不直接返回，让程序继续执行
            except Exception as e:
                logging.error(f"检查登录状态时发生错误: {e}")
                print(f"⚠️  检查登录状态时发生错误: {e}")
                print("程序将继续执行...")
            
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
    
    def close(self):
        """關閉瀏覽器"""
        try:
            if hasattr(self, 'driver') and self.driver:
                self.driver.quit()
                logging.info("✅ 瀏覽器已關閉")
        except Exception as e:
            logging.error(f"關閉瀏覽器時發生錯誤: {e}")

def main():
    print("=== NCKU 自動選課系統 ===")
    print("🤖 此程序将自动完成以下步骤：")
    print("   1. 开启浏览器")
    print("   2. 自动登录选课系统")
    print("   3. AI 自动识别验证码")
    print("   4. 检查目标课程")
    print("   5. 自动选课")
    print("\n⚙️ 配置信息：")
    print("   - 使用 GPT-4o-mini 模型")
    print("   - 自动验证码识别已启用")
    print("   - 智能浏览器管理")
    print("\n按Enter鍵開始自動選課...")
    
    try:
        input()
        print("🚀 開始執行自動選課...")
        
        bot = NCKUCourseBot()
        bot.auto_course_selection()
        
    except KeyboardInterrupt:
        print("\n程式被使用者中斷")
    except Exception as e:
        print(f"\n❌ 主程式執行錯誤: {e}")
        logging.error(f"主程式執行錯誤: {e}")

if __name__ == "__main__":
    main()
"""
验证码识别模块
使用OpenAI API自动识别验证码图片
"""

import base64
import io
import logging
from PIL import Image
import openai
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CaptchaSolver:
    """验证码识别器"""
    
    def __init__(self, openai_api_key, model="gpt-4o-mini"):
        """
        初始化验证码识别器
        
        Args:
            openai_api_key (str): OpenAI API密钥
            model (str): 使用的模型名称
        """
        self.client = openai.OpenAI(api_key=openai_api_key)
        self.model = model
        self.logger = logging.getLogger(__name__)
    
    def capture_captcha_image(self, driver, captcha_selector=None):
        """
        截取验证码图片
        
        Args:
            driver: Selenium WebDriver实例
            captcha_selector (str, optional): 验证码图片的选择器
            
        Returns:
            PIL.Image.Image: 验证码图片对象，如果失败返回None
        """
        try:
            # 如果没有提供选择器，尝试自动查找验证码图片
            if not captcha_selector:
                captcha_selectors = [
                    "//img[contains(@src, 'verifycode')]",  # 根据src属性查找
                    "//img[contains(@src, 'captcha')]",     # 备用：captcha
                    "//img[contains(@class, 'captcha')]",   # 备用：class包含captcha
                    "//div[contains(@class, 'captcha')]//img",  # 备用：captcha容器中的图片
                    "//input[@name='code']/following-sibling::img",  # 备用：验证码输入框后的图片
                    "//input[@id='code']/following-sibling::img"     # 备用：验证码输入框后的图片
                ]
                
                captcha_img = None
                for selector in captcha_selectors:
                    try:
                        captcha_img = WebDriverWait(driver, 3).until(
                            EC.presence_of_element_located((By.XPATH, selector))
                        )
                        self.logger.info(f"找到验证码图片: {selector}")
                        break
                    except:
                        continue
                
                if not captcha_img:
                    self.logger.error("无法找到验证码图片")
                    return None
            else:
                captcha_img = driver.find_element(By.XPATH, captcha_selector)
            
            # 使用简单的元素截图方式
            try:
                screenshot = captcha_img.screenshot_as_png
                image = Image.open(io.BytesIO(screenshot))
                self.logger.info(f"成功截取验证码图片，尺寸: {image.size}, 模式: {image.mode}")
                
                # 保存图片用于调试（可选）
                try:
                    import time
                    debug_path = f"captcha_debug_{int(time.time())}.png"
                    image.save(debug_path)
                    self.logger.info(f"验证码图片已保存到: {debug_path}")
                except Exception as e:
                    self.logger.warning(f"无法保存调试图片: {e}")
                
                return image
                
            except Exception as e:
                self.logger.error(f"截图失败: {e}")
                return None
            
        except Exception as e:
            self.logger.error(f"截取验证码图片时发生错误: {e}")
            return None
    
    def capture_captcha_image_original(self, driver, captcha_selector=None):
        """
        截取原始验证码图片（不进行预处理）
        
        Args:
            driver: Selenium WebDriver实例
            captcha_selector (str, optional): 验证码图片的选择器
            
        Returns:
            PIL.Image.Image: 原始验证码图片对象，如果失败返回None
        """
        # 直接调用主要的截图方法
        return self.capture_captcha_image(driver, captcha_selector)
    
    def preprocess_image(self, image):
        """
        图像预处理：针对十六进制验证码进行优化
        
        Args:
            image (PIL.Image.Image): 原始验证码图片
            
        Returns:
            PIL.Image.Image: 预处理后的图片
        """
        try:
            self.logger.info("开始图像预处理...")
            
            # 转换为RGB模式
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # 尝试多种预处理策略，针对十六进制验证码优化
            processed_images = []
            
            # 策略1: 十六进制验证码专用预处理
            try:
                from PIL import ImageFilter, ImageEnhance
                
                # 转换为灰度图
                gray = image.convert('L')
                
                # 自适应阈值二值化
                threshold = self._get_adaptive_threshold(gray)
                binary = gray.point(lambda x: 255 if x > threshold else 0, '1')
                
                # 锐化处理
                sharpened = binary.filter(ImageFilter.UnsharpMask(radius=1, percent=200, threshold=2))
                
                # 对比度增强
                enhancer = ImageEnhance.Contrast(sharpened)
                enhanced = enhancer.enhance(2.0)
                
                # 转换为RGB
                final_image = enhanced.convert('RGB')
                processed_images.append(("十六进制专用预处理", final_image))
                self.logger.info("策略1完成：十六进制验证码专用预处理")
                
            except Exception as e:
                self.logger.warning(f"策略1失败: {e}")
            
            # 策略2: 字符分割优化
            try:
                from PIL import ImageFilter, ImageEnhance
                
                # 转换为灰度图
                gray = image.convert('L')
                
                # 高斯模糊去噪
                blurred = gray.filter(ImageFilter.GaussianBlur(radius=0.8))
                
                # 边缘检测
                edges = blurred.filter(ImageFilter.FIND_EDGES)
                
                # 锐化
                sharpened = edges.filter(ImageFilter.UnsharpMask(radius=0.5, percent=150, threshold=1))
                
                # 对比度增强
                enhancer = ImageEnhance.Contrast(sharpened)
                enhanced = enhancer.enhance(1.8)
                
                # 转换为RGB
                final_image = enhanced.convert('RGB')
                processed_images.append(("字符分割优化", final_image))
                self.logger.info("策略2完成：字符分割优化")
                
            except Exception as e:
                self.logger.warning(f"策略2失败: {e}")
            
            # 策略3: 高对比度模式
            try:
                from PIL import ImageFilter, ImageEnhance, ImageOps
                
                # 转换为灰度图
                gray = image.convert('L')
                
                # 直方图均衡化
                equalized = ImageOps.equalize(gray)
                
                # 中值滤波去噪
                median_filtered = equalized.filter(ImageFilter.MedianFilter(size=3))
                
                # 锐化
                sharpened = median_filtered.filter(ImageFilter.UnsharpMask(radius=1, percent=180, threshold=2))
                
                # 对比度增强
                enhancer = ImageEnhance.Contrast(sharpened)
                enhanced = enhancer.enhance(2.2)
                
                # 亮度调整
                brightness_enhancer = ImageEnhance.Brightness(enhanced)
                final_image = brightness_enhancer.enhance(1.1)
                
                # 转换为RGB
                final_image = final_image.convert('RGB')
                processed_images.append(("高对比度模式", final_image))
                self.logger.info("策略3完成：高对比度模式")
                
            except Exception as e:
                self.logger.warning(f"策略3失败: {e}")
            
            # 策略4: 原始策略（作为备用）
            try:
                from PIL import ImageFilter, ImageEnhance
                
                # 应用高斯模糊来减少杂讯
                blurred = image.filter(ImageFilter.GaussianBlur(radius=0.5))
                
                # 锐化处理，增强边缘
                sharpened = blurred.filter(ImageFilter.UnsharpMask(radius=1, percent=150, threshold=3))
                
                # 对比度增强
                enhancer = ImageEnhance.Contrast(sharpened)
                enhanced = enhancer.enhance(1.5)
                
                # 亮度调整
                brightness_enhancer = ImageEnhance.Brightness(enhanced)
                final_image = brightness_enhancer.enhance(1.2)
                
                processed_images.append(("原始策略", final_image))
                self.logger.info("策略4完成：原始策略")
                
            except Exception as e:
                self.logger.warning(f"策略4失败: {e}")
            
            # 如果没有成功处理，返回原图
            if not processed_images:
                self.logger.warning("所有预处理策略都失败，返回原图")
                return image
            
            # 选择第一个成功的处理结果
            strategy_name, processed_image = processed_images[0]
            self.logger.info(f"使用预处理策略: {strategy_name}")
            
            return processed_image
            
        except Exception as e:
            self.logger.warning(f"图像预处理失败: {e}，返回原图")
            return image
    
    def _get_adaptive_threshold(self, gray_image):
        """
        计算自适应阈值
        
        Args:
            gray_image: 灰度图像
            
        Returns:
            int: 阈值
        """
        try:
            # 获取图像直方图
            histogram = gray_image.histogram()
            
            # 计算平均灰度值
            total_pixels = sum(histogram)
            weighted_sum = sum(i * count for i, count in enumerate(histogram))
            mean_gray = weighted_sum / total_pixels if total_pixels > 0 else 128
            
            # 使用Otsu方法计算阈值
            threshold = int(mean_gray * 0.7)  # 稍微降低阈值以保留更多字符信息
            
            return max(50, min(200, threshold))  # 限制阈值范围
            
        except Exception as e:
            self.logger.warning(f"自适应阈值计算失败: {e}")
            return 128  # 返回默认阈值
    
    def solve_captcha(self, image, max_retries=3):
        """
        使用OpenAI API识别验证码
        
        Args:
            image (PIL.Image.Image): 验证码图片
            max_retries (int): 最大重试次数
            
        Returns:
            str: 识别出的验证码文本，如果失败返回None
        """
        for attempt in range(max_retries):
            try:
                # 将图片转换为base64编码
                buffered = io.BytesIO()
                # 确保图片是RGB模式，转换为JPEG格式（OpenAI API 更兼容）
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                image.save(buffered, format="JPEG", quality=95)
                img_base64 = base64.b64encode(buffered.getvalue()).decode()
                
                self.logger.info(f"图片已转换为JPEG格式，base64长度: {len(img_base64)}")
                
                # 构建OpenAI API请求 - 针对4位十六进制验证码优化
                self.logger.info(f"正在调用OpenAI API，模型: {self.model}")
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": """你是一个专业的验证码识别专家。请快速识别图片中的4位十六进制验证码。

规则：
- 只输出4位十六进制字符（0-9, A-F）
- 忽略所有干扰元素
- 专注于字符形状特征
- 快速响应，不要解释

字符特征：
0: 圆形/椭圆，可能有中心点
1: 直线，可能有小钩
2: 弯曲顶部和底部
3: 两条水平线+弯曲中间
4: 两条垂直线+一条水平线
5: 弯曲顶部和底部
6: 圆形，顶部开口
7: 水平线+斜线
8: 两个圆形/椭圆
9: 圆形，底部开口
A: 三角形顶部+中间横线
B: 两条垂直线+两条水平线
C: 开口圆形
D: 圆形+一条垂直线
E: 垂直线+三条水平线
F: 垂直线+两条水平线

快速识别，只输出结果。"""
                        },
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "快速识别4位十六进制验证码。只输出结果，不要解释。"
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{img_base64}"
                                    }
                                }
                            ]
                        }
                    ]
                )
                
                self.logger.info(f"OpenAI API 响应状态: {response.choices[0].finish_reason}")
                self.logger.info(f"OpenAI API 响应ID: {response.id}")
                
                # 提取验证码文本
                captcha_text = response.choices[0].message.content.strip()
                
                # 记录原始响应内容用于调试
                self.logger.info(f"第{attempt + 1}次尝试 - 原始响应: '{captcha_text}'")
                
                # 针对4位十六进制验证码进行精确清理和验证
                cleaned_text = self._clean_hex_captcha(captcha_text)
                
                if cleaned_text:
                    self.logger.info(f"成功识别验证码: '{captcha_text}' -> 清理后: '{cleaned_text}'")
                    return cleaned_text
                else:
                    self.logger.warning(f"第{attempt + 1}次尝试：识别结果为空或无法清理")
                    self.logger.warning(f"原始内容: '{captcha_text}'")
                    
                    # 尝试其他清理方法
                    if captcha_text:
                        # 如果原始内容不为空，尝试提取任何可能的4位十六进制验证码
                        possible_codes = self._extract_hex_codes(captcha_text)
                        if possible_codes:
                            self.logger.info(f"找到可能的验证码: {possible_codes[0]}")
                            return possible_codes[0]
                    
            except Exception as e:
                self.logger.error(f"第{attempt + 1}次尝试识别验证码时发生错误: {e}")
                
            if attempt < max_retries - 1:
                self.logger.info(f"等待1秒后重试...")
                import time
                time.sleep(1)
        
        self.logger.error(f"验证码识别失败，已尝试{max_retries}次")
        return None
    
    def _clean_hex_captcha(self, text):
        """
        清理并验证4位十六进制验证码
        
        Args:
            text (str): 原始识别文本
            
        Returns:
            str: 清理后的4位十六进制验证码，如果无效返回None
        """
        import re
        
        # 移除所有非十六进制字符
        hex_chars = re.sub(r'[^0-9A-Fa-f]', '', text)
        
        # 转换为大写
        hex_chars = hex_chars.upper()
        
        # 验证是否为4位十六进制
        if len(hex_chars) == 4 and re.match(r'^[0-9A-F]{4}$', hex_chars):
            return hex_chars
        
        # 如果不是4位，尝试从更长的字符串中提取4位
        if len(hex_chars) > 4:
            # 尝试找到连续的4位十六进制
            for i in range(len(hex_chars) - 3):
                candidate = hex_chars[i:i+4]
                if re.match(r'^[0-9A-F]{4}$', candidate):
                    return candidate
        
        # 如果还是找不到，尝试从原始文本中提取
        hex_patterns = re.findall(r'[0-9A-Fa-f]{4}', text.upper())
        if hex_patterns:
            return hex_patterns[0]
        
        return None
    
    def _extract_hex_codes(self, text):
        """
        从文本中提取所有可能的4位十六进制验证码
        
        Args:
            text (str): 原始文本
            
        Returns:
            list: 找到的4位十六进制验证码列表
        """
        import re
        
        # 查找所有4位十六进制模式
        hex_codes = re.findall(r'[0-9A-Fa-f]{4}', text.upper())
        
        # 过滤掉明显不是验证码的（比如全是0或全是F）
        valid_codes = []
        for code in hex_codes:
            if not (code == '0000' or code == 'FFFF' or code == 'AAAA'):
                valid_codes.append(code)
        
        return valid_codes
    
    def solve_captcha_multiple_attempts(self, image, max_attempts=6):
        """
        多次尝试识别验证码，选择最佳结果
        
        Args:
            image (PIL.Image.Image): 验证码图片
            max_attempts (int): 最大尝试次数
            
        Returns:
            str: 识别出的验证码文本，如果失败返回None
        """
        results = []
        
        for attempt in range(max_attempts):
            try:
                # 每次尝试使用不同的提示词 - 针对4位十六进制验证码优化
                prompts = [
                    "快速识别4位十六进制验证码。只输出结果。",
                    "识别验证码，忽略干扰。只输出4位字符。",
                    "分析字符形状，快速识别。只输出结果。",
                    "专注字符特征，快速识别。只输出结果。",
                    "忽略背景，识别字符。只输出结果。",
                    "快速分析，识别验证码。只输出结果。",
                    "专注形状，快速识别。只输出结果。",
                    "分析线条，识别字符。只输出结果。"
                ]
                
                prompt = prompts[attempt % len(prompts)]
                
                # 将图片转换为base64编码
                buffered = io.BytesIO()
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                image.save(buffered, format="JPEG", quality=95)
                img_base64 = base64.b64encode(buffered.getvalue()).decode()
                
                # 调用OpenAI API
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": """你是一个专业的验证码识别专家。请快速识别图片中的4位十六进制验证码。

规则：
- 只输出4位十六进制字符（0-9, A-F）
- 忽略所有干扰元素
- 专注于字符形状特征
- 快速响应，不要解释

字符特征：
0: 圆形/椭圆，可能有中心点
1: 直线，可能有小钩
2: 弯曲顶部和底部
3: 两条水平线+弯曲中间
4: 两条垂直线+一条水平线
5: 弯曲顶部和底部
6: 圆形，顶部开口
7: 水平线+斜线
8: 两个圆形/椭圆
9: 圆形，底部开口
A: 三角形顶部+中间横线
B: 两条垂直线+两条水平线
C: 开口圆形
D: 圆形+一条垂直线
E: 垂直线+三条水平线
F: 垂直线+两条水平线

快速识别，只输出结果。"""
                        },
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}
                                }
                            ]
                        }
                    ]
                )
                
                captcha_text = response.choices[0].message.content.strip()
                
                # 使用新的十六进制验证码清理方法
                cleaned_text = self._clean_hex_captcha(captcha_text)
                
                if cleaned_text:
                    results.append(cleaned_text)
                    self.logger.info(f"第{attempt + 1}次尝试成功: '{cleaned_text}'")
                else:
                    self.logger.warning(f"第{attempt + 1}次尝试结果为空")
                    
            except Exception as e:
                self.logger.error(f"第{attempt + 1}次尝试失败: {e}")
            
            if attempt < max_attempts - 1:
                import time
                time.sleep(1)
        
        # 选择最佳结果
        if results:
            # 如果有多个结果，选择出现次数最多的
            from collections import Counter
            counter = Counter(results)
            best_result = counter.most_common(1)[0][0]
            self.logger.info(f"多次识别完成，选择最佳结果: '{best_result}' (出现{counter[best_result]}次)")
            return best_result
        
        return None
    
    def auto_solve_captcha(self, driver, captcha_selector=None, max_retries=3):
        """
        自动识别并填写验证码
        
        Args:
            driver: Selenium WebDriver实例
            captcha_selector (str, optional): 验证码图片的选择器
            max_retries (int): 最大重试次数
            
        Returns:
            bool: 是否成功识别并填写验证码
        """
        try:
            # 尝试多种识别策略
            captcha_text = None
            all_results = []
            
            # 策略1: 使用预处理后的图片识别
            self.logger.info("策略1: 使用预处理后的图片识别...")
            captcha_image = self.capture_captcha_image(driver, captcha_selector)
            if captcha_image:
                captcha_text = self.solve_captcha(captcha_image, max_retries)
                if captcha_text:
                    all_results.append(("预处理图片", captcha_text))
            
            # 策略2: 如果策略1失败，尝试使用原图
            if not captcha_text:
                self.logger.info("策略2: 使用原图识别...")
                original_image = self.capture_captcha_image_original(driver, captcha_selector)
                if original_image:
                    captcha_text = self.solve_captcha(original_image, max_retries)
                    if captcha_text:
                        all_results.append(("原图", captcha_text))
            
            # 策略3: 如果还是失败，尝试多次识别并选择最佳结果
            if not captcha_text:
                self.logger.info("策略3: 多次识别选择最佳结果...")
                if captcha_image:
                    captcha_text = self.solve_captcha_multiple_attempts(captcha_image, max_retries * 2)
                    if captcha_text:
                        all_results.append(("多次识别", captcha_text))
            
            # 策略4: 智能重试 - 如果所有策略都失败，尝试不同的预处理方法
            if not captcha_text and captcha_image:
                self.logger.info("策略4: 智能重试不同预处理方法...")
                captcha_text = self._smart_retry_with_different_preprocessing(captcha_image, max_retries)
                if captcha_text:
                    all_results.append(("智能重试", captcha_text))
            
            if not captcha_text:
                self.logger.error("所有识别策略都失败")
                return False
            
            # 记录所有成功的结果
            if all_results:
                self.logger.info("所有识别结果:")
                for method, result in all_results:
                    self.logger.info(f"  {method}: {result}")
            
            # 查找验证码输入框
            input_selectors = [
                "//input[@name='code']",
                "//input[@id='code']",
                "//input[@placeholder*='验证码']",
                "//input[@placeholder*='驗證碼']",
                "//input[contains(@class, 'captcha')]",
                "//input[@type='text'][@maxlength='4']",
                "//input[@type='text'][@maxlength='6']"
            ]
            
            captcha_input = None
            for selector in input_selectors:
                try:
                    captcha_input = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    self.logger.info(f"找到验证码输入框: {selector}")
                    break
                except:
                    continue
            
            if not captcha_input:
                self.logger.error("无法找到验证码输入框")
                return False
            
            # 填写验证码
            captcha_input.clear()
            captcha_input.send_keys(captcha_text)
            self.logger.info(f"已填写验证码: {captcha_text}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"自动识别验证码时发生错误: {e}")
            return False
    
    def _smart_retry_with_different_preprocessing(self, image, max_retries=3):
        """
        使用不同预处理方法进行智能重试
        
        Args:
            image (PIL.Image.Image): 原始验证码图片
            max_retries (int): 最大重试次数
            
        Returns:
            str: 识别出的验证码文本，如果失败返回None
        """
        try:
            # 尝试不同的预处理参数
            preprocessing_variations = [
                ("高对比度", self._apply_high_contrast_preprocessing),
                ("边缘增强", self._apply_edge_enhancement_preprocessing),
                ("形态学优化", self._apply_morphological_preprocessing),
                ("自适应阈值", self._apply_adaptive_threshold_preprocessing)
            ]
            
            for variation_name, preprocessing_func in preprocessing_variations:
                try:
                    self.logger.info(f"尝试 {variation_name} 预处理...")
                    processed_image = preprocessing_func(image)
                    if processed_image:
                        result = self.solve_captcha(processed_image, max_retries=2)
                        if result:
                            self.logger.info(f"{variation_name} 预处理成功识别: {result}")
                            return result
                except Exception as e:
                    self.logger.warning(f"{variation_name} 预处理失败: {e}")
                    continue
            
            return None
            
        except Exception as e:
            self.logger.error(f"智能重试失败: {e}")
            return None
    
    def _apply_high_contrast_preprocessing(self, image):
        """应用高对比度预处理"""
        try:
            from PIL import ImageEnhance, ImageFilter
            
            # 转换为灰度图
            gray = image.convert('L')
            
            # 锐化
            sharpened = gray.filter(ImageFilter.UnsharpMask(radius=2, percent=300, threshold=1))
            
            # 对比度增强
            enhancer = ImageEnhance.Contrast(sharpened)
            enhanced = enhancer.enhance(3.0)
            
            # 转换为RGB
            return enhanced.convert('RGB')
        except Exception as e:
            self.logger.warning(f"高对比度预处理失败: {e}")
            return None
    
    def _apply_edge_enhancement_preprocessing(self, image):
        """应用边缘增强预处理"""
        try:
            from PIL import ImageFilter, ImageEnhance
            
            # 转换为灰度图
            gray = image.convert('L')
            
            # 边缘检测
            edges = gray.filter(ImageFilter.FIND_EDGES)
            
            # 锐化
            sharpened = edges.filter(ImageFilter.UnsharpMask(radius=1, percent=200, threshold=1))
            
            # 对比度增强
            enhancer = ImageEnhance.Contrast(sharpened)
            enhanced = enhancer.enhance(2.5)
            
            # 转换为RGB
            return enhanced.convert('RGB')
        except Exception as e:
            self.logger.warning(f"边缘增强预处理失败: {e}")
            return None
    
    def _apply_morphological_preprocessing(self, image):
        """应用形态学预处理"""
        try:
            from PIL import ImageFilter, ImageEnhance, ImageMorph
            
            # 转换为灰度图
            gray = image.convert('L')
            
            # 中值滤波去噪
            median_filtered = gray.filter(ImageFilter.MedianFilter(size=5))
            
            # 形态学操作：开运算
            morph = ImageMorph.MorphOp('open')
            opened = morph.apply(median_filtered)
            
            # 锐化
            sharpened = opened.filter(ImageFilter.UnsharpMask(radius=1, percent=180, threshold=2))
            
            # 转换为RGB
            return sharpened.convert('RGB')
        except Exception as e:
            self.logger.warning(f"形态学预处理失败: {e}")
            return None
    
    def _apply_adaptive_threshold_preprocessing(self, image):
        """应用自适应阈值预处理"""
        try:
            from PIL import ImageEnhance
            
            # 转换为灰度图
            gray = image.convert('L')
            
            # 计算自适应阈值
            threshold = self._get_adaptive_threshold(gray)
            
            # 二值化
            binary = gray.point(lambda x: 255 if x > threshold else 0, '1')
            
            # 对比度增强
            enhancer = ImageEnhance.Contrast(binary)
            enhanced = enhancer.enhance(2.0)
            
            # 转换为RGB
            return enhanced.convert('RGB')
        except Exception as e:
            self.logger.warning(f"自适应阈值预处理失败: {e}")
            return None

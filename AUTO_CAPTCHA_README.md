# NCKU Course Bot 自动验证码识别功能

## 功能概述

本项目已集成 OpenAI API 自动验证码识别功能，可以自动识别登录和选课过程中的验证码，大大提升自动化程度。

## 新增功能

### 1. 自动验证码识别
- 使用 OpenAI GPT-5-fast 模型识别验证码图片
- 支持登录验证码和选课验证码的自动识别
- 自动填写验证码到对应输入框
- 失败时自动回退到手动输入模式

### 2. 智能图片截取
- 自动定位验证码图片元素
- 支持多种选择器策略
- 智能截图并转换为适合AI识别的格式

### 3. 配置灵活性
- 支持环境变量配置
- 支持配置文件配置
- 可启用/禁用自动验证码识别

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置说明

### 方法1：环境变量（推荐）

```bash
# 设置OpenAI API密钥
export OPENAI_API_KEY="your_openai_api_key_here"

# 设置NCKU登录凭据（可选）
export NCKU_USERNAME="your_username"
export NCKU_PASSWORD="your_password"

# 启用/禁用自动验证码识别（可选，默认启用）
export AUTO_CAPTCHA="true"
```

### 方法2：配置文件

在 `config.json` 中添加：

```json
{
  "openai_config": {
    "api_key": "your_openai_api_key_here",
    "model": "gpt-5-fast",
    "max_tokens": 10,
    "temperature": 0.1
  },
  "verification": {
    "auto_captcha": true,
    "captcha_retry_count": 3
  }
}
```

## 使用方法

### 1. 基本使用

```python
from course_bot import NCKUCourseBot

# 创建机器人实例
bot = NCKUCourseBot()

# 自动登录（包含自动验证码识别）
bot.auto_login()

# 自动选课（包含自动验证码识别）
bot.select_all_courses()
```

### 2. 测试功能

```bash
# 测试自动验证码识别功能
python test_auto_captcha.py
```

## 工作流程

### 登录流程
1. 自动填写用户名和密码
2. 截取验证码图片
3. 使用 OpenAI API 识别验证码
4. 自动填写验证码
5. 点击登录按钮

### 选课流程
1. 点击选课按钮
2. 等待验证码输入框出现
3. 截取验证码图片
4. 使用 OpenAI API 识别验证码
5. 自动填写验证码
6. 点击确认按钮

## 错误处理

### 自动识别失败时的回退策略
1. 如果 AI 识别失败，自动切换到手动输入模式
2. 给用户足够的时间手动输入验证码
3. 记录详细的错误日志

### 重试机制
- 验证码识别支持多次重试
- 可配置重试次数和间隔时间
- 智能错误分类和处理

## 性能优化

### 图片处理优化
- 使用 PIL 库进行图片处理
- 优化图片格式和大小
- 减少 API 调用延迟

### 选择器优化
- 多种备用选择器策略
- 智能元素定位
- 减少页面等待时间

## 安全考虑

### API 密钥安全
- 优先使用环境变量存储敏感信息
- 避免在代码中硬编码 API 密钥
- 支持配置文件加密（可选）

### 反检测机制
- 保持原有的反检测功能
- 智能等待时间
- 模拟真实用户行为

## 故障排除

### 常见问题

1. **无法导入模块**
   ```bash
   pip install -r requirements.txt
   ```

2. **API 密钥错误**
   - 检查环境变量设置
   - 验证 API 密钥有效性
   - 确认账户余额充足

3. **验证码识别失败**
   - 检查网络连接
   - 验证图片截取是否成功
   - 查看详细错误日志

4. **浏览器兼容性**
   - 确保 Chrome 版本兼容
   - 检查 WebDriver 版本
   - 更新相关依赖

### 调试模式

启用详细日志：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 更新日志

### v2.0.0
- 新增 OpenAI API 自动验证码识别
- 集成智能图片截取功能
- 支持多种配置方式
- 增强错误处理和回退机制

## 技术支持

如果遇到问题，请：
1. 查看日志文件 `course_bot.log`
2. 运行测试脚本 `test_auto_captcha.py`
3. 检查配置文件和环境变量
4. 查看详细的错误信息

## 注意事项

1. **API 费用**：使用 OpenAI API 会产生费用，请合理使用
2. **识别准确率**：AI 识别准确率通常在 90% 以上，但并非 100%
3. **网络要求**：需要稳定的网络连接访问 OpenAI API
4. **隐私保护**：验证码图片会发送到 OpenAI 服务器，请注意隐私保护

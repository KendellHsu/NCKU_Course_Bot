# NCKU_Course_Bot

成功大学选课机器人 - 支持自动验证码识别

## 🚀 新功能：AI 自动验证码识别

本项目已集成 **OpenAI API 自动验证码识别功能**，可以：

- 🤖 自动识别登录验证码
- 🤖 自动识别选课验证码  
- 📸 智能截取验证码图片
- 🔄 失败时自动回退到手动模式
- ⚙️ 灵活的配置选项

## ✨ 主要特性

- **全自动化选课**：从登录到选课全程自动化
- **AI 验证码识别**：使用 GPT-4o 模型自动识别验证码
- **智能浏览器管理**：支持连接现有浏览器或开启新浏览器
- **批量选课支持**：可同时选择多门课程
- **反检测机制**：隐藏自动化特征，避免被系统检测
- **完善的错误处理**：详细的日志记录和异常处理

## 🛠️ 安装和配置

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 OpenAI API

**方法1：环境变量（推荐）**
```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```

**方法2：配置文件**
在 `config.json` 中添加：
```json
{
  "openai_config": {
    "api_key": "your_openai_api_key_here",
    "model": "gpt-5-fast"
  }
}
```

### 3. 配置课程信息

编辑 `config.json` 文件，添加你要选择的课程：
```json
{
  "courses": [
    {
      "department_code": "M1",
      "course_number": "023", 
      "course_name": "射頻振盪器電路設計專論"
    }
  ]
}
```

## 🚀 使用方法

### 基本使用

```python
from course_bot import NCKUCourseBot

# 创建机器人实例
bot = NCKUCourseBot()

# 自动登录（包含AI验证码识别）
bot.auto_login()

# 自动选课（包含AI验证码识别）
bot.select_all_courses()
```

### 测试功能

```bash
# 测试自动验证码识别
python test_auto_captcha.py

# 测试完整流程
python test_complete_flow.py
```

## 📋 工作流程

1. **启动浏览器** → 连接现有或开启新浏览器
2. **自动登录** → 填写账号密码 + AI识别验证码
3. **导航选课页面** → 自动跳转到选课系统
4. **课程检查** → 验证目标课程是否存在
5. **自动选课** → 点击选课按钮 + AI识别验证码
6. **确认选课** → 自动点击确认按钮

## 🔧 高级配置

### 验证码设置

```json
{
  "verification": {
    "auto_captcha": true,        // 启用AI验证码识别
    "captcha_retry_count": 3,    // 验证码识别重试次数
    "wait_time": 2               // 等待时间
  }
}
```

### OpenAI 模型配置

```json
{
  "openai_config": {
    "model": "gpt-5-fast",       // 使用的模型
    "max_tokens": 10,            // 最大输出长度
    "temperature": 0.1           // 输出随机性
  }
}
```

## 📚 详细文档

- [自动验证码识别功能说明](AUTO_CAPTCHA_README.md)
- [配置文件模板](config_template.json)
- [测试脚本说明](test_*.py)

## ⚠️ 注意事项

1. **API 费用**：使用 OpenAI API 会产生费用
2. **识别准确率**：AI 识别准确率通常在 90% 以上
3. **网络要求**：需要稳定的网络连接
4. **隐私保护**：验证码图片会发送到 OpenAI 服务器

## 🐛 故障排除

### 常见问题

1. **无法导入模块** → 运行 `pip install -r requirements.txt`
2. **API 密钥错误** → 检查环境变量或配置文件
3. **验证码识别失败** → 查看日志文件，检查网络连接
4. **浏览器兼容性** → 确保 Chrome 版本兼容

### 调试模式

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📝 更新日志

### v2.0.0
- 🆕 新增 OpenAI API 自动验证码识别
- 🆕 集成智能图片截取功能
- 🆕 支持多种配置方式
- 🔧 增强错误处理和回退机制

### v1.0.0
- 🆕 基础选课机器人功能
- 🆕 Selenium 自动化支持
- 🆕 反检测机制

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目仅供学习和研究使用，请遵守相关法律法规和网站使用条款。
# NCKU Course Bot 使用指南

## 🚀 快速开始

### 1. 环境建置
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置 OpenAI API
```bash
# 设置环境变量（推荐）
export OPENAI_API_KEY="your_api_key_here"

# 或者编辑 config.json 文件
```

### 3. 配置课程信息
编辑 `config.json` 文件，填入：
- 你的学号和密码
- 要选择的课程信息
- OpenAI API 配置

### 4. 运行程序
```bash
# 测试功能
python test_auto_captcha.py

# 查看演示
python demo_usage.py

# 运行主程序
python course_bot.py
```

## 🤖 主要功能

### 自动验证码识别
- **登录验证码**：自动识别并填写登录验证码
- **选课验证码**：自动识别并填写选课验证码
- **智能回退**：识别失败时自动切换到手动模式

### 全自动化选课
1. 自动启动浏览器
2. 自动填写登录信息
3. AI 识别验证码
4. 自动选课操作
5. 智能错误处理

## ⚙️ 配置选项

### 模型设置
- **当前模型**：`gpt-5-fast`
- **识别准确率**：通常在 90% 以上
- **响应速度**：快速响应，适合实时操作

### 验证码设置
```json
{
  "verification": {
    "auto_captcha": true,        // 启用AI识别
    "captcha_retry_count": 3,    // 重试次数
    "wait_time": 2               // 等待时间
  }
}
```

## 🔧 故障排除

### 常见问题
1. **依赖包未安装** → 运行 `pip install -r requirements.txt`
2. **API 密钥错误** → 检查环境变量或配置文件
3. **验证码识别失败** → 查看日志，检查网络连接
4. **浏览器问题** → 确保 Chrome 版本兼容

### 调试模式
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📚 更多信息

- [完整功能说明](AUTO_CAPTCHA_README.md)
- [配置文件模板](config_example.json)
- [测试脚本](test_auto_captcha.py)
- [使用演示](demo_usage.py)

## ⚠️ 注意事项

1. **API 费用**：使用 OpenAI API 会产生费用
2. **网络要求**：需要稳定的网络连接
3. **隐私保护**：验证码图片会发送到 OpenAI 服务器
4. **使用条款**：请遵守相关法律法规和网站使用条款

## 🎯 下一步

1. 设置 OpenAI API 密钥
2. 配置你的课程信息
3. 测试自动验证码识别功能
4. 开始自动化选课！

---

**祝您选课顺利！** 🎉

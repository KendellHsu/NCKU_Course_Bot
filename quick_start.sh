#!/bin/bash

# NCKU Course Bot 快速启动脚本
echo "🤖 NCKU Course Bot 快速启动"
echo "================================"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在，请先运行: python3 -m venv venv"
    exit 1
fi

# 激活虚拟环境
echo "1. 激活虚拟环境..."
source venv/bin/activate

# 检查依赖
echo "2. 检查依赖包..."
python -c "import selenium, openai, PIL, requests, dotenv" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ 依赖包未安装，正在安装..."
    pip install -r requirements.txt
fi

# 检查配置文件
if [ ! -f "config.json" ]; then
    echo "3. 配置文件不存在，创建示例配置..."
    cp config_example.json config.json
    echo "⚠️  请编辑 config.json 文件，填入你的配置信息"
    echo "   特别是 OpenAI API 密钥和课程信息"
fi

# 检查环境变量
if [ -z "$OPENAI_API_KEY" ]; then
    echo "4. 环境变量检查..."
    echo "⚠️  未设置 OPENAI_API_KEY 环境变量"
    echo "   请运行以下命令设置："
    echo "   export OPENAI_API_KEY='your_api_key_here'"
    echo ""
    echo "   或者编辑 config.json 文件，在 openai_config.api_key 中填入密钥"
fi

echo ""
echo "5. 运行测试..."
echo "   测试自动验证码识别: python test_auto_captcha.py"
echo "   查看使用演示: python demo_usage.py"
echo "   运行主程序: python course_bot.py"
echo ""
echo "6. 环境变量设置示例："
echo "   export OPENAI_API_KEY='your_api_key_here'"
echo "   export NCKU_USERNAME='your_username'"
echo "   export NCKU_PASSWORD='your_password'"
echo "   export AUTO_CAPTCHA='true'"
echo ""
echo "✅ 环境建置完成！"
echo "   现在你可以开始使用 NCKU Course Bot 了"

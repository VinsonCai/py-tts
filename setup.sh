#!/bin/bash

# TTS服务安装脚本

echo "正在创建Python虚拟环境..."
python3 -m venv venv

echo "正在激活虚拟环境..."
source venv/bin/activate

echo "正在安装依赖包..."
pip install --upgrade pip
pip install -r requirements.txt

echo "安装完成！"
echo ""
echo "要启动服务，请运行："
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
echo "或者使用uvicorn："
echo "  source venv/bin/activate"
echo "  uvicorn app:app --host 0.0.0.0 --port 8000 --reload"


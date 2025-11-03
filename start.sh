#!/bin/bash

# TTS服务启动脚本

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "虚拟环境不存在，请先运行 ./setup.sh 进行安装"
    exit 1
fi

# 激活虚拟环境
source venv/bin/activate

# 启动服务
echo "正在启动TTS服务..."
echo "服务地址: http://localhost:8000"
echo "API文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

python app.py


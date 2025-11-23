#!/bin/bash

# TTS服务部署脚本
# 用于将服务安装为 systemd 服务并启动

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_NAME="py-tts"
SERVICE_FILE="${SCRIPT_DIR}/${SERVICE_NAME}.service"
SYSTEMD_DIR="/etc/systemd/system"

echo "=========================================="
echo "TTS服务部署脚本"
echo "=========================================="
echo ""

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then 
    echo "错误: 请使用 sudo 运行此脚本"
    echo "用法: sudo ./deploy.sh"
    exit 1
fi

# 检查服务文件是否存在
if [ ! -f "$SERVICE_FILE" ]; then
    echo "错误: 找不到服务文件 $SERVICE_FILE"
    exit 1
fi

# 检查虚拟环境是否存在
if [ ! -d "${SCRIPT_DIR}/venv" ]; then
    echo "警告: 虚拟环境不存在，正在创建..."
    cd "$SCRIPT_DIR"
    ./setup.sh
fi

# 更新服务文件中的路径
echo "正在更新服务文件路径..."
sed -i "s|WorkingDirectory=.*|WorkingDirectory=${SCRIPT_DIR}|g" "$SERVICE_FILE"
sed -i "s|Environment=\"PATH=.*|Environment=\"PATH=${SCRIPT_DIR}/venv/bin\"|g" "$SERVICE_FILE"
sed -i "s|ExecStart=.*|ExecStart=${SCRIPT_DIR}/venv/bin/uvicorn app:app --host 0.0.0.0 --port 8000|g" "$SERVICE_FILE"

# 获取当前用户名（如果服务文件中有 %i）
CURRENT_USER=$(whoami)
sed -i "s|User=%i|User=${CURRENT_USER}|g" "$SERVICE_FILE"

# 复制服务文件到 systemd 目录
echo "正在安装 systemd 服务..."
cp "$SERVICE_FILE" "${SYSTEMD_DIR}/${SERVICE_NAME}.service"

# 重新加载 systemd
echo "正在重新加载 systemd..."
systemctl daemon-reload

# 启用服务（开机自启）
echo "正在启用服务（开机自启）..."
systemctl enable "${SERVICE_NAME}.service"

# 启动服务
echo "正在启动服务..."
systemctl start "${SERVICE_NAME}.service"

# 等待一下，检查服务状态
sleep 2

# 检查服务状态
if systemctl is-active --quiet "${SERVICE_NAME}.service"; then
    echo ""
    echo "=========================================="
    echo "✓ 服务部署成功！"
    echo "=========================================="
    echo ""
    echo "服务状态:"
    systemctl status "${SERVICE_NAME}.service" --no-pager -l
    echo ""
    echo "常用命令:"
    echo "  查看状态: sudo systemctl status ${SERVICE_NAME}.service"
    echo "  查看日志: sudo journalctl -u ${SERVICE_NAME}.service -f"
    echo "  停止服务: sudo systemctl stop ${SERVICE_NAME}.service"
    echo "  重启服务: sudo systemctl restart ${SERVICE_NAME}.service"
    echo "  禁用自启: sudo systemctl disable ${SERVICE_NAME}.service"
    echo ""
    echo "服务地址: http://localhost:8000"
    echo "API文档: http://localhost:8000/docs"
else
    echo ""
    echo "=========================================="
    echo "✗ 服务启动失败"
    echo "=========================================="
    echo ""
    echo "请查看日志以获取详细信息:"
    echo "  sudo journalctl -u ${SERVICE_NAME}.service -n 50"
    exit 1
fi


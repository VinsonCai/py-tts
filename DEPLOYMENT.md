# TTS服务部署指南

本指南提供了将TTS服务打包并运行在后台的详细步骤。

## 方式一：使用 systemd 服务（推荐）

这是 Linux 系统上最推荐的方式，可以确保服务在系统重启后自动启动，并提供完善的日志管理。

### 前置要求

1. Linux 系统（Ubuntu/Debian/CentOS等）
2. Python 3.8+
3. sudo 权限

### 步骤 1: 准备项目

确保项目已经安装好依赖：

```bash
cd /home/vinson/codes/ai/py-tts
./setup.sh
```

### 步骤 2: 安装 systemd 服务

使用提供的部署脚本（推荐）：

```bash
sudo ./deploy.sh
```

或者手动安装：

```bash
# 1. 编辑服务文件，确保路径正确
nano py-tts.service

# 2. 复制服务文件到 systemd 目录
sudo cp py-tts.service /etc/systemd/system/

# 3. 重新加载 systemd
sudo systemctl daemon-reload

# 4. 启用服务（开机自启）
sudo systemctl enable py-tts.service

# 5. 启动服务
sudo systemctl start py-tts.service
```

### 步骤 3: 验证服务

```bash
# 查看服务状态
sudo systemctl status py-tts.service

# 查看服务日志
sudo journalctl -u py-tts.service -f

# 测试服务
curl http://localhost:8000/
```

### 常用管理命令

```bash
# 启动服务
sudo systemctl start py-tts.service

# 停止服务
sudo systemctl stop py-tts.service

# 重启服务
sudo systemctl restart py-tts.service

# 查看状态
sudo systemctl status py-tts.service

# 查看日志（实时）
sudo journalctl -u py-tts.service -f

# 查看最近50条日志
sudo journalctl -u py-tts.service -n 50

# 禁用开机自启
sudo systemctl disable py-tts.service

# 启用开机自启
sudo systemctl enable py-tts.service
```

### 配置代理（如果需要）

如果服务器需要通过代理访问外网，编辑服务文件：

```bash
sudo nano /etc/systemd/system/py-tts.service
```

在 `[Service]` 部分添加或修改：

```ini
Environment="EDGE_TTS_PROXY=http://proxy:port"
```

然后重启服务：

```bash
sudo systemctl daemon-reload
sudo systemctl restart py-tts.service
```

---

## 方式二：使用 Docker（可选）

Docker 方式便于部署和迁移，适合容器化环境。

### 前置要求

1. Docker 已安装
2. Docker Compose（可选）

### 步骤 1: 创建 Dockerfile

已提供 `Dockerfile`，可以直接使用。

### 步骤 2: 构建镜像

```bash
docker build -t py-tts:latest .
```

### 步骤 3: 运行容器

```bash
# 后台运行
docker run -d \
  --name py-tts \
  -p 8000:8000 \
  --restart unless-stopped \
  py-tts:latest

# 如果需要代理
docker run -d \
  --name py-tts \
  -p 8000:8000 \
  -e EDGE_TTS_PROXY="http://proxy:port" \
  --restart unless-stopped \
  py-tts:latest
```

### 步骤 4: 管理容器

```bash
# 查看日志
docker logs -f py-tts

# 停止容器
docker stop py-tts

# 启动容器
docker start py-tts

# 重启容器
docker restart py-tts

# 删除容器
docker rm py-tts
```

### 使用 Docker Compose

已提供 `docker-compose.yml`，可以直接使用：

```bash
# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

---

## 方式三：使用 nohup（简单快速）

适合临时运行或测试，不推荐用于生产环境。

### 步骤 1: 启动服务

```bash
cd /home/vinson/codes/ai/py-tts
source venv/bin/activate
nohup uvicorn app:app --host 0.0.0.0 --port 8000 > tts.log 2>&1 &
```

### 步骤 2: 查看日志

```bash
tail -f tts.log
```

### 步骤 3: 停止服务

```bash
# 查找进程
ps aux | grep uvicorn

# 停止进程（替换 PID 为实际进程号）
kill <PID>
```

---

## 方式四：使用 screen/tmux（适合开发测试）

适合需要交互式管理的场景。

### 使用 screen

```bash
# 创建新的 screen 会话
screen -S tts

# 在 screen 中启动服务
cd /home/vinson/codes/ai/py-tts
source venv/bin/activate
uvicorn app:app --host 0.0.0.0 --port 8000

# 按 Ctrl+A 然后按 D 来分离会话

# 重新连接会话
screen -r tts

# 列出所有会话
screen -ls
```

### 使用 tmux

```bash
# 创建新的 tmux 会话
tmux new -s tts

# 在 tmux 中启动服务
cd /home/vinson/codes/ai/py-tts
source venv/bin/activate
uvicorn app:app --host 0.0.0.0 --port 8000

# 按 Ctrl+B 然后按 D 来分离会话

# 重新连接会话
tmux attach -t tts

# 列出所有会话
tmux ls
```

---

## 防火墙配置

如果服务需要从外部访问，确保防火墙允许 8000 端口：

### Ubuntu/Debian (ufw)

```bash
sudo ufw allow 8000/tcp
sudo ufw reload
```

### CentOS/RHEL (firewalld)

```bash
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload
```

---

## 故障排除

### 服务无法启动

1. 检查日志：
   ```bash
   sudo journalctl -u py-tts.service -n 50
   ```

2. 检查端口是否被占用：
   ```bash
   sudo netstat -tlnp | grep 8000
   # 或
   sudo lsof -i :8000
   ```

3. 检查虚拟环境是否正确：
   ```bash
   /home/vinson/codes/ai/py-tts/venv/bin/python --version
   ```

### 服务启动但无法访问

1. 检查服务是否在监听：
   ```bash
   curl http://localhost:8000/
   ```

2. 检查防火墙设置

3. 检查服务绑定的地址（应该是 0.0.0.0，不是 127.0.0.1）

### 查看详细日志

```bash
# systemd 服务日志
sudo journalctl -u py-tts.service -f

# Docker 容器日志
docker logs -f py-tts

# nohup 日志
tail -f tts.log
```

---

## 性能优化建议

1. **使用 gunicorn + uvicorn workers**（生产环境推荐）：
   ```bash
   pip install gunicorn
   gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

2. **配置反向代理**（如 Nginx）：
   - 提供 HTTPS
   - 负载均衡
   - 静态文件服务

3. **监控和告警**：
   - 使用 systemd 的监控功能
   - 集成 Prometheus/Grafana
   - 设置健康检查

---

## 推荐方案总结

| 场景 | 推荐方案 |
|------|---------|
| 生产环境 | systemd 服务 |
| 容器化环境 | Docker |
| 开发测试 | screen/tmux |
| 临时运行 | nohup |

**生产环境强烈推荐使用 systemd 服务方式**，因为它提供了：
- 自动重启
- 开机自启
- 完善的日志管理
- 系统集成
- 资源限制（可选）


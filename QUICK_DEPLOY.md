# 快速部署参考

## 方式一：systemd 服务（推荐，3步完成）

```bash
# 1. 安装依赖
./setup.sh

# 2. 部署服务
sudo ./deploy.sh

# 3. 验证服务
curl http://localhost:8000/
```

**完成！** 服务已在后台运行，系统重启后会自动启动。

### 常用命令

```bash
# 查看状态
sudo systemctl status py-tts.service

# 查看日志
sudo journalctl -u py-tts.service -f

# 重启服务
sudo systemctl restart py-tts.service

# 停止服务
sudo systemctl stop py-tts.service
```

---

## 方式二：Docker（2步完成）

```bash
# 1. 启动服务
docker-compose up -d

# 2. 验证服务
curl http://localhost:8000/
```

### 常用命令

```bash
# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 重启服务
docker-compose restart
```

---

## 方式三：nohup（1步完成）

```bash
source venv/bin/activate
nohup uvicorn app:app --host 0.0.0.0 --port 8000 > tts.log 2>&1 &
```

查看日志：`tail -f tts.log`

---

## 详细文档

更多详细信息请参考 [DEPLOYMENT.md](DEPLOYMENT.md)


# TTS服务故障排除指南

## 问题：401 未授权错误

如果遇到以下错误：
```
TTS生成失败: 401, message='Invalid response status', url='wss://api.msedgeservices.com/...'
```

这表示 edge-tts 无法连接到微软的 TTS 服务。可能的原因和解决方案：

### 原因1：网络连接问题

**检查方法：**
```bash
# 测试是否能连接到微软服务
curl -I --connect-timeout 5 https://api.msedgeservices.com/

# 测试DNS解析
nslookup api.msedgeservices.com
```

**解决方案：**
- 确保服务器可以访问外网
- 检查防火墙设置，确保允许 HTTPS 和 WebSocket 连接
- 如果服务器在内网，可能需要配置代理

### 原因2：需要配置代理

如果服务器需要通过代理访问外网，可以：

**方法1：使用环境变量**
```bash
export EDGE_TTS_PROXY="http://proxy.example.com:8080"
python app.py
```

**方法2：在请求中指定代理**
```bash
# POST请求
curl -X POST http://localhost:8000/tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "你好，测试",
    "proxy": "http://proxy.example.com:8080"
  }' \
  --output test.mp3
```

**方法3：修改配置**
在 `app.py` 中设置默认代理（不推荐，安全性较低）

### 原因3：edge-tts 版本问题

尝试更新 edge-tts 到最新版本：
```bash
source venv/bin/activate
pip install --upgrade edge-tts
```

### 原因4：服务器环境限制

某些服务器环境（如 Docker 容器、云服务器）可能需要额外配置：

1. **检查网络模式**
   ```bash
   # Docker容器中，确保网络配置正确
   docker network inspect <network_name>
   ```

2. **检查DNS配置**
   ```bash
   cat /etc/resolv.conf
   ```

3. **测试WebSocket连接**
   ```bash
   # 使用websocat测试（如果已安装）
   websocat wss://api.msedgeservices.com/tts/cognitiveservices/websocket/v1
   ```

## 问题：生成的MP3文件内容不对

如果生成的MP3文件包含JSON错误消息而不是音频数据：

**检查清单：**
1. 查看服务日志，确认是否有错误信息
2. 测试网络连接（见上面）
3. 尝试使用POST方式而不是GET方式
4. 检查文本内容是否为空或包含特殊字符

**测试命令：**
```bash
# 使用POST方式（更可靠）
curl -X POST http://localhost:8000/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "test"}' \
  --output test.mp3

# 检查文件类型
file test.mp3
# 应该显示: MPEG ADTS, layer III, v2

# 检查文件大小
ls -lh test.mp3
# 应该大于1KB
```

## 问题：服务启动后无法访问

**检查清单：**
1. 确认服务正在运行：
   ```bash
   ps aux | grep python
   netstat -tlnp | grep 8000
   ```

2. 检查防火墙：
   ```bash
   # Ubuntu/Debian
   sudo ufw status
   
   # CentOS/RHEL
   sudo firewall-cmd --list-all
   ```

3. 检查端口是否被占用：
   ```bash
   lsof -i :8000
   ```

## 调试技巧

### 启用详细日志

修改 `app.py`，将日志级别改为 DEBUG：
```python
logging.basicConfig(level=logging.DEBUG)
```

### 使用测试脚本

```bash
source venv/bin/activate
python quick_test.py
```

### 查看服务日志

如果使用 uvicorn 启动：
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --log-level debug
```

## 常见错误代码

- **400 Bad Request**: 请求参数错误，检查文本内容和参数格式
- **401 Unauthorized**: 无法连接到微软服务，检查网络和代理配置
- **500 Internal Server Error**: 服务器内部错误，查看日志获取详细信息
- **Connection Timeout**: 网络超时，增加超时时间或检查网络连接

## 获取帮助

如果以上方法都无法解决问题，请提供以下信息：
1. 完整的错误日志
2. 网络环境（是否在内网、是否需要代理）
3. edge-tts 版本：`pip show edge-tts`
4. Python 版本：`python --version`
5. 操作系统信息：`uname -a`


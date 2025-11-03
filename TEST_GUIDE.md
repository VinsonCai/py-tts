# TTS服务本地测试指南

本文档介绍如何在服务器本地测试TTS服务。

## 前提条件

确保TTS服务已启动：
```bash
# 激活虚拟环境
source venv/bin/activate

# 启动服务
python app.py
# 或
./start.sh
```

服务将在 `http://localhost:8000` 运行。

## 测试方法

### 方法1：使用测试脚本（推荐）

运行完整的自动化测试：

```bash
# 确保服务在另一个终端运行，然后执行：
source venv/bin/activate
python test_client.py
```

这将测试所有接口并生成测试音频文件。

### 方法2：使用curl命令行

#### 1. 健康检查
```bash
curl http://localhost:8000/
```

#### 2. 获取语音列表
```bash
curl http://localhost:8000/voices | python -m json.tool
```

#### 3. 文本转语音（GET方式）
```bash
# 生成中文语音
curl "http://localhost:8000/tts/simple?text=你好，这是一个测试" --output test.mp3

# 生成英文语音（指定语音）
curl "http://localhost:8000/tts/simple?text=Hello%20World&voice=en-US-AriaNeural" --output test_en.mp3
```

#### 4. 文本转语音（POST方式）
```bash
curl -X POST http://localhost:8000/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "你好，这是一个TTS测试服务"}' \
  --output test_post.mp3
```

#### 5. 测试指定语音
```bash
curl -X POST http://localhost:8000/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "你好，我是晓伊", "voice": "zh-CN-XiaoyiNeural"}' \
  --output test_xiaoyi.mp3
```

### 方法3：使用Python交互式测试

```bash
source venv/bin/activate
python quick_test.py
```

### 方法4：浏览器测试

#### 访问API文档
打开浏览器访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

在Swagger UI中可以：
1. 直接测试所有接口
2. 查看请求/响应格式
3. 下载生成的音频文件

#### 直接访问接口
- 健康检查: http://localhost:8000/
- 语音列表: http://localhost:8000/voices
- GET方式TTS: http://localhost:8000/tts/simple?text=测试

## 测试音频文件

测试成功后，你会得到以下音频文件：
- `test_audio_post.mp3` - POST方式生成的音频
- `test_audio_get.mp3` - GET方式生成的音频
- `test.mp3` - curl测试生成的音频

可以使用以下命令播放（如果服务器有音频播放器）：
```bash
# 使用ffplay（如果已安装）
ffplay test.mp3

# 或使用aplay（Linux）
aplay test.mp3
```

## 常见问题

### 1. 连接被拒绝
- 检查服务是否已启动
- 检查端口8000是否被占用
- 确保防火墙允许本地连接

### 2. 音频文件为空或损坏
- 检查网络连接（edge-tts需要联网）
- 检查文本内容是否有效
- 查看服务日志中的错误信息

### 3. 语音列表为空
- edge-tts需要联网获取语音列表
- 如果网络问题，接口会返回默认的儿童语音列表
- 不影响TTS功能使用

## 性能测试

测试大量文本：
```bash
# 测试长文本
curl -X POST http://localhost:8000/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "这是一个较长的测试文本，用于测试TTS服务的性能和稳定性。服务应该能够处理各种长度的文本内容，并生成高质量的语音输出。"}' \
  --output long_test.mp3
```


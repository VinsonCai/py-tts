# TTS服务 - Microsoft Edge TTS

这是一个使用Microsoft Edge TTS免费服务的文本转语音服务，特别优化了适合儿童的声音。

## 功能特点

- 使用Microsoft Edge TTS免费服务
- 默认使用适合儿童的声音（中文：晓晓/晓伊，英文：Aria）
- 提供RESTful API供NextJS等应用调用
- 支持CORS跨域请求
- 返回MP3格式音频流

## 快速开始

### 方式1：使用安装脚本（推荐）

```bash
# 运行安装脚本
./setup.sh

# 启动服务
./start.sh
```

### 方式2：手动安装

#### 1. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

#### 2. 安装依赖

```bash
pip install -r requirements.txt
```

## 运行服务

### 方式1：直接运行

```bash
python app.py
```

### 方式2：使用uvicorn

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

服务将在 `http://localhost:8000` 启动

## API接口

### 1. 健康检查

```
GET /
```

返回服务状态

### 2. 获取可用语音列表

```
GET /voices
```

返回所有可用的儿童语音列表

### 3. 文本转语音（POST）

```
POST /tts
Content-Type: application/json

{
  "text": "你好，这是一个测试",
  "voice": "zh-CN-XiaoxiaoNeural",  // 可选
  "language": "zh-CN"  // 可选，默认zh-CN
}
```

返回MP3音频流

### 4. 文本转语音（GET - 简化版）

```
GET /tts/simple?text=你好，这是一个测试&voice=zh-CN-XiaoxiaoNeural
```

返回MP3音频流

## NextJS调用示例

### 使用fetch API

```javascript
// POST方式
async function generateSpeech(text) {
  const response = await fetch('http://localhost:8000/tts', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      text: text,
      // voice: 'zh-CN-XiaoxiaoNeural', // 可选
    }),
  });
  
  const blob = await response.blob();
  const audioUrl = URL.createObjectURL(blob);
  
  // 播放音频
  const audio = new Audio(audioUrl);
  audio.play();
  
  return audioUrl;
}

// GET方式（更简单）
async function generateSpeechSimple(text) {
  const response = await fetch(
    `http://localhost:8000/tts/simple?text=${encodeURIComponent(text)}`
  );
  
  const blob = await response.blob();
  const audioUrl = URL.createObjectURL(blob);
  
  const audio = new Audio(audioUrl);
  audio.play();
  
  return audioUrl;
}
```

### 使用axios

```javascript
import axios from 'axios';

async function generateSpeech(text) {
  const response = await axios.post('http://localhost:8000/tts', {
    text: text,
  }, {
    responseType: 'blob',
  });
  
  const audioUrl = URL.createObjectURL(response.data);
  const audio = new Audio(audioUrl);
  audio.play();
  
  return audioUrl;
}
```

## 默认儿童声音

- **中文（zh-CN）**: `zh-CN-XiaoxiaoNeural` (晓晓) - 年轻女性声音
- **中文（zh-CN-child）**: `zh-CN-XiaoyiNeural` (晓伊) - 更年轻的声音
- **英文（en-US）**: `en-US-AriaNeural` (Aria) - 年轻女性声音

## 测试服务

有多种方式可以测试服务，详细说明请参考 [测试指南](TEST_GUIDE.md)。

### 快速测试

#### 方式1：使用快速测试脚本（推荐）
```bash
source venv/bin/activate
python quick_test.py
```

#### 方式2：使用完整测试脚本
```bash
source venv/bin/activate
python test_client.py
```

#### 方式3：使用curl脚本
```bash
./test_curl.sh
```

#### 方式4：使用curl命令
```bash
# 健康检查
curl http://localhost:8000/

# 获取语音列表
curl http://localhost:8000/voices | python3 -m json.tool

# 生成语音（GET方式）
curl "http://localhost:8000/tts/simple?text=你好，测试" --output test.mp3

# 生成语音（POST方式）
curl -X POST http://localhost:8000/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "你好，这是一个测试"}' \
  --output test.mp3
```

#### 方式5：浏览器测试
访问 API 文档页面进行交互式测试：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

测试脚本会：
- 检查服务健康状态
- 获取可用语音列表
- 测试POST和GET方式的TTS接口
- 生成测试音频文件

## 注意事项

1. 确保防火墙允许8000端口
2. 如果NextJS应用在不同机器上，需要将`app.py`中的`allow_origins`设置为具体的域名
3. 首次运行时，edge-tts可能需要下载语音模型，请确保网络连接正常
4. 生产环境建议使用gunicorn或systemd来管理服务
5. **如果遇到401错误**，请参考 [故障排除指南](TROUBLESHOOTING.md)
6. 如果服务器需要通过代理访问外网，可以设置环境变量：`export EDGE_TTS_PROXY="http://proxy:port"`

## 项目结构

```
py-tts/
├── app.py              # 主服务程序
├── requirements.txt    # Python依赖包
├── setup.sh           # 安装脚本
├── start.sh           # 启动脚本
├── test_client.py     # 完整测试客户端
├── quick_test.py      # 快速测试脚本
├── test_curl.sh       # curl测试脚本
├── TEST_GUIDE.md      # 详细测试指南
├── TROUBLESHOOTING.md # 故障排除指南
├── README.md          # 本文件
└── .gitignore         # Git忽略文件
```

## 许可证

MIT License


#!/bin/bash

# curl测试脚本 - 快速测试TTS服务

BASE_URL="http://localhost:8000"

echo "=========================================="
echo "TTS服务 curl测试脚本"
echo "=========================================="
echo ""

echo "1. 健康检查..."
curl -s "$BASE_URL/" | python3 -m json.tool
echo ""

echo "2. 获取语音列表..."
curl -s "$BASE_URL/voices" | python3 -m json.tool | head -30
echo ""

echo "3. GET方式 TTS测试 (中文)..."
curl -s "http://localhost:8000/tts/simple?text=你好，这是一个测试" \
  --output test_curl_get.mp3
if [ -f test_curl_get.mp3 ]; then
    SIZE=$(stat -f%z test_curl_get.mp3 2>/dev/null || stat -c%s test_curl_get.mp3 2>/dev/null || echo "unknown")
    echo "✅ 成功! 音频已保存到 test_curl_get.mp3 (大小: $SIZE 字节)"
else
    echo "❌ 失败: 无法生成音频文件"
fi
echo ""

echo "4. POST方式 TTS测试 (中文)..."
curl -s -X POST "$BASE_URL/tts" \
  -H "Content-Type: application/json" \
  -d '{"text": "你好，这是POST方式的测试"}' \
  --output test_curl_post.mp3
if [ -f test_curl_post.mp3 ]; then
    SIZE=$(stat -f%z test_curl_post.mp3 2>/dev/null || stat -c%s test_curl_post.mp3 2>/dev/null || echo "unknown")
    echo "✅ 成功! 音频已保存到 test_curl_post.mp3 (大小: $SIZE 字节)"
else
    echo "❌ 失败: 无法生成音频文件"
fi
echo ""

echo "5. POST方式 TTS测试 (英文，指定语音)..."
curl -s -X POST "$BASE_URL/tts" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, this is a test with Aria voice", "voice": "en-US-AriaNeural"}' \
  --output test_curl_english.mp3
if [ -f test_curl_english.mp3 ]; then
    SIZE=$(stat -f%z test_curl_english.mp3 2>/dev/null || stat -c%s test_curl_english.mp3 2>/dev/null || echo "unknown")
    echo "✅ 成功! 音频已保存到 test_curl_english.mp3 (大小: $SIZE 字节)"
else
    echo "❌ 失败: 无法生成音频文件"
fi
echo ""

echo "=========================================="
echo "测试完成！"
echo "=========================================="
echo ""
echo "生成的测试文件:"
ls -lh test_curl_*.mp3 2>/dev/null || echo "  无音频文件生成"


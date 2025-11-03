#!/usr/bin/env python3
"""
快速测试脚本 - 用于快速验证TTS服务
"""
import requests
import sys
import os

BASE_URL = "http://localhost:8000"

def print_section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_health():
    """测试服务健康状态"""
    print_section("1. 健康检查")
    try:
        r = requests.get(f"{BASE_URL}/")
        print(f"状态码: {r.status_code}")
        print(f"响应: {r.json()}")
        return r.status_code == 200
    except Exception as e:
        print(f"❌ 失败: {e}")
        return False

def test_voices():
    """测试获取语音列表"""
    print_section("2. 获取语音列表")
    try:
        r = requests.get(f"{BASE_URL}/voices")
        data = r.json()
        print(f"状态码: {r.status_code}")
        print(f"总语音数: {data.get('total_voices', 0)}")
        print(f"默认儿童声音:")
        for lang, voice in data.get('default_children_voices', {}).items():
            print(f"  {lang}: {voice}")
        if 'warning' in data:
            print(f"⚠️  警告: {data['warning']}")
        return r.status_code == 200
    except Exception as e:
        print(f"❌ 失败: {e}")
        return False

def test_tts_get():
    """测试GET方式TTS"""
    print_section("3. GET方式 TTS测试")
    text = "你好，这是一个快速测试。"
    print(f"文本: {text}")
    try:
        url = f"{BASE_URL}/tts/simple?text={requests.utils.quote(text)}"
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            filename = "quick_test_get.mp3"
            with open(filename, "wb") as f:
                f.write(r.content)
            size = len(r.content)
            print(f"✅ 成功! 音频大小: {size:,} 字节")
            print(f"📁 已保存到: {filename}")
            return True
        else:
            print(f"❌ 失败: 状态码 {r.status_code}")
            print(f"响应: {r.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ 失败: {e}")
        return False

def test_tts_post():
    """测试POST方式TTS"""
    print_section("4. POST方式 TTS测试")
    text = "Hello, this is a quick test."
    print(f"文本: {text}")
    try:
        payload = {"text": text}
        r = requests.post(
            f"{BASE_URL}/tts",
            json=payload,
            timeout=30
        )
        if r.status_code == 200:
            filename = "quick_test_post.mp3"
            with open(filename, "wb") as f:
                f.write(r.content)
            size = len(r.content)
            print(f"✅ 成功! 音频大小: {size:,} 字节")
            print(f"📁 已保存到: {filename}")
            return True
        else:
            print(f"❌ 失败: 状态码 {r.status_code}")
            print(f"响应: {r.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ 失败: {e}")
        return False

def test_custom_voice():
    """测试自定义语音"""
    print_section("5. 自定义语音测试")
    text = "你好，我是晓伊。"
    voice = "zh-CN-XiaoyiNeural"
    print(f"文本: {text}")
    print(f"语音: {voice}")
    try:
        payload = {"text": text, "voice": voice}
        r = requests.post(
            f"{BASE_URL}/tts",
            json=payload,
            timeout=30
        )
        if r.status_code == 200:
            filename = "quick_test_custom.mp3"
            with open(filename, "wb") as f:
                f.write(r.content)
            size = len(r.content)
            print(f"✅ 成功! 音频大小: {size:,} 字节")
            print(f"📁 已保存到: {filename}")
            return True
        else:
            print(f"❌ 失败: 状态码 {r.status_code}")
            return False
    except Exception as e:
        print(f"❌ 失败: {e}")
        return False

def main():
    print("\n" + "🚀 " * 20)
    print("    TTS服务快速测试")
    print("🚀 " * 20)
    print(f"\n测试目标: {BASE_URL}")
    print("请确保服务已启动!\n")
    
    results = []
    results.append(("健康检查", test_health()))
    results.append(("语音列表", test_voices()))
    results.append(("GET TTS", test_tts_get()))
    results.append(("POST TTS", test_tts_post()))
    results.append(("自定义语音", test_custom_voice()))
    
    print_section("测试结果汇总")
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name:15} : {status}")
    
    print(f"\n总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！服务运行正常！")
        print("\n生成的测试文件:")
        for f in ["quick_test_get.mp3", "quick_test_post.mp3", "quick_test_custom.mp3"]:
            if os.path.exists(f):
                size = os.path.getsize(f)
                print(f"  - {f} ({size:,} 字节)")
    else:
        print("\n⚠️  部分测试失败，请检查服务状态")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  测试被中断")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("\n❌ 无法连接到服务!")
        print("请确保:")
        print("  1. 服务已启动 (运行: python app.py)")
        print("  2. 服务运行在 http://localhost:8000")
        sys.exit(1)


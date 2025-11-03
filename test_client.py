#!/usr/bin/env python3
"""
TTS服务测试客户端
用于测试TTS服务是否正常工作
"""
import requests
import sys

BASE_URL = "http://localhost:8000"

def test_health_check():
    """测试健康检查"""
    print("测试健康检查...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✓ 健康检查成功: {response.json()}")
        return True
    except Exception as e:
        print(f"✗ 健康检查失败: {e}")
        return False

def test_list_voices():
    """测试获取语音列表"""
    print("\n测试获取语音列表...")
    try:
        response = requests.get(f"{BASE_URL}/voices")
        data = response.json()
        print(f"✓ 获取语音列表成功")
        print(f"  默认儿童声音: {data.get('default_children_voices', {})}")
        return True
    except Exception as e:
        print(f"✗ 获取语音列表失败: {e}")
        return False

def test_tts_post(text="你好，这是一个测试。", voice=None):
    """测试POST方式的TTS"""
    print(f"\n测试POST方式TTS (文本: {text})...")
    try:
        payload = {"text": text}
        if voice:
            payload["voice"] = voice
        
        response = requests.post(
            f"{BASE_URL}/tts",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            audio_size = len(response.content)
            print(f"✓ POST方式TTS成功 (音频大小: {audio_size} 字节)")
            
            # 保存音频文件
            with open("test_audio_post.mp3", "wb") as f:
                f.write(response.content)
            print(f"  音频已保存到: test_audio_post.mp3")
            return True
        else:
            print(f"✗ POST方式TTS失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ POST方式TTS失败: {e}")
        return False

def test_tts_get(text="Hello, this is a test.", voice=None):
    """测试GET方式的TTS"""
    print(f"\n测试GET方式TTS (文本: {text})...")
    try:
        params = {"text": text}
        if voice:
            params["voice"] = voice
        
        response = requests.get(
            f"{BASE_URL}/tts/simple",
            params=params,
            timeout=30
        )
        
        if response.status_code == 200:
            audio_size = len(response.content)
            print(f"✓ GET方式TTS成功 (音频大小: {audio_size} 字节)")
            
            # 保存音频文件
            with open("test_audio_get.mp3", "wb") as f:
                f.write(response.content)
            print(f"  音频已保存到: test_audio_get.mp3")
            return True
        else:
            print(f"✗ GET方式TTS失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ GET方式TTS失败: {e}")
        return False

def main():
    print("=" * 50)
    print("TTS服务测试客户端")
    print("=" * 50)
    print(f"\n确保TTS服务已在 http://localhost:8000 运行\n")
    
    results = []
    
    # 运行测试
    results.append(("健康检查", test_health_check()))
    results.append(("语音列表", test_list_voices()))
    results.append(("POST TTS (中文)", test_tts_post("你好，这是一个TTS测试服务。", None)))
    results.append(("GET TTS (英文)", test_tts_get("Hello, this is a TTS test.", None)))
    
    # 显示测试结果
    print("\n" + "=" * 50)
    print("测试结果汇总:")
    print("=" * 50)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name}: {status}")
    
    print(f"\n总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！")
        return 0
    else:
        print("\n⚠️  部分测试失败，请检查服务是否正常运行")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n测试过程中发生错误: {e}")
        sys.exit(1)


"""
TTS服务 - 使用Microsoft Edge TTS
为NextJS应用提供文本转语音服务
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import edge_tts
from typing import Optional
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="TTS Service", version="1.0.0")

# 配置CORS，允许NextJS应用调用
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境建议设置为具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 适合儿童的声音列表（中文和英文）
CHILDREN_VOICES = {
    "zh-CN": "zh-CN-XiaoxiaoNeural",  # 晓晓（年轻女性，适合儿童内容）
    "zh-CN-child": "zh-CN-XiaoyiNeural",  # 晓伊（更年轻的声音）
    "en-US": "en-US-AriaNeural",  # Aria（年轻女性）
}

class TTSRequest(BaseModel):
    text: str
    voice: Optional[str] = None  # 如果不指定，使用默认儿童声音
    language: Optional[str] = "zh-CN"
    proxy: Optional[str] = None  # 可选的代理地址


@app.get("/")
async def root():
    return {"message": "TTS Service is running", "version": "1.0.0"}


@app.get("/voices")
async def list_voices():
    """获取可用的语音列表"""
    try:
        voices = await edge_tts.list_voices()
        
        # 筛选出适合儿童的声音
        children_voices = []
        for v in voices:
            try:
                # 安全地访问字典键
                name = str(v.get("Name", "")).lower()
                short_name = str(v.get("ShortName", "")).lower()
                
                # 检查是否包含适合儿童的关键词
                keywords = ["xiao", "xiaoxiao", "xiaoyi", "aria", "young", "child"]
                if any(keyword in name or keyword in short_name for keyword in keywords):
                    children_voices.append(v)
            except (KeyError, AttributeError, TypeError) as e:
                # 跳过无法处理的声音条目
                continue
        
        return {
            "voices": children_voices,
            "default_children_voices": CHILDREN_VOICES,
            "total_voices": len(voices)
        }
    except Exception as e:
        # 如果获取语音列表失败，至少返回默认的儿童声音
        # 将默认声音格式化为类似 list_voices 返回的格式
        default_voices_list = []
        for lang, voice_name in CHILDREN_VOICES.items():
            default_voices_list.append({
                "ShortName": voice_name,
                "Name": voice_name,
                "Locale": lang.split("-")[0] + "-" + lang.split("-")[1] if "-" in lang else lang,
                "Language": lang
            })
        
        return {
            "voices": default_voices_list,
            "default_children_voices": CHILDREN_VOICES,
            "warning": f"无法从服务器获取完整语音列表: {str(e)}",
            "total_voices": len(default_voices_list),
            "note": "返回的是默认的儿童语音列表"
        }


async def generate_audio_data(text: str, voice: str, proxy: Optional[str] = None) -> bytes:
    """
    生成完整的音频数据
    
    Args:
        text: 要转换的文本
        voice: 语音名称
        proxy: 可选的代理地址（格式：http://proxy:port 或 https://proxy:port）
        
    Returns:
        音频数据（bytes）
        
    Raises:
        Exception: 如果生成音频数据失败
    """
    try:
        # 从环境变量获取代理，如果提供了参数则使用参数
        proxy_url = proxy or os.getenv("EDGE_TTS_PROXY", None)
        
        # 增加超时时间，并尝试配置代理
        communicate = edge_tts.Communicate(
            text=text,
            voice=voice,
            proxy=proxy_url,
            connect_timeout=30,  # 增加连接超时到30秒
            receive_timeout=120   # 增加接收超时到120秒
        )
        
        logger.info(f"开始生成TTS音频: text长度={len(text)}, voice={voice}, proxy={proxy_url}")
        
        audio_data = b""
        chunk_count = 0
        async for chunk in communicate.stream():
            chunk_count += 1
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
            elif chunk["type"] == "error":
                error_msg = chunk.get("error", "Unknown error")
                logger.error(f"TTS流中收到错误: {error_msg}")
                raise Exception(f"TTS错误: {error_msg}")
        
        logger.info(f"TTS音频生成完成: 收到{chunk_count}个块, 总大小={len(audio_data)}字节")
        
        if not audio_data:
            raise Exception("未收到任何音频数据")
        
        return audio_data
    except Exception as e:
        logger.error(f"生成音频数据失败: {str(e)}", exc_info=True)
        # 重新抛出异常，让上层处理
        raise


@app.post("/tts")
async def text_to_speech(request: TTSRequest):
    """
    文本转语音接口
    
    Args:
        request: 包含文本、语音和语言的请求对象
        
    Returns:
        音频流（MP3格式）
    """
    if not request.text:
        raise HTTPException(status_code=400, detail="文本内容不能为空")
    
    # 选择语音
    if request.voice:
        voice = request.voice
    else:
        # 根据语言选择默认的儿童声音
        voice = CHILDREN_VOICES.get(
            request.language or "zh-CN",
            CHILDREN_VOICES["zh-CN"]
        )
    
    try:
        # 生成音频数据
        audio_data = await generate_audio_data(request.text, voice, proxy=request.proxy)
        
        if not audio_data:
            raise HTTPException(status_code=500, detail="未能生成音频数据")
        
        # 创建音频流生成器
        def audio_generator():
            yield audio_data
        
        return StreamingResponse(
            audio_generator(),
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f'attachment; filename="tts_audio.mp3"',
                "Content-Length": str(len(audio_data))
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS生成失败: {str(e)}")


@app.get("/tts/simple")
async def simple_tts(
    text: str = Query(..., description="要转换的文本", min_length=1),
    voice: Optional[str] = Query(None, description="可选的语音名称")
):
    """
    简化的GET接口，方便快速测试
    
    Args:
        text: 要转换的文本（必需）
        voice: 可选的语音名称
        
    Returns:
        音频流（MP3格式）
    """
    request = TTSRequest(text=text, voice=voice)
    return await text_to_speech(request)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


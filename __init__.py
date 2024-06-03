import os
import time
import asyncio
import folder_paths
from edge_tts import VoicesManager

out_path = folder_paths.get_output_directory()


async def get_voices():
    global voice_list
    voices = await VoicesManager.create()
    voice_list = [ voice['ShortName'] for voice in voices.voices]

asyncio.run(get_voices())

class EdgeTTS:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required":{
                "text": ("STRING",{
                        "default":"""edge-tts is a Python module that allows you to use Microsoft Edge's online text-to-speech service from within your Python code or using the provided edge-tts or edge-playback command.""",
                        "multiline": True,
                }),
                "voice": (voice_list,{
                    "default": "en-GB-SoniaNeural"
                }),
                "rate": ("STRING",{
                    "default": "+0%"
                }),
                "volume": ("STRING",{
                    "default": "+0%"
                }),
                "pitch": ("STRING",{
                    "default": "+0Hz"
                }),
            }
        }
    CATEGORY = "AIFSH_EdgeTTS"
    DESCRIPTION = "hello world!"

    RETURN_TYPES = ("AUDIO",)

    OUTPUT_NODE = False

    FUNCTION = "tts"

    def tts(self,text,voice,rate,volume,pitch):
        out_file = os.path.join(out_path, f"edge_tts_{time.time_ns()}.mp3")
        vtt_file = out_file.split(".")[0] + ".vtt"
        text = text.replace('\n', '')
        edge_tts_cmd = f"""edge-tts -t "{text}" -v {voice} --rate={rate} --volume={volume} \
            --pitch={pitch} --write-media {out_file} --write-subtitles {vtt_file}"""
        print(edge_tts_cmd)
        os.system(edge_tts_cmd)
        return (out_file, )

class PreViewAudio:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {"audio": ("AUDIO",),}
                }

    CATEGORY = "AIFSH_EdgeTTS"
    DESCRIPTION = "hello world!"

    RETURN_TYPES = ()

    OUTPUT_NODE = True

    FUNCTION = "load_audio"

    def load_audio(self, audio):
        audio_name = os.path.basename(audio)
        tmp_path = os.path.dirname(audio)
        audio_root = os.path.basename(tmp_path)
        return {"ui": {"audio":[audio_name,audio_root]}}

WEB_DIRECTORY = "./web"

# Set the web directory, any .js file in that directory will be loaded by the frontend as a frontend extension
# WEB_DIRECTORY = "./somejs"

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "EdgeTTS":EdgeTTS,
    "PreViewAudio": PreViewAudio
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "EdgeTTS":"EdgeTTS Node",
    "PreViewAudio": "PreView Audio"
}

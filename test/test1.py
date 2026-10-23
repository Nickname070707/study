from openai import OpenAI
import json
import os

HISTORY_FILE="messages.json"

class History:
    def __init__(self,system_prompt="you are a helpful assistant.",
                 file=HISTORY_FILE):
        self.file=file
        self.messages=[
            {"role":"system","content":system_prompt}
        ]

    def load(self):
        # """从文件读取历史（如果存在）"""
        if os.path.exists(self.file):
            with open(self.file,"r",encoding="utf-8") as f:
                data=json.load(f)
            if data:
                self.messages=data
        return self.messages

    def save(self):
        # """把当前历史写入文件"""
        with open(self.file,"w",encoding="utf-8") as f:
            json.dump(self.messages,f,ensure_ascii=False,indent=2)

    def clear(self):
        # """清空历史，只保留 system"""
        self.messages=self.messages[:1]
        self.save()

    def user_add(self,text):
        self.messages.append({"role":"user","content":text})

    def assistant_add(self,text):
        self.messages.append({"role":"assistant","content":text})


if __name__ == "__main__":
    history=History()
    history.load()          # 启动时恢复上次的对话

    client=OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",
    )

    while True:
        userin=input("user>")
        if userin.strip().lower() in ("exit","quit"):
            break

        if userin.strip() == "/clear":
            history.clear()      # 调用写好的方法
            print("history has cleared")
            continue

        history.user_add(userin)  # 调用写好的方法

        completion=client.chat.completions.create(
            model="deepseek-r1:8b-0528-qwen3-q4_K_M",
            messages=history.messages,
        )
        reply=completion.choices[0].message.content
        print(f"ai>{reply}")

        history.assistant_add(reply)  # 调用写好的方法
        history.save()                # 调用写好的方法
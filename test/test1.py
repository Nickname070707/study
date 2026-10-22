from openai import OpenAI
import json

class History:
    def __init__(self):
        self.messages=[
            {"role": "system", "content": "you are a helpful assistant."}
        ]

if __name__=="__main__":
    history=History()
    client=OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",
    )
    while True:
        userin=input("user>")
        if userin.strip().lower() in ("exit","quit"):
            break
        if userin.strip()=="/clear":
            history.messages=history.messages[:1]
            print("history has cleared")
            continue
        history.messages.append({"role":"user","content":userin})
        completion=client.chat.completions.create(
            model="deepseek-r1:8b-0528-qwen3-q4_K_M",
            messages=history.messages,
        )
        reply=completion.choices[0].message.content
        print(f"ai>{reply}")
        history.messages.append({"role":"assistant","content":reply})
        messagesStr=json.dumps(history.messages)
        with open("messages.json","w+") as msg:
            msg.write(messagesStr)
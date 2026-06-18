import argparse
import os
import sys
import json
import subprocess
from openai import OpenAI

API_KEY = os.getenv("OPENROUTER_API_KEY","ollama")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    model = os.getenv(
        "LOCAL_MODEL",# 由于是学习的代码 这里先给系统添加环境变量 调用本地ollama
        default="anthropic/claude-haiku-4.5"
    )

    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    messages = [{"role":"user","content":args.p}]

    while True:# Loop
        # 调用LLM
        chat = client.chat.completions.create(
            model=model,
            messages=messages,
            # 所有agent工具集
            tools=[
                # 给模型注册read这个工具（注册!=实现）
                {
                    "type":"function",
                    "function":{
                        "name":"Read",
                        "description":"Read and return the contents of a file",
                        "parameters":{
                            "type":"object",
                            "properties":{
                                "file_path":{
                                    "type":"string",
                                    "description":"The path to the file to read"
                                }
                            },
                            "required":["file_path"]
                        }
                    }
                },
                # 给模型注册Write工具
                {
                    "type":"function",
                    "function":{
                        "name":"Write",
                        "description":"Write content to a file",
                        "parameters":{
                            "type":"object",
                            "properties":{
                                "file_path":{
                                    "type":"string",
                                    "description":"The path of the file write to"
                                },
                                "content":{
                                    "type":"string",
                                    "description":"The content to write to the file"
                                }
                            },
                            "required":["file_path","content"]
                        }
                    }
                },
                # 给模型注册Bash工具
                {
                    "type":"function",
                    "function":{
                        "name":"Bash",
                        "description":"Execute a shell command",
                        "parameters":{
                            "type":"object",
                            "properties":{
                                "command":{
                                    "type":"string",
                                    "description":"The command to execute"
                                }
                            },
                            "required":["command"]
                        }
                    }
                }

            ]
        )

        if not chat.choices or len(chat.choices) == 0:
            raise RuntimeError("no choices in response")

        message = chat.choices[0].message
        # 先把助手消息加入历史
        messages.append(message.model_dump())

        # 如果没有工具调用 说明任务完成了 可以输出内容了
        if not getattr(message,"tool_calls",None):
            print(message.content)
            break

        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            if tool_name == "Read":
                file_path = tool_args["file_path"]
                with open(file_path,"r",encoding="utf-8") as f:
                    content = f.read()
                
                # 将工具输出的文件内容返回给历史消息 供LLM参考
                messages.append({
                    "role":"tool",
                    "tool_call_id":tool_call.id,
                    "content":content
                })
            elif tool_name == "Write":
                file_path = tool_args["file_path"]
                content = tool_args["content"]
                # 写入文件 不存在就创建 存在就覆盖
                with open(file_path,"w",encoding="utf-8") as f:
                    f.write(content)
                messages.append({
                    "role":"tool",
                    "tool_call_id":tool_call.id,
                    "content":f"Wrote to {file_path}"
                })
            elif tool_name == "Bash":
                command = tool_args["command"]
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True
                )
                output = result.stdout + result.stderr
                messages.append({
                    "role":"tool",
                    "tool_call_id":tool_call.id,
                    "content":output
                })

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    # # print(chat.choices[0].message.content)
    # message=chat.choices[0].message
    # #这里让LLM真正使用工具Read
    # if message.tool_calls:# 如果调用了read就返回文件内容
    #     tool_call = message.tool_calls[0]
    #     tool_name = tool_call.function.name
    #     tool_args = json.loads(
    #         tool_call.function.arguments
    #     )
    #     if tool_name == "Read":
    #         file_path = tool_args["file_path"]
    #         with open(file_path,"r",encoding="utf-8") as f:
    #             content = f.read()
    #         print(content)
    # else: # 如果没有调用Read的打算就直接返回原内容
    #     print(message.content)

if __name__ == "__main__":
    main()

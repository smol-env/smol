import json
import subprocess
import sys
import uuid
from random import random
from time import sleep
from urllib.request import Request, urlopen

url = sys.argv[1]
history = []
headers = {"Content-Type": "application/json", "session_id": uuid.uuid4().hex}
brief_prompt = "Handoff brief: goals, constraints, progress, decisions, next steps, exact values; omit noise. Return text, not a tool call."

def post(body):
    for attempt in range(3):
        try: return json.load(urlopen(Request(url, json.dumps(body).encode(), headers), timeout=300))
        except OSError as error:
            if attempt == 2 or getattr(error, "code", 500) < 500: raise
            sleep(2**attempt + random())

def shell(command, head=12_800, tail=27_200):
    output = subprocess.getoutput(command)
    return output if len(output) <= head + tail else output[:head] + "\n…output truncated…\n" + output[-tail:]

body = {
    "model": "gpt-5.6-sol",
    "input": history,
    "tools": [{
        "type": "function", "name": "sh", "description": "Run a shell command",
        "parameters": {"type": "object", "properties": {"command": {"type": "string"}}, "required": ["command"]},
    }],
}

while prompt := input("> "):
    history.append({"role": "user", "content": prompt})
    while True:
        response = post(body)
        output = response["output"]
        history += output
        calls = [item for item in output if item["type"] == "function_call"]
        if calls:
            history += [dict(type="function_call_output", call_id=c["call_id"], output=shell(**json.loads(c["arguments"]))) for c in calls]
        else:
            messages = [item["content"][0]["text"] for item in output if item["type"] == "message"]
            print(messages[-1])

        if response["usage"]["total_tokens"] > 244_800:
            brief = history + [{"role": "user", "content": brief_prompt}]
            compacted = post(dict(body, input=brief, tool_choice="none"))
            if any(item["type"] == "function_call" for item in compacted["output"]):
                compacted = post(dict(body, input=brief, tools=[]))
            messages = [item["content"][0]["text"] for item in compacted["output"] if item["type"] == "message"]
            history[:] = [{"role": "user", "content": "Briefing:\n" + messages[-1] + ("\nContinue." if calls else "")}]

        if calls: continue
        break

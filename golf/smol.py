import json,sys;from subprocess import getoutput;from urllib.request import Request,urlopen;from uuid import uuid4
url=sys.argv[1];h=[];H={"Content-Type":"application/json","session_id":uuid4().hex};b=dict(model="gpt-5.6-sol",input=h,tools=[dict(type="custom",name="sh")])
while True:
  if not(p:=input("> ")).strip():continue
  h+=[dict(role="user",content=p)]
  while True:
    r=json.load(urlopen(Request(url,json.dumps(b).encode(),H)));o=r["output"];h+=o;c=[i for i in o if i["type"]=="custom_tool_call"]
    if not c:print(o[-1]["content"][0]["text"],f'\n[{r["usage"]["total_tokens"]/10500:05.2f}%]');break
    h+=[dict(type="custom_tool_call_output",call_id=i["call_id"],output=getoutput(i["input"])) for i in c]

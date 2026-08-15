package main
import("bufio";"bytes";"crypto/rand";"encoding/json";"fmt";"net/http";"os";"os/exec")
type M=map[string]any
func main(){
 u:=os.Args[1];k:=rand.Text();h:=[]any{};s:=bufio.NewScanner(os.Stdin)
 for fmt.Print("> ");s.Scan();fmt.Print("> "){
  if len(bytes.TrimSpace(s.Bytes()))<1{continue}
  h=append(h,M{"role":"user","content":s.Text()})
  for{
   b,_:=json.Marshal(M{"model":"gpt-5.6-sol","input":h,"tools":[]M{{"type":"custom","name":"sh"}}})
   q,_:=http.NewRequest("POST",u,bytes.NewReader(b));q.Header=http.Header{"Content-Type":{"application/json"},"session_id":{k}};r,_:=http.DefaultClient.Do(q);x:=M{}
   json.NewDecoder(r.Body).Decode(&x);r.Body.Close();o:=x["output"].([]any);h=append(h,o...);c:=false
   for _,v:=range o{m:=v.(M);if m["type"]=="custom_tool_call"{
    c=true;p:=exec.Command("/bin/sh","-c",m["input"].(string));q,_:=p.CombinedOutput();n:=p.ProcessState.ExitCode()
    h=append(h,M{"type":"custom_tool_call_output","call_id":m["call_id"],"output":fmt.Sprintf("exit %d\n%s",n,q)})
   }}
   if !c{fmt.Printf("%s\n[%05.2f%%]\n",o[len(o)-1].(M)["content"].([]any)[0].(M)["text"],x["usage"].(M)["total_tokens"].(float64)/10500);break}
  }
 }
}

<?php
$u=$argv[1];$x=[];$k=bin2hex(random_bytes(16));
while(fwrite(STDOUT,"> ")&&($s=fgets(STDIN))!==false){
 if(!strlen(trim($s)))continue;
 $x[]=["role"=>"user","content"=>rtrim($s,"\r\n")];
 while(1){
  $b=json_encode(["model"=>"gpt-5.6-sol","input"=>$x,"tools"=>[["type"=>"custom","name"=>"sh"]]]);
  $r=json_decode(file_get_contents($u,0,stream_context_create(["http"=>[
   "method"=>"POST","header"=>"Content-Type: application/json\r\nsession_id: $k","content"=>$b
  ]])),1);$o=$r["output"];array_push($x,...$o);$c=0;
  foreach($o as $i)if($i["type"]=="custom_tool_call"){
   $c=1;$q=[];exec("/bin/sh -c ".escapeshellarg($i["input"])." 2>&1",$q,$n);
   $x[]=["type"=>"custom_tool_call_output","call_id"=>$i["call_id"],"output"=>"exit $n\n".implode("\n",$q)];
  }
  if(!$c){$i=end($o);printf("%s\n[%05.2f%%]\n",$i["content"][0]["text"],$r["usage"]["total_tokens"]/10500);break;}
 }
}

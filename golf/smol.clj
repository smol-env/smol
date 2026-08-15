(require '[babashka.http-client :as h]'[babashka.process :as p]'[cheshire.core :as j])
(let [u(first *command-line-args*) k(str(random-uuid))]
 (loop [x []](print "> ")(flush)
  (when-let [s(read-line)](recur(if(.isBlank s)x
    (loop [x(conj x {:role "user" :content s})]
     (let [r(->(h/post u {:headers {:content-type "application/json" :session_id k}
                          :body(j/encode {:model "gpt-5.6-sol" :input x :tools [{:type "custom" :name "sh"}]})})
                 :body(j/decode true))
           o(:output r) x(into x o) c(filter #(="custom_tool_call"(:type %))o)]
      (if(seq c)(recur(into x(for [i c]
        (let [z(p/sh {:err :out} "/bin/sh" "-c"(:input i))]
         {:type "custom_tool_call_output" :call_id(:call_id i) :output(format "exit %d\n%s"(:exit z)(:out z))}))))
       (do(printf "%s\n[%05.2f%%]\n"(-> o last :content first :text)(/(-> r :usage :total_tokens)10500.0))x)))))))))

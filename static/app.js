const $ = (id) => document.getElementById(id);

function setLoading(el, text="Thinking..."){el.className="output loading";el.textContent=text}
function setError(el,message){el.className="output error";el.textContent=message}
async function requestJson(url, options={}){
  const response=await fetch(url,{headers:{"Content-Type":"application/json",...(options.headers||{})},...options});
  const data=await response.json().catch(()=>({}));
  if(!response.ok) throw new Error(data.detail||data.error||`Request failed (${response.status})`);
  return data;
}

$("qaForm").addEventListener("submit",async(e)=>{
  e.preventDefault(); const out=$("qaResult"); setLoading(out);
  try{const q=encodeURIComponent($("question").value.trim());const d=await requestJson(`/qa?question=${q}`);out.textContent=d.answer}
  catch(err){setError(out,err.message)}
});
$("explainForm").addEventListener("submit",async(e)=>{
  e.preventDefault(); const out=$("explanationResult"); setLoading(out);
  try{const d=await requestJson("/explain/",{method:"POST",body:JSON.stringify({topic:$("topic").value.trim()})});out.textContent=d.explanation}
  catch(err){setError(out,err.message)}
});
$("summaryForm").addEventListener("submit",async(e)=>{
  e.preventDefault(); const out=$("summaryResult"); setLoading(out);
  try{const d=await requestJson("/summarize/",{method:"POST",body:JSON.stringify({text:$("summaryText").value.trim()})});out.textContent=d.summary}
  catch(err){setError(out,err.message)}
});
$("quizForm").addEventListener("submit",async(e)=>{
  e.preventDefault(); const out=$("quizResult"); setLoading(out);
  try{
    const d=await requestJson("/quiz",{method:"POST",body:JSON.stringify({text:$("quizText").value.trim()})});
    out.className="output";out.innerHTML="";
    d.quiz.forEach((item,i)=>{
      const box=document.createElement("div");box.className="quiz-item";
      const q=document.createElement("strong");q.textContent=`Q${i+1}: ${item.question}`;box.appendChild(q);
      item.options.forEach(option=>{const div=document.createElement("div");div.className="option";div.textContent=option;box.appendChild(div)});
      const ans=document.createElement("div");ans.className="answer";ans.textContent=`Answer: ${item.answer}`;box.appendChild(ans);
      out.appendChild(box);
    });
  }catch(err){setError(out,err.message)}
});
$("recommendForm").addEventListener("submit",async(e)=>{
  e.preventDefault(); const out=$("recommendResult"); setLoading(out);
  try{const t=encodeURIComponent($("recommendTopic").value.trim());const d=await requestJson(`/learn/recommendations?topic=${t}`);out.textContent=d.recommendation}
  catch(err){setError(out,err.message)}
});

/* practice exam: select answers, check, print */
(function(){
  const main=document.querySelector("main[data-exam]"); if(!main) return;
  const KEY="chem_exam_"+main.dataset.exam;
  const qs=[...document.querySelectorAll(".xq[data-a]")];
  let st={sel:{},score:null,total:qs.length};
  try{ st=Object.assign(st, JSON.parse(localStorage.getItem(KEY)||"{}")); }catch(e){}
  const save=()=>{ try{ localStorage.setItem(KEY, JSON.stringify(st)); }catch(e){} };
  const scoreEl=document.querySelector(".xscore");

  function paint(){
    qs.forEach(q=>{
      const sel=st.sel[q.id];
      q.querySelectorAll(".xo").forEach(b=>b.setAttribute("aria-pressed", String(b.dataset.i===String(sel))));
    });
  }
  function check(){
    document.body.classList.add("checked");
    let ok=0;
    qs.forEach(q=>{
      const a=q.dataset.a, sel=st.sel[q.id];
      q.querySelectorAll(".xo").forEach(b=>{ b.classList.toggle("right", b.dataset.i===a); b.classList.toggle("wrong", sel!=null && b.dataset.i===String(sel) && b.dataset.i!==a); });
      q.querySelector(".verdict")?.remove();
      const v=document.createElement("p"); v.className="verdict";
      if(String(sel)===a){ ok++; v.classList.add("ok"); v.textContent="✓ נכון"; }
      else { v.classList.add("no"); v.textContent= sel==null ? "לא סומנה תשובה" : "✗ לא נכון – כדאי לקרוא את הפתרון"; q.querySelector("details.xsol").open=true; }
      q.querySelector(".xopts").after(v);
    });
    st.score=ok; save();
    scoreEl.textContent=`ציון באמריקאיות: ${ok} מתוך ${qs.length} (${Math.round(100*ok/qs.length)}%). את השאלות הפתוחות בודקים מול הפתרונות.`;
  }
  qs.forEach(q=>q.querySelectorAll(".xo").forEach(b=>b.addEventListener("click",()=>{
    if(document.body.classList.contains("checked")) return;
    st.sel[q.id] = (String(st.sel[q.id])===b.dataset.i) ? null : Number(b.dataset.i);
    save(); paint();
  })));
  document.querySelectorAll("[data-act]").forEach(b=>b.addEventListener("click",()=>{
    const act=b.dataset.act;
    if(act==="check") check();
    if(act==="reset"){ st={sel:{},score:null,total:qs.length}; save(); document.body.classList.remove("checked");
      document.querySelectorAll(".verdict").forEach(v=>v.remove()); document.querySelectorAll(".xo").forEach(x=>x.classList.remove("right","wrong"));
      document.querySelectorAll("details.xsol").forEach(d=>d.open=false); scoreEl.textContent=""; paint(); window.scrollTo({top:0}); }
    if(act==="print-exam"){ document.body.classList.add("p-exam"); window.print(); document.body.classList.remove("p-exam"); }
    if(act==="print-key"){ const opened=[...document.querySelectorAll("details.xsol")].filter(d=>!d.open);
      opened.forEach(d=>d.open=true); qs.forEach(q=>q.querySelector(`.xo[data-i="${q.dataset.a}"]`).classList.add("right"));
      document.body.classList.add("p-key","checked"); window.print(); document.body.classList.remove("p-key");
      if(st.score==null){ document.body.classList.remove("checked"); qs.forEach(q=>q.querySelectorAll(".xo").forEach(x=>x.classList.remove("right"))); }
      opened.forEach(d=>d.open=false); }
  }));
  paint();
  if(st.score!=null) check();
})();

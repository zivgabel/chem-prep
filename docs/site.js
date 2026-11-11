/* formula cards: click to open an enlarged copy */
(function(){
  const dlg=document.createElement("dialog"); dlg.className="fzoom"; document.body.appendChild(dlg);
  document.querySelectorAll(".fcard").forEach(c=>{
    if(!c.querySelector(".zoom")){const z=document.createElement("span");z.className="zoom";z.textContent="⤢ הגדלה";c.appendChild(z);}
    c.tabIndex=0; c.setAttribute("role","button"); c.setAttribute("aria-label","הגדלת הנוסחה: "+(c.querySelector(".fname")||{}).textContent);
    const open=()=>{const part=c.closest("[data-part]"); dlg.innerHTML=""; if(part) dlg.dataset.part=part.dataset.part;
      const b=document.createElement("button");b.className="close";b.textContent="סגירה ✕";b.onclick=()=>dlg.close();
      const k=c.cloneNode(true); k.querySelector(".zoom")?.remove(); k.removeAttribute("tabindex"); k.removeAttribute("role");
      dlg.append(b,k); dlg.showModal();};
    c.addEventListener("click",open); c.addEventListener("keydown",e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();open();}});
  });
  dlg.addEventListener("click",e=>{if(e.target===dlg) dlg.close();});
})();

(function(){
  const r=document.documentElement, b=document.getElementById("themeBtn");
  try{ const t=localStorage.getItem("chem_theme"); if(t) r.dataset.theme=t; }catch(e){}
  b.onclick=()=>{ const dark = r.dataset.theme ? r.dataset.theme==="dark" : matchMedia("(prefers-color-scheme: dark)").matches;
    r.dataset.theme = dark ? "light" : "dark"; try{ localStorage.setItem("chem_theme", r.dataset.theme); }catch(e){} };
})();

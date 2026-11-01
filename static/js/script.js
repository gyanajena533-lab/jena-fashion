document.addEventListener("DOMContentLoaded", () => {
 const menu=document.getElementById("menuToggle"), nav=document.getElementById("navigation");
 const search=document.getElementById("productSearch"), form=document.getElementById("searchForm");
 const category=document.getElementById("categoryFilter"), sort=document.getElementById("priceSort");
 const grid=document.getElementById("productGrid"), message=document.getElementById("searchMessage"), empty=document.getElementById("emptyState");
 if(menu&&nav){menu.addEventListener("click",()=>nav.classList.toggle("open"));nav.querySelectorAll("a").forEach(a=>a.addEventListener("click",()=>nav.classList.remove("open")));}
 if(!grid)return;
 const cards=[...grid.querySelectorAll(".product-card")];
 function update(){
  const term=(search?.value||"").trim().toLowerCase(), cat=category?.value||"all", order=sort?.value||"default";
  const shown=cards.filter(c=>c.textContent.toLowerCase().includes(term)&&(cat==="all"||c.dataset.category===cat));
  shown.sort((a,b)=>order==="low-high"?+a.dataset.price- +b.dataset.price:order==="high-low"?+b.dataset.price- +a.dataset.price:cards.indexOf(a)-cards.indexOf(b));
  cards.forEach(c=>c.hidden=true);shown.forEach(c=>{c.hidden=false;grid.appendChild(c);});
  if(empty)empty.hidden=shown.length>0;if(message)message.textContent=term?`${shown.length} product(s) found.`:"";
 }
 search?.addEventListener("input",update);form?.addEventListener("submit",e=>{e.preventDefault();update();document.getElementById("products")?.scrollIntoView({behavior:"smooth"});});
 category?.addEventListener("change",update);sort?.addEventListener("change",update);
 let saved=[];try{saved=JSON.parse(localStorage.getItem("jenaWishlist")||"[]");}catch{saved=[];}
 function paint(){document.querySelectorAll(".wishlist-button").forEach(b=>{const id=b.closest(".product-card").dataset.id,yes=saved.includes(id);b.setAttribute("aria-pressed",String(yes));b.textContent=yes?"♥":"♡";});}
 document.querySelectorAll(".wishlist-button").forEach(b=>b.addEventListener("click",()=>{const id=b.closest(".product-card").dataset.id;saved=saved.includes(id)?saved.filter(x=>x!==id):[...saved,id];try{localStorage.setItem("jenaWishlist",JSON.stringify(saved));}catch{}paint();}));
 document.querySelectorAll("[data-category-link]").forEach(a=>a.addEventListener("click",()=>{if(category)category.value=a.dataset.categoryLink;update();}));
 document.getElementById("year").textContent=new Date().getFullYear();paint();update();
});
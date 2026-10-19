(function() {
'use strict';
const data = JSON.parse(document.getElementById('connections-data').textContent);
const C = window.Connections;
const $ = id => document.getElementById(id);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const F = Object.fromEntries(data.films.map(f => [f.id,f]));
const H = Object.fromEntries(data.hubs.map(h => [h.id,h]));
const sortedFilms = [...data.films].sort((a,b)=>a.t.localeCompare(b.t,'en'));
const poster = (f, eager=false) => f.img
  ? '<img class="poster" src="'+esc(f.img)+'" alt="" loading="'+(eager?'eager':'lazy')+'" width="120" height="180">'
  : '<span class="poster" aria-hidden="true">No poster</span>';
const filmLink = id => '<a href="'+esc(F[id].url)+'">'+esc(F[id].t)+'</a>';
const exploreLink = id => '<a class="note-link" href="#explore" data-explore="'+esc(id)+'">Follow '+esc(F[id].t)+' ↗</a>';
const sources = list => '<div class="sources">'+(list?.length ? list.map(([label,url])=>'<a href="'+esc(url)+'" target="_blank" rel="noopener">'+esc(label)+' ↗</a>').join('') : 'Library research notes')+'</div>';
const options = sortedFilms.map(f=>'<option value="'+esc(f.id)+'">'+esc(f.t)+' ('+f.y+')</option>').join('');
['film-select','route-from','route-to'].forEach(id=>$(id).innerHTML=options);
$('tally').innerHTML='<b>'+data.films.length+'</b> films · <b>'+data.direct.length+'</b> shared-credit pairs · <b>'+data.hubs.length+'</b> detours';
let selected = new URLSearchParams(location.search).get('film');
if(!F[selected]) selected = F['horror-hospital'] ? 'horror-hospital' : sortedFilms[0].id;
$('film-select').value=selected;
let showAll=false;
function chooseFilm(id, updateURL=true) {
  if(!F[id]) return;
  selected=id; $('film-select').value=id; showAll=false;
  if(updateURL) {
    const url=new URL(location.href);url.searchParams.set('film',id);history.replaceState(null,'',url);
  }
  renderFilm();
}
function renderFilm() {
  const f=F[selected], friends=C.neighbours(data,selected,$('credit-filter').value);
  $('focus-film').innerHTML=poster(f,true)+'<h3>'+esc(f.t)+'</h3><p>'+f.y+' · '+esc(f.c)+'</p><p>'+esc(f.d)+'</p><a href="'+esc(f.url)+'">Read the review ↗</a>';
  $('thread-summary').textContent=f.t+' · '+friends.length+' connected review'+(friends.length===1?'':'s')+' · '+($('credit-filter').value==='all'?'all shared credits':$('credit-filter').selectedOptions[0].text);
  const limit=showAll?friends.length:6;
  $('thread-map').innerHTML=friends.length ? friends.slice(0,limit).map(n=>{
    const friend=F[n.id];
    const via=n.via.map(p=>{
      const roles=[...new Set([...p.a,...p.b])].join(' / ');
      return esc(p.n)+' <small>('+esc(roles)+')</small>';
    }).join(' · ');
    return '<article class="thread-card">'+poster(friend)+'<div><span class="year">'+friend.y+'</span><h3><button type="button" data-film="'+esc(friend.id)+'">'+esc(friend.t)+'</button></h3><p class="credit-line">'+via+'</p></div></article>';
  }).join('') : '<p class="empty">No shared '+($('credit-filter').value==='all'?'credits':esc($('credit-filter').selectedOptions[0].text.toLowerCase()))+' in the current review credits. Try another filter, an outside detour or a thematic double bill.</p>';
  $('more-threads').hidden=friends.length<=6;
  $('more-threads').textContent=showAll?'Show fewer connections':'Show all '+friends.length+' connections';
  const hubs=data.hubs.filter(h=>Object.hasOwn(h.films,selected));
  $('detours').innerHTML=hubs.length?'<span>Take a detour via</span>'+hubs.map(h=>'<a href="#hub-'+esc(h.id)+'" data-hub="'+esc(h.id)+'">'+esc(h.name)+' ↗</a>').join(''):'<span>No outside detours recorded yet. This is an open end, not a dead end.</span>';
}
$('film-select').addEventListener('change',e=>chooseFilm(e.target.value));
$('credit-filter').addEventListener('change',()=>{showAll=false;renderFilm();});
$('more-threads').addEventListener('click',()=>{showAll=!showAll;renderFilm();});
$('random-film').addEventListener('click',()=>{
  const choices=sortedFilms.filter(f=>f.id!==selected);
  chooseFilm(choices[Math.floor(Math.random()*choices.length)].id);
});
document.addEventListener('click',e=>{
  const choice=e.target.closest('[data-film], [data-explore]');
  if(choice) {
    chooseFilm(choice.dataset.film || choice.dataset.explore);
    if(choice.dataset.film) $('film-select').focus({preventScroll:true});
  }
  const hub=e.target.closest('[data-hub]');
  if(hub) openHub(hub.dataset.hub);
});
function openHub(id) {
  const el=$('hub-'+id);
  if(!el) return;
  $('hub-search').value=''; filterHubs();
  el.closest('details').open=true;
}
window.addEventListener('hashchange',()=>{
  if(location.hash.startsWith('#hub-')) openHub(location.hash.slice(5));
});
function route() {
  const from=$('route-from').value, to=$('route-to').value, allow=$('allow-detours').checked;
  const path=C.shortestPath(C.network(data,allow),'f:'+from,'f:'+to);
  if(!path) {
    $('route-status').textContent='No route recorded between these films'+(allow?'. Try a different pair; selected credits do not cover every career.':'. Try allowing outside detours.');
    $('route-result').innerHTML=''; return;
  }
  const steps=path.length-1, outside=path.filter(p=>p.id.startsWith('h:')).length;
  $('route-status').textContent=steps===0?'You’re already there. Choose a different destination to explore a connection.':steps+' connecting step'+(steps===1?'':'s')+' · '+outside+' outside detour'+(outside===1?'':'s')+' · shortest recorded route';
  $('route-result').innerHTML=path.map((p,i)=>{
    const isFilm=p.id.startsWith('f:'), id=p.id.slice(2), item=isFilm?F[id]:H[id], next=path[i+1];
    const edge=next?.edge;
    const reason=edge ? (edge.kind==='credit' ? edge.via.map(v=>v.n+' ('+[...new Set([...v.a,...v.b])].join(' / ')+')').join(' · ') : edge.note) : '';
    return '<li class="route-stop'+(isFilm?'':' outside')+'"><small>'+(isFilm?'IN THE LIBRARY':'OUTSIDE DETOUR')+'</small>'+
      (isFilm?poster(item):'<div class="outside-stamp" aria-hidden="true">↝</div>')+
      '<h3>'+(isFilm?filmLink(id):esc(item.name))+'</h3><small>'+esc(isFilm?item.y:item.year)+'</small>'+
      (!isFilm?sources(item.sources):'')+(edge?'<p class="edge">↳ '+esc(reason)+'</p>':'')+'</li>';
  }).join('');
}
$('route-from').value='sugar-hill';$('route-to').value='horror-hospital';
$('route-form').addEventListener('submit',e=>{e.preventDefault();route();});
$('allow-detours').addEventListener('change',route);
$('route-from').addEventListener('change',route);$('route-to').addEventListener('change',route);
let billIndex=0;
function renderBill() {
  const bill=data.bills[billIndex];
  $('bill').innerHTML='<div class="bill-layout">'+bill.films.map(id=>'<div class="bill-film">'+poster(F[id])+filmLink(id)+'</div>').join('')+
    '<div class="bill-copy"><div class="ticket">ADMIT ONE / STAY FOR BOTH</div><span class="eyebrow">'+esc(bill.kind)+'</span><h3>'+esc(bill.title)+'</h3><p>'+esc(bill.text)+'</p></div></div>';
}
$('next-bill').addEventListener('click',()=>{billIndex=(billIndex+1)%data.bills.length;renderBill();});
$('dossiers').innerHTML=data.dossiers.map((d,i)=>'<article class="dossier"><div class="mini-posters">'+d.films.map(id=>'<a href="'+esc(F[id].url)+'" aria-label="'+esc(F[id].t)+'">'+poster(F[id])+'</a>').join('')+'</div><div class="eyebrow">'+String(i+1).padStart(2,'0')+' / '+esc(d.kicker)+'</div><h3>'+esc(d.title)+'</h3><p>'+esc(d.text)+'</p>'+sources(d.sources)+(d.hub?'<a class="note-link" href="#hub-'+esc(d.hub)+'" data-hub="'+esc(d.hub)+'">Explore this detour ↗</a>':exploreLink(d.films[0]))+'</article>').join('');
$('hub-count').textContent=data.hubs.length+' detours';
$('hub-list').innerHTML=[...data.hubs].sort((a,b)=>a.name.localeCompare(b.name,'en')).map(h=>
  '<article class="hub" id="hub-'+esc(h.id)+'"><h3>'+esc(h.name)+'</h3><div class="eyebrow">'+esc(h.year || '')+'</div><ul>'+Object.entries(h.films).map(([id,reason])=>'<li>'+filmLink(id)+esc(reason)+'</li>').join('')+'</ul>'+sources(h.sources)+'</article>').join('');
function filterHubs() {
  const q=$('hub-search').value.trim().toLocaleLowerCase();
  let visible=0;
  document.querySelectorAll('.hub').forEach(el=>{el.hidden=!el.textContent.toLocaleLowerCase().includes(q);if(!el.hidden)visible++;});
  let empty=$('hub-empty');
  if(!empty){empty=document.createElement('p');empty.id='hub-empty';empty.className='empty';$('hub-list').append(empty);}
  empty.textContent='No matching detours. Try a film, a person or a different spelling.';empty.hidden=visible>0;
}
$('hub-search').addEventListener('input',filterHubs);
let personIndex=0;
function renderPersonOptions() {
  const q=$('person-search').value.toLocaleLowerCase().trim();
  const people=data.rep.map((p,i)=>({p,i})).filter(({p})=>p.n.toLocaleLowerCase().includes(q));
  $('person-select').innerHTML=people.map(({p,i})=>'<option value="'+i+'">'+esc(p.n)+' · '+Object.keys(p.films).length+' films</option>').join('');
  if(!people.length) {$('person-select').disabled=true;$('person-timeline').innerHTML='<p class="empty">No recurring credit matches that name.</p>';return;}
  $('person-select').disabled=false;
  if(!people.some(({i})=>i===personIndex))personIndex=people[0].i;
  $('person-select').value=personIndex;renderPerson();
}
function renderPerson() {
  const p=data.rep[personIndex];
  $('person-timeline').innerHTML=Object.entries(p.films).sort(([a],[b])=>F[a].y-F[b].y||F[a].t.localeCompare(F[b].t,'en')).map(([id,roles])=>
    '<article class="career-film"><span class="year">'+F[id].y+'</span>'+poster(F[id])+'<h3>'+filmLink(id)+'</h3><p>'+esc(roles.join(' / '))+'</p></article>').join('');
}
$('person-select').addEventListener('change',e=>{personIndex=Number(e.target.value);renderPerson();});
$('person-search').addEventListener('input',renderPersonOptions);
$('clubs').innerHTML=[...data.clubs,...data.themes].map(g=>'<article><h3>'+esc(g.name)+'</h3><ul>'+Object.entries(g.films).map(([id,note])=>'<li>'+filmLink(id)+(note?' — '+esc(note):'')+'</li>').join('')+'</ul></article>').join('');
$('echoes').innerHTML=data.echoes.map(e=>'<article><h3>'+esc(e.src)+' <small>('+e.year+')</small></h3><p>Watch alongside '+filmLink(e.film)+'.</p><p>'+esc(e.note)+'</p></article>').join('');
$('aliases').innerHTML=data.aliases.map(a=>'<article><h3>'+esc(a.real)+'</h3><p>Also credited as '+esc(a.alias)+'</p><p>'+a.films.map(filmLink).join(' · ')+'</p></article>').join('')+
  data.clashes.map(c=>'<article><h3>'+esc(c.title)+'</h3><p>'+esc(c.note)+'</p><p>'+c.films.map(filmLink).join(' · ')+'</p></article>').join('');
renderFilm();route();renderBill();renderPersonOptions();
if(location.hash.startsWith('#hub-'))openHub(location.hash.slice(5));
})();

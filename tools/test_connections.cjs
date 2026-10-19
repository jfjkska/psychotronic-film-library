const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const C = require('../assets/js/connections-core.js');
const root = path.join(__dirname,'..');
const html = fs.readFileSync(path.join(root,'connections/index.html'),'utf8');
const data = JSON.parse(html.match(/<script id="connections-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
const pairs = (a,b,role='all') => C.neighbours(data,a,role).find(n=>n.id===b);
const expectedReviews = fs.readdirSync(path.join(root, '_posts')).filter(name => name.endsWith('.md') && !/^published:\s*false\s*$/m.test(fs.readFileSync(path.join(root, '_posts', name), 'utf8').split('---')[1])).map(name => name.replace(/^\d{4}-\d{2}-\d{2}-/, '').replace(/\.md$/, '')).sort();
assert.deepEqual(data.films.map(f => f.id).sort(), expectedReviews);
assert(data.films.some(f=>f.id==='horror-hospital'));
assert(!data.hubs.some(h=>h.id==='horror-hospital'),'A reviewed title must not also be an outside hub');
assert(pairs('horror-hospital','secrets-of-sex','director'));
assert(pairs('burial-ground','strip-nude-for-your-killer','music').via.some(p=>p.n==='Berto Pisano'),'Resolve the documented Burt Rexon alias');
assert(!pairs('silent-night-bloody-night','deathsport'),'Father and son are not a shared credit');
assert(!pairs('hands-of-steel','zombie-creeping-flesh'),'A member is not interchangeable with a band');
const franco=data.rep.find(p=>p.n==='Jess Franco');
assert.deepEqual(franco.films['she-killed-in-ecstasy'],['director','cast'],'Keep multiple roles on the same film');
assert.equal(data.rep.filter(p=>p.n==='Candace Glendenning').length,1);
const strict = C.network(data,false), expanded = C.network(data,true);
const pathTo=(graph,a,b)=>C.shortestPath(graph,'f:'+a,'f:'+b);
assert.equal(pathTo(strict,'sugar-hill','spider-baby'),null);
assert.deepEqual(pathTo(expanded,'sugar-hill','spider-baby').map(s=>s.id),['f:sugar-hill','h:thx-1138','f:spider-baby']);
assert.equal(pathTo(expanded,'apaches','the-finishing-line'),null,'Editorial pairings cannot manufacture a route');
assert.equal(pathTo(strict,'horror-hospital','horror-hospital').length,1);
assert.equal(pathTo(expanded,'missing','horror-hospital'),null);
const diamond = new Map([
 ['a',[{to:'b',edge:'ab'},{to:'c',edge:'ac'}]],
 ['b',[{to:'a',edge:'ab'},{to:'d',edge:'bd'}]],
 ['c',[{to:'a',edge:'ac'},{to:'d',edge:'cd'}]],
 ['d',[{to:'b',edge:'bd'},{to:'c',edge:'cd'}]]
]);
assert.deepEqual(C.shortestPath(diamond,'a','d'),[{id:'a',edge:null},{id:'b',edge:'ab'},{id:'d',edge:'bd'}]);
for(const graph of [strict,expanded]) {
  for(const [start] of graph) {
    // Independent layer expansion supplies the expected distance for every endpoint.
    const distance=new Map([[start,0]]);let frontier=[start],layer=0;
    while(frontier.length) {
      const next=[];layer++;
      frontier.forEach(id=>graph.get(id).forEach(({to})=>{if(!distance.has(to)){distance.set(to,layer);next.push(to);}}));
      frontier=next;
    }
    for(const [end] of graph) {
      const found=C.shortestPath(graph,start,end);
      assert.equal(found ? found.length-1 : undefined,distance.get(end));
      if(found) {
        assert.equal(new Set(found.map(p=>p.id)).size,found.length);
        found.slice(1).forEach((step,i)=>assert(graph.get(found[i].id).some(e=>e.to===step.id)));
      }
    }
  }
}
for(const f of data.films) if(f.img) assert(fs.existsSync(path.join(root,f.img)));
assert(html.includes('name="robots" content="noindex"'));
assert(html.includes('sitemap: false'));
assert(!html.includes('cdnjs.cloudflare.com'),'No CDN required');
console.log('Connections: metadata, aliases, role filters, all-pairs shortest routes, poster paths and draft flags passed.');

/* Pure graph operations shared by the page and its tests. */
(function(root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.Connections = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function() {
  'use strict';
  function credits(link, role) {
    return link.via.filter(p => role === 'all' || p.a.includes(role) || p.b.includes(role));
  }
  function neighbours(data, id, role = 'all') {
    const films = new Map(data.films.map(f => [f.id, f]));
    return data.direct.filter(l => l.a === id || l.b === id)
      .map(l => ({ id: l.a === id ? l.b : l.a, via: credits(l, role) }))
      .filter(l => l.via.length)
      .sort((a,b) => b.via.length - a.via.length || films.get(a.id).t.localeCompare(films.get(b.id).t, 'en'));
  }
  function network(data, detours = false) {
    const graph = new Map();
    function add(a,b,edge) {
      if(!graph.has(a)) graph.set(a,[]);
      if(!graph.has(b)) graph.set(b,[]);
      graph.get(a).push({to:b,edge}); graph.get(b).push({to:a,edge});
    }
    data.films.forEach(f => graph.set('f:'+f.id,[]));
    data.direct.forEach(l => add('f:'+l.a,'f:'+l.b,{kind:'credit',via:l.via, a:l.a,b:l.b}));
    if(detours) data.hubs.forEach(h => Object.entries(h.films).forEach(([f,note]) =>
      add('f:'+f,'h:'+h.id,{kind:'detour',note,sources:h.sources || []})));
    graph.forEach(edges => edges.sort((a,b) => a.to.localeCompare(b.to,'en')));
    return graph;
  }
  function shortestPath(graph, start, end) {
    if(!graph.has(start) || !graph.has(end)) return null;
    const seen = new Map([[start,null]]), queue=[start];
    for(let i=0;i<queue.length;i++) {
      const id=queue[i];
      if(id===end) {
        const path=[];
        for(let cur=end;cur!==null;) {
          const step=seen.get(cur);
          path.push({id:cur,edge:step ? step.edge : null});
          cur=step ? step.from : null;
        }
        return path.reverse();
      }
      for(const next of graph.get(id)) if(!seen.has(next.to)) {
        seen.set(next.to,{from:id,edge:next.edge}); queue.push(next.to);
      }
    }
    return null;
  }
  return {credits,neighbours,network,shortestPath};
});

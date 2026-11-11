(function (root) {
  'use strict';
  const keys = ['projects','signals','competitors','clients','opportunities','sources','reviews'];
  const norm = v => String(v || '').normalize('NFKC').trim().toLocaleLowerCase('es');
  function identity(key, row) {
    return [key, norm(row.name || row.title), norm(row.country)].join('|');
  }
  function normalize(value, legacy = false) {
    if (!value || typeof value !== 'object' || Array.isArray(value)) throw Error('Datos incompatibles');
    const result = {};
    if (!keys.some(k => Array.isArray(value[k]))) throw Error('Faltan los apartados de datos');
    for (const key of keys) {
      if (value[key] !== undefined && !Array.isArray(value[key])) throw Error('Apartado incompatible: ' + key);
      result[key] = (value[key] || []).map(row => {
        if (!row || typeof row !== 'object' || Array.isArray(row)) throw Error('Registro incompatible: ' + key);
        let item = {...row};
        if (legacy && key === 'signals') item = {...item, name: item.name || item.title, source: item.source || item.url};
        if (typeof item.name !== 'string' || !item.name.trim()) throw Error('Registro sin nombre: ' + key);
        for (const [field, val] of Object.entries(item)) {
          if (field.startsWith('_')) continue;
          if (!['string','number','boolean'].includes(typeof val) && val !== null) throw Error('Campo incompatible: ' + field);
        }
        return item;
      });
    }
    const meta = value._sync && typeof value._sync === 'object' ? value._sync : {};
    result._sync = {...meta, dismissed: Array.isArray(meta.dismissed) ? meta.dismissed.filter(x => typeof x === 'string') : []};
    return result;
  }
  function merge(local, feed, managed = true) {
    const next = normalize(local), incoming = normalize(feed, true);
    const dismissed = new Set(next._sync.dismissed);
    const stats = {added:0, updated:0, preserved:0, dismissed:0};
    for (const key of keys) {
      for (const raw of incoming[key]) {
        const item = Object.fromEntries(Object.entries(raw).filter(([k]) => !k.startsWith('_')));
        const token = key + ':' + (item.id || identity(key, item));
        if (managed && dismissed.has(token)) { stats.dismissed++; continue; }
        const index = next[key].findIndex(row => (item.id && row.id === item.id) || identity(key,row) === identity(key,item));
        if (index < 0) {
          next[key].push({...item, ...(managed ? {_feed: true, _feedToken: token} : {})}); stats.added++;
        } else if (managed && next[key][index]._feed) {
          // Preserve local extra fields; refresh only the public fields supplied by the feed.
          const previous = next[key][index];
          const replacement = {...previous, ...item, _feed:true, _feedToken:token};
          if (JSON.stringify(previous) !== JSON.stringify(replacement)) stats.updated++;
          next[key][index] = replacement;
        } else { stats.preserved++; }
      }
    }
    if (managed) {
      next._sync.generatedAt = String(feed.generatedAt || '');
      next._sync.coverage = String(feed.coverage || '');
      next._sync.lastSuccess = new Date().toISOString();
    }
    return {state:next, stats};
  }
  function dismiss(state, key, index) {
    const next = normalize(state), row = next[key][index];
    if (!row) return next;
    if (row._feedToken && !next._sync.dismissed.includes(row._feedToken)) next._sync.dismissed.push(row._feedToken);
    next[key].splice(index,1);
    return next;
  }
  const api = {keys, normalize, merge, dismiss, identity};
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.PCTSync = api;
})(typeof globalThis === 'object' ? globalThis : this);

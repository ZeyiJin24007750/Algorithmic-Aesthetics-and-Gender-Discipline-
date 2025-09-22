
async function loadCSV(path) {
  const res = await fetch(path + '?cache=' + Date.now());
  const text = await res.text();
  const [headerLine, ...lines] = text.split(/\r?\n/).filter(Boolean);
  const headers = headerLine.split(',');
  return lines.map(line => {
    // naive CSV split (no embedded commas expected in our schema)
    const cols = line.split(',');
    const row = {};
    headers.forEach((h, i) => row[h] = (cols[i] || '').trim());
    return row;
  });
}

function normalize(s){ return (s||'').toLowerCase(); }

function render(items) {
  const grid = document.querySelector('.grid');
  grid.innerHTML = '';
  for (const r of items) {
    const img = `../screenshots/${r.filename}`;
    const card = document.createElement('a');
    card.href = img;
    card.target = '_blank';
    card.rel = 'noopener';
    card.className = 'card';
    card.innerHTML = `
      <img class="thumb" src="${img}" alt="${r.filter_name || r.filename}">
      <div class="meta">
        <div class="f">${r.filter_name || '(unknown)'} <span class="chip">${r.filename}</span></div>
        <div class="row"><span>Whitening</span><span>${r.whitening_value || '-'}</span></div>
        <div class="row"><span>Face Slim</span><span>${r.face_slim_ratio || '-'}</span></div>
        <div class="row"><span>Captured</span><span>${r.captured_at || '-'}</span></div>
      </div>`;
    grid.appendChild(card);
  }
  document.querySelector('.count').textContent = items.length + ' items';
}

function unique(list, key){
  const set = new Set(list.map(x => x[key]).filter(Boolean).map(x=>x.toLowerCase()));
  return ['All', ...Array.from(set).sort((a,b)=>a.localeCompare(b)).map(s => s)];
}

(async function(){
  const rows = await loadCSV('../data/metadata.csv');
  const filterSelect = document.querySelector('#filterName');
  const search = document.querySelector('#searchBox');

  // populate filter names
  for (const name of unique(rows, 'filter_name')) {
    const opt = document.createElement('option');
    opt.value = name;
    opt.textContent = name;
    filterSelect.appendChild(opt);
  }

  function apply() {
    const q = normalize(search.value);
    const chosen = normalize(filterSelect.value);
    let list = rows;
    if (chosen && chosen !== 'all') {
      list = list.filter(r => normalize(r.filter_name) === chosen);
    }
    if (q) {
      list = list.filter(r =>
        normalize(r.filter_name).includes(q) ||
        normalize(r.filename).includes(q) ||
        normalize(r.tags).includes(q) ||
        normalize(r.notes).includes(q)
      );
    }
    render(list);
  }

  search.addEventListener('input', apply);
  filterSelect.addEventListener('change', apply);
  apply();
})();

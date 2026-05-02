const runBtn = document.getElementById('runBtn');
const resultsEl = document.getElementById('results');
const summaryEl = document.getElementById('summary');

function esc(x) { return String(x ?? '').replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m])); }

async function run() {
  const rank = document.getElementById('rank').value;
  const rankType = document.getElementById('rankType').value;
  const includePartial = document.getElementById('includePartial').checked;
  const url = `/api/simulate?rank=${encodeURIComponent(rank)}&rank_type=${encodeURIComponent(rankType)}&include_partial=${includePartial}&max_results=20`;
  resultsEl.innerHTML = '<div class="card">Loading...</div>';
  const res = await fetch(url);
  const data = await res.json();
  summaryEl.innerHTML = `<div class="card"><strong>Data version:</strong> ${esc(data.data_version)}<br><strong>Safety gate:</strong> ${esc(data.safety_gate)}<br><strong>Returned:</strong> ${esc(data.counts?.visible_returned)} / loaded ${esc(data.counts?.total_loaded)}. Default publishable total: ${esc(data.counts?.default_publishable_total)}.</div>`;
  resultsEl.innerHTML = '';
  for (const r of data.results || []) {
    const div = document.createElement('article');
    div.className = 'result';
    div.innerHTML = `
      <h3>${esc(r.college)} — ${esc(r.program)}</h3>
      <p>${esc(r.route)}</p>
      <div class="tags">
        <span class="tag">${esc(r.admission_bucket)}</span>
        <span class="tag">Job score: ${esc(r.job_strength_score ?? 'N/A')}</span>
        <span class="tag">Confidence: ${esc(r.placement_confidence ?? 'N/A')}</span>
        <span class="tag">${r.publish_default ? 'Default visible' : 'Internal only'}</span>
      </div>
      ${(r.warnings || []).map(w => `<div class="warn">${esc(w)}</div>`).join('')}
      <p><a href="/api/sources/${encodeURIComponent(r.program_key)}" target="_blank">Open source drawer JSON</a></p>
    `;
    resultsEl.appendChild(div);
  }
  if (!data.results?.length) resultsEl.innerHTML = '<div class="card">No rows visible under the current safety gate.</div>';
}

runBtn.addEventListener('click', run);
run();

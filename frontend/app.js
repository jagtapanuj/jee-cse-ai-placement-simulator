const runBtn = document.getElementById('runBtn');
const resultsEl = document.getElementById('results');
const summaryEl = document.getElementById('summary');
const dataQualityEl = document.getElementById('dataQuality');
const drawerEl = document.getElementById('drawer');
const drawerContentEl = document.getElementById('drawerContent');
const closeDrawerBtn = document.getElementById('closeDrawer');

function esc(x) {
  return String(x ?? '').replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
}

async function loadDataQuality() {
  const res = await fetch('/api/data-quality');
  const data = await res.json();
  const s = data.summary || {};
  dataQualityEl.innerHTML = `
    <div class="card grid-4">
      <div><strong>Total rows</strong><br>${esc(s.total_program_rows)}</div>
      <div><strong>Default visible</strong><br>${esc(s.default_visible_rows)}</div>
      <div><strong>Hidden pending</strong><br>${esc(s.hidden_pending_verification_rows)}</div>
      <div><strong>Sources</strong><br>${esc(s.source_register_rows)}</div>
    </div>
    <div class="card small"><strong>Safety gate:</strong> ${esc(data.safety_gate)}</div>
  `;
}

async function openSourceDrawer(programKey) {
  drawerContentEl.innerHTML = '<p>Loading source evidence...</p>';
  drawerEl.classList.remove('hidden');

  const res = await fetch(`/api/sources/${encodeURIComponent(programKey)}`);
  const data = await res.json();

  const p = data.program || {};
  const sourceLinks = (data.program_source_urls || [])
    .map((u, idx) => `<li><a href="${esc(u)}" target="_blank" rel="noreferrer">Source ${idx + 1}</a></li>`)
    .join('');

  const audits = data.quality_audit || [];

  drawerContentEl.innerHTML = `
    <h2>${esc(p.college)} — ${esc(p.program)}</h2>
    <p class="muted">${esc(p.route)}</p>
    <div class="warning">${esc(data.warning || '')}</div>

    <h3>Publication status</h3>
    <table>
      <tr><th>Default visible</th><td>${p.publish_default ? 'Yes' : 'No — internal only'}</td></tr>
      <tr><th>Data quality</th><td>${esc(p.data_quality_status)}</td></tr>
      <tr><th>Why not ready</th><td>${esc(p.why_not_ready || 'No blocker recorded')}</td></tr>
      <tr><th>Manual verification required</th><td>${data.manual_verification_required ? 'Yes' : 'No for pilot gate'}</td></tr>
    </table>

    <h3>Admission evidence</h3>
    <table>
      <tr><th>Cutoff status</th><td>${esc(p.admission_cutoff_status)}</td></tr>
      <tr><th>Seat type</th><td>${esc(p.admission_seat_type)}</td></tr>
      <tr><th>Closing rank/merit</th><td>${esc(p.closing_rank_or_merit ?? 'Not published/verified')}</td></tr>
      <tr><th>Closing score</th><td>${esc(p.closing_score ?? 'Not published/verified')}</td></tr>
    </table>

    <h3>Placement and score evidence</h3>
    <table>
      <tr><th>Placement status</th><td>${esc(p.placement_status)}</td></tr>
      <tr><th>Placement confidence</th><td>${esc(p.placement_confidence ?? 'N/A')}</td></tr>
      <tr><th>Placement score</th><td>${esc(p.placement_score ?? 'N/A')}</td></tr>
      <tr><th>Salary score</th><td>${esc(p.salary_score ?? 'N/A')}</td></tr>
      <tr><th>ROI score, fee only</th><td>${esc(p.roi_score_fee_only ?? 'N/A')}</td></tr>
      <tr><th>Internal job score</th><td>${esc(p.internal_job_score_v3 ?? 'N/A')}</td></tr>
    </table>

    <h3>Source links</h3>
    <ul>${sourceLinks || '<li>No source URL attached. Do not publish.</li>'}</ul>

    <h3>Quality audit rows</h3>
    ${
      audits.length
        ? audits.map(a => `<div class="audit"><strong>${esc(a.field || a.check || 'Audit')}</strong><br>${esc(JSON.stringify(a))}</div>`).join('')
        : '<p class="muted">No row-level audit entries available yet.</p>'
    }
  `;
}

async function run() {
  const rank = document.getElementById('rank').value;
  const rankType = document.getElementById('rankType').value;
  const includePartial = document.getElementById('includePartial').checked;
  const url = `/api/simulate?rank=${encodeURIComponent(rank)}&rank_type=${encodeURIComponent(rankType)}&include_partial=${includePartial}&max_results=20`;

  resultsEl.innerHTML = '<div class="card">Loading...</div>';

  const res = await fetch(url);
  const data = await res.json();

  summaryEl.innerHTML = `
    <div class="card">
      <strong>Data version:</strong> ${esc(data.data_version)}<br>
      <strong>Safety gate:</strong> ${esc(data.safety_gate)}<br>
      <strong>Returned:</strong> ${esc(data.counts?.visible_returned)} / loaded ${esc(data.counts?.total_loaded)}.
      Default publishable total: ${esc(data.counts?.default_publishable_total)}.
    </div>
  `;

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
      <button class="secondary source-btn" data-program-key="${esc(r.program_key)}">Open readable source drawer</button>
    `;
    resultsEl.appendChild(div);
  }

  if (!data.results?.length) {
    resultsEl.innerHTML = '<div class="card">No rows visible under the current safety gate.</div>';
  }
}

resultsEl.addEventListener('click', (event) => {
  const target = event.target;
  if (target.classList.contains('source-btn')) {
    openSourceDrawer(target.dataset.programKey);
  }
});

closeDrawerBtn.addEventListener('click', () => drawerEl.classList.add('hidden'));

drawerEl.addEventListener('click', (event) => {
  if (event.target === drawerEl) drawerEl.classList.add('hidden');
});

runBtn.addEventListener('click', run);

loadDataQuality();
run();

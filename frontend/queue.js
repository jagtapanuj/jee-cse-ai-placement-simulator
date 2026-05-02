const queueSummaryEl = document.getElementById('queueSummary');
const queueEl = document.getElementById('queue');
const filterBox = document.getElementById('filterBox');
const statusFilter = document.getElementById('statusFilter');
const refreshBtn = document.getElementById('refreshBtn');

let queueData = null;

function esc(x) {
  return String(x ?? '').replace(/[&<>"']/g, m => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  }[m]));
}

function blockerPriority(row) {
  const cutoff = String(row.admission_cutoff_status || '').toLowerCase();
  const quality = String(row.data_quality_status || '').toLowerCase();
  const reason = String(row.why_not_ready || '').toLowerCase();

  if (cutoff.includes('no_verified_cutoff') || cutoff.includes('staged')) return 'P0 cutoff verification';
  if (quality.includes('partial') || reason.includes('denominator') || reason.includes('median')) return 'P0 placement/denominator verification';
  if (reason.includes('fee')) return 'P1 fee verification';
  return 'P1 review needed';
}

function populateStatusFilter(rows) {
  const current = statusFilter.value;
  const statuses = Array.from(new Set(rows.map(r => r.data_quality_status || 'UNKNOWN'))).sort();

  statusFilter.innerHTML = '<option value="">All statuses</option>';
  for (const status of statuses) {
    const option = document.createElement('option');
    option.value = status;
    option.textContent = status;
    statusFilter.appendChild(option);
  }
  statusFilter.value = current;
}

function filteredRows() {
  if (!queueData) return [];

  const q = filterBox.value.trim().toLowerCase();
  const status = statusFilter.value;

  return (queueData.hidden_blockers || []).filter(row => {
    if (status && row.data_quality_status !== status) return false;
    if (!q) return true;

    const text = [
      row.program_key,
      row.college,
      row.program,
      row.route,
      row.data_quality_status,
      row.placement_status,
      row.admission_cutoff_status,
      row.why_not_ready,
      blockerPriority(row)
    ].join(' ').toLowerCase();

    return text.includes(q);
  });
}

function renderQueue() {
  if (!queueData) return;

  const s = queueData.summary || {};
  const rows = filteredRows();

  queueSummaryEl.innerHTML = `
    <div class="card grid-4">
      <div><strong>Total rows</strong><br>${esc(s.total_program_rows)}</div>
      <div><strong>Default visible</strong><br>${esc(s.default_visible_rows)}</div>
      <div><strong>Hidden pending</strong><br>${esc(s.hidden_pending_verification_rows)}</div>
      <div><strong>Sources</strong><br>${esc(s.source_register_rows)}</div>
    </div>
    <div class="card small">
      <strong>Safety gate:</strong> ${esc(queueData.safety_gate)}
    </div>
    <div class="card small">
      Showing ${esc(rows.length)} hidden row(s) after filters.
    </div>
  `;

  if (!rows.length) {
    queueEl.innerHTML = '<div class="card">No hidden rows match the current filters.</div>';
    return;
  }

  queueEl.innerHTML = '';
  rows.forEach(row => {
    const item = document.createElement('article');
    item.className = 'result';
    item.innerHTML = `
      <h3>${esc(row.college)} — ${esc(row.program)}</h3>
      <p>${esc(row.route)}</p>

      <div class="tags">
        <span class="tag">${esc(blockerPriority(row))}</span>
        <span class="tag">${esc(row.data_quality_status)}</span>
        <span class="tag">Sources: ${esc(row.source_count)}</span>
      </div>

      <table>
        <tr><th>Program key</th><td>${esc(row.program_key)}</td></tr>
        <tr><th>Admission cutoff status</th><td>${esc(row.admission_cutoff_status)}</td></tr>
        <tr><th>Placement status</th><td>${esc(row.placement_status)}</td></tr>
        <tr><th>Why not ready</th><td>${esc(row.why_not_ready || 'No blocker note recorded')}</td></tr>
        <tr><th>Next action</th><td>${esc(blockerPriority(row))}</td></tr>
      </table>

      <div class="warn">
        Internal only. Do not make this row default-visible until the verification checklist is complete.
      </div>
    `;
    queueEl.appendChild(item);
  });
}

async function loadQueue() {
  queueEl.innerHTML = '<div class="card">Loading verification queue...</div>';

  const res = await fetch('/api/data-quality');
  queueData = await res.json();

  populateStatusFilter(queueData.hidden_blockers || []);
  renderQueue();
}

filterBox.addEventListener('input', renderQueue);
statusFilter.addEventListener('change', renderQueue);
refreshBtn.addEventListener('click', loadQueue);

loadQueue();

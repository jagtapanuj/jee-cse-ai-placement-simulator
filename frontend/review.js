const programSummaryEl = document.getElementById('programSummary');
const sourceEvidenceEl = document.getElementById('sourceEvidence');
const reviewNotesEl = document.getElementById('reviewNotes');
const lastCheckedDateEl = document.getElementById('lastCheckedDate');
const saveReviewBtn = document.getElementById('saveReviewBtn');
const exportReviewBtn = document.getElementById('exportReviewBtn');
const clearReviewBtn = document.getElementById('clearReviewBtn');
const exportBox = document.getElementById('exportBox');

const params = new URLSearchParams(window.location.search);
const programKey = params.get('program_key');

let drawerData = null;

function esc(x) {
  return String(x ?? '').replace(/[&<>"']/g, m => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  }[m]));
}

function storageKey() {
  return `review-checklist:${programKey || 'unknown'}`;
}

function checklistState() {
  const checks = {};
  document.querySelectorAll('[data-check]').forEach(input => {
    checks[input.dataset.check] = input.checked;
  });
  return checks;
}

function setChecklistState(checks) {
  document.querySelectorAll('[data-check]').forEach(input => {
    input.checked = Boolean(checks && checks[input.dataset.check]);
  });
}

function loadLocalReview() {
  const raw = localStorage.getItem(storageKey());
  if (!raw) return;

  try {
    const saved = JSON.parse(raw);
    setChecklistState(saved.checks || {});
    reviewNotesEl.value = saved.review_notes || '';
    lastCheckedDateEl.value = saved.last_checked_date || '';
  } catch {
    localStorage.removeItem(storageKey());
  }
}

function buildReviewPayload() {
  return {
    program_key: programKey,
    saved_at: new Date().toISOString(),
    local_only: true,
    checks: checklistState(),
    review_notes: reviewNotesEl.value,
    last_checked_date: lastCheckedDateEl.value,
    program_snapshot: drawerData?.program || null,
    source_urls: drawerData?.program_source_urls || [],
    manual_verification_required: drawerData?.manual_verification_required ?? true
  };
}

function saveLocalReview() {
  localStorage.setItem(storageKey(), JSON.stringify(buildReviewPayload(), null, 2));
  exportBox.classList.remove('hidden');
  exportBox.textContent = 'Saved locally in this browser. This did not change the dataset.';
}

function exportReview() {
  const payload = buildReviewPayload();
  exportBox.classList.remove('hidden');
  exportBox.textContent = JSON.stringify(payload, null, 2);
}

function clearReview() {
  localStorage.removeItem(storageKey());
  setChecklistState({});
  reviewNotesEl.value = '';
  lastCheckedDateEl.value = '';
  exportBox.classList.remove('hidden');
  exportBox.textContent = 'Local review cleared. Dataset was not changed.';
}

function renderProgram(data) {
  const p = data.program || {};
  const sourceLinks = (data.program_source_urls || [])
    .map((url, i) => `<li><a href="${esc(url)}" target="_blank" rel="noreferrer">Program source ${i + 1}</a></li>`)
    .join('');

  programSummaryEl.innerHTML = `
    <div class="card">
      <h2>${esc(p.college)} — ${esc(p.program)}</h2>
      <p class="muted">${esc(p.route)}</p>
      <div class="tags">
        <span class="tag">${p.publish_default ? 'Default visible' : 'Internal only'}</span>
        <span class="tag">${esc(p.data_quality_status)}</span>
        <span class="tag">Sources: ${esc((data.program_source_urls || []).length)}</span>
      </div>
      <div class="warning">${esc(data.warning || '')}</div>
    </div>
  `;

  sourceEvidenceEl.innerHTML = `
    <article class="result">
      <h3>Admission evidence</h3>
      <table>
        <tr><th>Cutoff status</th><td>${esc(p.admission_cutoff_status)}</td></tr>
        <tr><th>Seat type</th><td>${esc(p.admission_seat_type)}</td></tr>
        <tr><th>Closing rank/merit</th><td>${esc(p.closing_rank_or_merit ?? 'Not published/verified')}</td></tr>
        <tr><th>Closing score</th><td>${esc(p.closing_score ?? 'Not published/verified')}</td></tr>
      </table>
    </article>

    <article class="result">
      <h3>Placement and score evidence</h3>
      <table>
        <tr><th>Placement status</th><td>${esc(p.placement_status)}</td></tr>
        <tr><th>Placement confidence</th><td>${esc(p.placement_confidence ?? 'N/A')}</td></tr>
        <tr><th>Placement score</th><td>${esc(p.placement_score ?? 'N/A')}</td></tr>
        <tr><th>Salary score</th><td>${esc(p.salary_score ?? 'N/A')}</td></tr>
        <tr><th>ROI score, fee only</th><td>${esc(p.roi_score_fee_only ?? 'N/A')}</td></tr>
        <tr><th>Internal job score</th><td>${esc(p.internal_job_score_v3 ?? 'N/A')}</td></tr>
      </table>
    </article>

    <article class="result">
      <h3>Source links</h3>
      <ul>${sourceLinks || '<li>No source URL attached. Do not publish.</li>'}</ul>
    </article>

    <article class="result">
      <h3>Quality audit rows</h3>
      ${
        (data.quality_audit || []).length
          ? data.quality_audit.map(a => `<div class="audit">${esc(JSON.stringify(a))}</div>`).join('')
          : '<p class="muted">No row-level audit entries available yet.</p>'
      }
    </article>
  `;
}

async function init() {
  if (!programKey) {
    programSummaryEl.innerHTML = '<div class="card">No program_key supplied. Open this page from the verification queue.</div>';
    return;
  }

  programSummaryEl.innerHTML = '<div class="card">Loading program evidence...</div>';

  const res = await fetch(`/api/sources/${encodeURIComponent(programKey)}`);
  drawerData = await res.json();

  renderProgram(drawerData);
  loadLocalReview();
}

saveReviewBtn.addEventListener('click', saveLocalReview);
exportReviewBtn.addEventListener('click', exportReview);
clearReviewBtn.addEventListener('click', clearReview);

init();

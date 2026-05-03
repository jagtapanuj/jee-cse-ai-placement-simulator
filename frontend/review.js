const programSummaryEl = document.getElementById('programSummary');
const publicationReviewEl = document.getElementById('publicationReview');
const sourceEvidenceEl = document.getElementById('sourceEvidence');
const reviewNotesEl = document.getElementById('reviewNotes');
const lastCheckedDateEl = document.getElementById('lastCheckedDate');
const saveReviewBtn = document.getElementById('saveReviewBtn');
const exportReviewBtn = document.getElementById('exportReviewBtn');
const clearReviewBtn = document.getElementById('clearReviewBtn');
const exportBox = document.getElementById('exportBox');

const params = new URLSearchParams(window.location.search);
const programKey = params.get('program_key');

let publicationData = null;

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
    publication_summary: publicationData?.summary || null,
    publication_checks: publicationData?.checks || [],
    pending_or_failed_check_keys: publicationData?.pending_or_failed_check_keys || [],
    rules: publicationData?.rules || [],
    program_snapshot: publicationData?.program || null
  };
}

function saveLocalReview() {
  localStorage.setItem(storageKey(), JSON.stringify(buildReviewPayload(), null, 2));
  exportBox.classList.remove('hidden');
  exportBox.textContent = 'Saved locally in this browser. This did not change the dataset or publish status.';
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
  const s = data.summary || {};
  const sourceLinks = (p.source_urls || [])
    .map((url, i) => `<li><a href="${esc(url)}" target="_blank" rel="noreferrer">Program source ${i + 1}</a></li>`)
    .join('');

  const publishMessage = s.can_publish_default
    ? 'All required source gates pass in the publication-review API.'
    : 'Publication blocked. Do not set publish_default=yes until every required check passes.';

  programSummaryEl.innerHTML = `
    <div class="card">
      <h2>${esc(p.college)} — ${esc(p.program)}</h2>
      <p class="muted">${esc(p.route)}</p>
      <div class="tags">
        <span class="tag">${p.publish_default ? 'Default visible' : 'Internal only'}</span>
        <span class="tag">${esc(p.data_quality_status)}</span>
        <span class="tag">Required checks: ${esc(s.passed_required_checks)} / ${esc(s.required_checks)}</span>
        <span class="tag">${s.can_publish_default ? 'Can publish' : 'Cannot publish'}</span>
      </div>
      <div class="warning">${esc(publishMessage)}</div>
    </div>
  `;

  sourceEvidenceEl.innerHTML = `
    <article class="result">
      <h3>Source links from publication-review payload</h3>
      <ul>${sourceLinks || '<li>No source URL attached. Do not publish.</li>'}</ul>
    </article>

    <article class="result">
      <h3>Current row snapshot</h3>
      <table>
        <tr><th>Program key</th><td>${esc(p.program_key)}</td></tr>
        <tr><th>Admission cutoff status</th><td>${esc(p.admission_cutoff_status)}</td></tr>
        <tr><th>Placement status</th><td>${esc(p.placement_status)}</td></tr>
        <tr><th>Placement confidence</th><td>${esc(p.placement_confidence ?? 'N/A')}</td></tr>
        <tr><th>Internal job score</th><td>${esc(p.internal_job_score_v3 ?? 'N/A')}</td></tr>
        <tr><th>Why not ready</th><td>${esc(p.why_not_ready || 'No blocker note recorded')}</td></tr>
      </table>
    </article>
  `;
}

function renderPublicationReview(data) {
  const s = data.summary || {};
  const pendingKeys = data.pending_or_failed_check_keys || [];
  const checks = data.checks || [];
  const rules = data.rules || [];

  const rows = checks.map(check => {
    const statusText = check.passed ? 'Passed' : esc(check.status || 'missing');
    const rowWarning = check.passed
      ? ''
      : `<div class="warn">Required blocker: ${esc(check.notes || 'This check has not passed yet.')}</div>`;

    return `
      <tr>
        <td>
          <strong>${esc(check.check_name || check.check_key)}</strong><br>
          <span class="muted">${esc(check.description)}</span>
        </td>
        <td>${String(check.required_for_v1).toLowerCase() === 'yes' ? 'Yes' : 'No'}</td>
        <td>${statusText}${rowWarning}</td>
        <td>${esc(check.review_source || 'No review source recorded')}</td>
        <td>
          ${esc(check.reviewed_by || 'Unreviewed')}<br>
          <span class="muted">${esc(check.reviewed_at || '')}</span>
        </td>
      </tr>
    `;
  }).join('');

  publicationReviewEl.innerHTML = `
    <div class="card grid-4">
      <div><strong>Required checks</strong><br>${esc(s.required_checks)}</div>
      <div><strong>Passed</strong><br>${esc(s.passed_required_checks)}</div>
      <div><strong>Pending/failed</strong><br>${esc(s.pending_or_failed_required_checks)}</div>
      <div><strong>Publish gate</strong><br>${s.can_publish_default ? 'Open' : 'Blocked'}</div>
    </div>

    <div class="card small">
      <strong>Required checks all passed:</strong> ${s.all_required_checks_passed ? 'Yes' : 'No'}<br>
      <strong>can_publish_default:</strong> ${s.can_publish_default ? 'true' : 'false'}<br>
      <strong>Pending/failed check keys:</strong> ${pendingKeys.length ? esc(pendingKeys.join(', ')) : 'None'}
    </div>

    <article class="result">
      <h3>v1.0 publication checks</h3>
      <table>
        <tr>
          <th>Check</th>
          <th>Required for v1.0</th>
          <th>Status</th>
          <th>Review source</th>
          <th>Reviewed</th>
        </tr>
        ${rows}
      </table>
    </article>

    <article class="result">
      <h3>Publication rules</h3>
      <ul>${rules.map(rule => `<li>${esc(rule)}</li>`).join('')}</ul>
    </article>
  `;
}

async function init() {
  if (!programKey) {
    programSummaryEl.innerHTML = '<div class="card">No program_key supplied. Open this page from the verification queue.</div>';
    return;
  }

  programSummaryEl.innerHTML = '<div class="card">Loading publication review...</div>';

  const res = await fetch(`/api/publication-review/${encodeURIComponent(programKey)}`);
  publicationData = await res.json();

  if (!res.ok || publicationData.error) {
    programSummaryEl.innerHTML = `<div class="card">Unable to load publication review: ${esc(publicationData.error || res.statusText)}</div>`;
    return;
  }

  renderProgram(publicationData);
  renderPublicationReview(publicationData);
  loadLocalReview();
}

saveReviewBtn.addEventListener('click', saveLocalReview);
exportReviewBtn.addEventListener('click', exportReview);
clearReviewBtn.addEventListener('click', clearReview);

init();

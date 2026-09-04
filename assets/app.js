const ROOT = window.location.pathname.includes('/strong-formulation/') ? '/strong-formulation/' : '/';

async function getJSON(name){
  const response = await fetch(`${ROOT}data/${name}.json`);
  if(!response.ok) throw new Error(`${name}: ${response.status}`);
  return response.json();
}

function sourceHref(){
  return 'https://github.com/TitanicParker/strong-formulation/blob/main/SRC_COMPLETE_RECORD_FORENSIC.md';
}

function evidenceStatus(e){
  return e.id === 'E008' ? 'established case fact' : e.status;
}

function evidenceProposition(e){
  return e.id === 'E008'
    ? 'Before closure, the patient directly challenged the adequacy of the foot disposition. The Protest is established; its omission from the portable founding account is the documentary event under examination.'
    : e.proposition;
}

function evidenceHTML(e){
  return `<article class="evidence-card" id="${e.id}">
    <div class="meta"><span class="badge">${e.id}</span><span class="badge">${evidenceStatus(e)}</span></div>
    <h3>${evidenceProposition(e)}</h3>
    <p class="quote">“${e.quote}”</p>
    ${e.secondary_quote ? `<p><strong>Related extract:</strong> “${e.secondary_quote}”</p>` : ''}
    <p><strong>Why it matters:</strong> ${e.significance}</p>
    <p class="source-link">${e.document} · ${e.date} · <a href="${sourceHref(e)}">${e.clin_start}–${e.clin_end}</a></p>
    ${e.id === 'E008' ? '<p class="meta"><strong>Audit rule:</strong> the absence of the Protest from the portable founding synthesis is not negative evidence against the Protest; that absence is the alleged omission.</p>' : ''}
  </article>`;
}

async function renderEvidence(target='evidence-list'){
  const el = document.getElementById(target);
  if(!el) return;
  try {
    const data = await getJSON('evidence-index');
    el.innerHTML = data.map(evidenceHTML).join('');
  } catch (error) {
    el.innerHTML = '<p class="notice">Evidence data could not be loaded in this view.</p>';
  }
}

async function renderTimeline(){
  const el = document.getElementById('timeline-list');
  if(!el) return;
  const events = await getJSON('timeline');
  el.innerHTML = events.map(x => `<div class="event"><time>${x.date}</time><h3>${x.label}</h3><p>${x.significance}</p><p class="meta">Evidence: ${x.evidence.join(', ')}</p></div>`).join('');
}

async function renderKnowledge(){
  const body = document.getElementById('knowledge-body');
  if(!body) return;
  const rows = await getJSON('knowledge-state');
  body.innerHTML = rows.map(r => `<tr><td>${r.date}</td><td>${r.patient_origin}</td><td>${r.authored_state}</td><td>${r.added_meaning}</td><td>${r.management_function}</td><td>${r.later_reuse}</td></tr>`).join('');
}

async function renderProfiles(){
  const el = document.getElementById('profiles');
  if(!el) return;
  const data = await getJSON('profiles');
  const filter = document.getElementById('profile-filter');
  function draw(){
    const f = filter?.value || 'all';
    el.innerHTML = data.filter(p => f === 'all' || p.severity === f).map(p => `<article class="profile-card" data-severity="${p.severity}"><div class="meta">Risk rank ${p.risk_rank} · Original profile ${String(p.original_profile).padStart(2,'0')} · ${p.severity}</div><h3>${p.title}</h3><p>${p.proposition}</p><p><strong>Causal stage:</strong> ${p.stage}</p><div class="dependency"><span>Upstream: ${p.upstream.join(', ') || '—'}</span><span>Downstream: ${p.downstream.join(', ') || '—'}</span></div></article>`).join('');
  }
  filter?.addEventListener('change', draw);
  draw();
}

function initMode(){
  const buttons = [...document.querySelectorAll('[data-mode]')];
  if(!buttons.length) return;
  buttons.forEach(button => button.addEventListener('click', () => {
    const evidence = button.dataset.mode === 'evidence';
    document.body.classList.toggle('evidence-mode', evidence);
    buttons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    history.replaceState(null, '', evidence ? '#evidence' : window.location.pathname);
  }));
  if(window.location.hash === '#evidence'){
    const evidenceButton = buttons.find(b => b.dataset.mode === 'evidence');
    evidenceButton?.click();
  }
}

function initProgress(){
  const bar = document.querySelector('.reading-progress span');
  if(!bar) return;
  const update = () => {
    const max = document.documentElement.scrollHeight - window.innerHeight;
    const ratio = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0;
    bar.style.width = `${ratio * 100}%`;
  };
  update();
  addEventListener('scroll', update, {passive:true});
  addEventListener('resize', update);
}

document.addEventListener('DOMContentLoaded', () => {
  initMode();
  initProgress();
  renderEvidence();
  renderTimeline();
  renderKnowledge();
  renderProfiles();
});

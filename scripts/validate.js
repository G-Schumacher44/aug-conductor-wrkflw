#!/usr/bin/env node
// Conductor spine validator — agnostic to workflow type.
// Checks project/ structure, parses active slice acceptance criteria,
// and reports git state. No npm dependencies.

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const REPO_ROOT = path.join(__dirname, '..');
const PROJECT = path.join(REPO_ROOT, 'project');

const results = [];

function check(name, fn) {
  try {
    const r = fn();
    results.push({ name, ...r });
  } catch (e) {
    results.push({ name, status: 'fail', message: e.message });
  }
}

function exists(p) { return fs.existsSync(p); }
function read(p) { return fs.readFileSync(p, 'utf8'); }

// ─── Conductor spine ───────────────────────────────────────────────────────

check('project/ directory', () => {
  if (!exists(PROJECT)) return { status: 'fail', message: 'not found — scaffold project/ first' };
  return { status: 'pass' };
});

for (const rel of ['AGENTS.md', 'intent.md', 'conductor/index.md', 'conductor/handoff-log.md']) {
  check(`project/${rel}`, () => {
    if (!exists(path.join(PROJECT, rel))) return { status: 'fail', message: 'missing — scaffold incomplete' };
    return { status: 'pass' };
  });
}

check('project/conductor/handoff-log.md written', () => {
  const f = path.join(PROJECT, 'conductor', 'handoff-log.md');
  if (!exists(f)) return { status: 'fail', message: 'missing' };
  const content = read(f).replace(/<!--[\s\S]*?-->/g, '').trim();
  if (content.length < 50) return { status: 'warn', message: 'appears empty — agent may not have written the handoff yet' };
  if (!content.includes('Commit:')) return { status: 'warn', message: 'Commit: field missing — required by handoff rules' };
  if (!content.includes('Next Slice Proposal')) return { status: 'warn', message: 'Next Slice Proposal missing — required by handoff rules' };
  return { status: 'pass' };
});

check('CI workflow stub', () => {
  const ci = path.join(PROJECT, '.github', 'workflows');
  if (!exists(ci) || fs.readdirSync(ci).length === 0)
    return { status: 'warn', message: 'no .github/workflows — stub recommended' };
  return { status: 'pass', message: fs.readdirSync(ci).join(', ') };
});

// ─── Active slice + acceptance criteria ────────────────────────────────────

function getActiveSliceRel() {
  const indexPath = path.join(PROJECT, 'conductor', 'index.md');
  if (!exists(indexPath)) return null;
  const m = read(indexPath).match(/Active slice:\s*(.+)/i);
  return m ? m[1].trim() : null;
}

function parseAcceptanceCriteria(content) {
  const m = content.match(/##\s+Acceptance Criteria([\s\S]*?)(?=\n##|$)/m);
  if (!m) return [];
  return m[1].split('\n').flatMap(line => {
    const ticked = line.match(/^[-*]\s+\[x\]\s+(.+)/i);
    const open   = line.match(/^[-*]\s+\[ \]\s+(.+)/i);
    if (ticked) return [{ done: true,  text: ticked[1].trim() }];
    if (open)   return [{ done: false, text: open[1].trim() }];
    return [];
  });
}

const activeSliceRel = getActiveSliceRel();

check('Active slice file', () => {
  if (!activeSliceRel) return { status: 'warn', message: 'could not parse from conductor/index.md' };
  if (!exists(path.join(PROJECT, activeSliceRel)))
    return { status: 'fail', message: `${activeSliceRel} not found` };
  return { status: 'pass', message: activeSliceRel };
});

if (activeSliceRel && exists(path.join(PROJECT, activeSliceRel))) {
  const criteria = parseAcceptanceCriteria(read(path.join(PROJECT, activeSliceRel)));
  if (criteria.length > 0) {
    const done  = criteria.filter(c => c.done).length;
    const total = criteria.length;
    const lines = criteria.map(c => `       ${c.done ? '[x]' : '[ ]'} ${c.text}`).join('\n');
    results.push({
      name: `Acceptance criteria  ${done}/${total} checked`,
      status: done === total ? 'pass' : 'warn',
      detail: lines,
    });
  } else {
    results.push({
      name: 'Acceptance criteria',
      status: 'warn',
      message: 'no checklist items found in slice — add an Acceptance Criteria section',
    });
  }
}

// ─── Git state ─────────────────────────────────────────────────────────────

check('Git branch is a feature branch', () => {
  try {
    const branch = execSync('git branch --show-current', { cwd: REPO_ROOT, encoding: 'utf8' }).trim();
    if (!branch) return { status: 'warn', message: 'detached HEAD' };
    if (['main', 'demo-run', 'dev'].includes(branch))
      return { status: 'fail', message: `on ${branch} — commits should go on a feature branch` };
    return { status: 'pass', message: branch };
  } catch {
    return { status: 'warn', message: 'could not determine branch' };
  }
});

// ─── Report ────────────────────────────────────────────────────────────────

const pass = results.filter(r => r.status === 'pass').length;
const warn = results.filter(r => r.status === 'warn').length;
const fail = results.filter(r => r.status === 'fail').length;

const hr = '─'.repeat(52);
console.log(`\nConductor Spine Validation\n${hr}`);

for (const r of results) {
  const icon = r.status === 'pass' ? '✓' : r.status === 'warn' ? '~' : '✗';
  const suffix = r.message ? `  — ${r.message}` : '';
  console.log(`  ${icon}  ${r.name}${suffix}`);
  if (r.detail) console.log(r.detail);
}

console.log(hr);
console.log(`  ${pass} passed  |  ${warn} warnings  |  ${fail} failed\n`);
process.exit(fail > 0 ? 1 : 0);

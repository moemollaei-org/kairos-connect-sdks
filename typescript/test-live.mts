import Kairos from './src/index.ts';

const API_KEY = 'kairos_sk_0PAMoQeXpi2L3UdAkJtsQc7jZ3bHgoW5KdmHNCfxQTE';

async function run() {
  const client = new Kairos({ apiKey: API_KEY });

  // ── /me ──────────────────────────────────────────────────────────────
  console.log('\n=== /me ===');
  const me = await client.me();
  console.log('✓ team_id:', me.team_id);
  console.log('✓ scopes:', me.scopes.join(', '));
  console.log('✓ rate_limit/min:', me.rate_limit_per_minute);

  // ── Tasks ─────────────────────────────────────────────────────────────
  console.log('\n=== tasks.list (with limit=3) ===');
  const tasks = await client.tasks.list({ limit: 3 });
  console.log('✓ total:', tasks.pagination.total, '| returned:', tasks.data.length, '| has_more:', tasks.pagination.has_more);

  if (tasks.data.length > 0) {
    const t = tasks.data[0];
    console.log('  first:', t.id, '|', t.title, '|', t.status);

    console.log('\n=== tasks.get ===');
    const tFull = await client.tasks.get(t.id);
    console.log('✓ id:', tFull.id);

    console.log('\n=== tasks.listLabels ===');
    const labels = await client.tasks.listLabels(t.id);
    console.log('✓ labels:', labels.length);

    console.log('\n=== tasks.listComments ===');
    const tc = await client.tasks.listComments(t.id, { limit: 3 });
    console.log('✓ comments total:', tc.pagination.total, '| has_more:', tc.pagination.has_more);
  }

  // ── Goals ─────────────────────────────────────────────────────────────
  console.log('\n=== goals.list ===');
  const goals = await client.goals.list({ limit: 3 });
  console.log('✓ total:', goals.pagination.total, '| returned:', goals.data.length);

  if (goals.data.length > 0) {
    const g = goals.data[0];
    console.log('  first:', g.id, '|', g.title.slice(0, 40));

    console.log('\n=== goals.get ===');
    const gFull = await client.goals.get(g.id);
    console.log('✓ id:', gFull.id);

    console.log('\n=== goals.listComments ===');
    const gc = await client.goals.listComments(g.id, { limit: 3 });
    console.log('✓ goal comments total:', gc.pagination.total);

    console.log('\n=== goals.listTasks (uses /tasks?goal_id=) ===');
    const gt = await client.goals.listTasks(g.id, { limit: 5 });
    console.log('✓ goal tasks total:', gt.pagination.total, '| returned:', gt.data.length);
  }

  // ── Documents ─────────────────────────────────────────────────────────
  console.log('\n=== documents.list ===');
  const docs = await client.documents.list({ limit: 3 });
  console.log('✓ total:', docs.pagination.total, '| returned:', docs.data.length, '| has_more:', docs.pagination.has_more);

  if (docs.data.length > 0) {
    console.log('\n=== documents.get ===');
    const d = await client.documents.get(docs.data[0].id);
    console.log('✓ id:', d.id);
  }

  // ── Whiteboards ───────────────────────────────────────────────────────
  console.log('\n=== whiteboards.list ===');
  const wbs = await client.whiteboards.list({ limit: 3 });
  console.log('✓ total:', wbs.pagination.total, '| returned:', wbs.data.length, '| has_more:', wbs.pagination.has_more);

  if (wbs.data.length > 0) {
    console.log('\n=== whiteboards.get ===');
    const w = await client.whiteboards.get(wbs.data[0].id);
    console.log('✓ id:', w.id);
  }

  // ── Forms ─────────────────────────────────────────────────────────────
  console.log('\n=== forms.list ===');
  const forms = await client.forms.list({ limit: 3 });
  console.log('✓ total:', forms.pagination.total, '| returned:', forms.data.length, '| has_more:', forms.pagination.has_more);

  if (forms.data.length > 0) {
    const f = forms.data[0];
    console.log('\n=== forms.get ===');
    const fFull = await client.forms.get(f.id);
    console.log('✓ id:', fFull.id);

    console.log('\n=== forms.listSubmissions ===');
    const subs = await client.forms.listSubmissions(f.id, { limit: 3 });
    console.log('✓ submissions total:', subs.pagination.total);
  }

  // ── Team ──────────────────────────────────────────────────────────────
  console.log('\n=== team.get (uses /teams) ===');
  const team = await client.team.get();
  console.log('✓ team:', team.name, '| id:', team.id);

  console.log('\n=== team.listMembers ===');
  const members = await client.team.listMembers(team.id);
  console.log('✓ members:', members.data.length);

  console.log('\n✅ All TypeScript SDK live tests passed');
}

run().catch(e => { console.error('\n❌', (e as Error).message); process.exit(1); });

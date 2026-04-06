import Kairos from './src/index.ts';

const API_KEY = 'kairos_sk_0PAMoQeXpi2L3UdAkJtsQc7jZ3bHgoW5KdmHNCfxQTE';

async function run() {
  const client = new Kairos({ apiKey: API_KEY });

  console.log('\n=== /me ===');
  const me = await client.me();
  console.log('✓ team_id:', me.team_id);
  console.log('✓ scopes:', me.scopes.join(', '));
  console.log('✓ rate_limit/min:', me.rate_limit_per_minute);

  console.log('\n=== tasks.list ===');
  const tasks = await client.tasks.list({ limit: 3 });
  console.log('✓ total:', tasks.pagination.total, '| returned:', tasks.data.length);

  if (tasks.data.length > 0) {
    const t = tasks.data[0];
    console.log('  first:', t.id, '|', t.title, '|', t.status);

    console.log('\n=== tasks.listLabels ===');
    const labels = await client.tasks.listLabels(t.id);
    console.log('✓ labels:', labels.length);

    console.log('\n=== tasks.listComments ===');
    const tc = await client.tasks.listComments(t.id, { limit: 3 });
    console.log('✓ comments total:', tc.pagination.total);
  }

  console.log('\n=== goals.list ===');
  const goals = await client.goals.list({ limit: 3 });
  console.log('✓ total:', goals.pagination.total, '| returned:', goals.data.length);

  if (goals.data.length > 0) {
    const g = goals.data[0];
    console.log('  first:', g.id, '|', g.title);

    console.log('\n=== goals.listComments ===');
    const gc = await client.goals.listComments(g.id, { limit: 3 });
    console.log('✓ goal comments total:', gc.pagination.total);

    console.log('\n=== goals.listTasks ===');
    const gt = await client.goals.listTasks(g.id, { limit: 3 });
    console.log('✓ goal tasks total:', gt.pagination.total);
  }

  console.log('\n=== documents.list ===');
  const docs = await client.documents.list({ limit: 3 });
  console.log('✓ total:', docs.pagination.total, '| returned:', docs.data.length);

  if (docs.data.length > 0) {
    const d = docs.data[0];
    console.log('\n=== documents.listComments ===');
    const dc = await client.documents.listComments(d.id, { limit: 3 });
    console.log('✓ doc comments total:', dc.pagination.total);
  }

  console.log('\n=== whiteboards.list ===');
  const wbs = await client.whiteboards.list({ limit: 3 });
  console.log('✓ total:', wbs.pagination.total, '| returned:', wbs.data.length);

  if (wbs.data.length > 0) {
    const w = wbs.data[0];
    console.log('\n=== whiteboards.listComments ===');
    const wc = await client.whiteboards.listComments(w.id, { limit: 3 });
    console.log('✓ whiteboard comments total:', wc.pagination.total);
  }

  console.log('\n=== forms.list ===');
  const forms = await client.forms.list({ limit: 3 });
  console.log('✓ total:', forms.pagination.total, '| returned:', forms.data.length);

  if (forms.data.length > 0) {
    const f = forms.data[0];
    console.log('\n=== forms.listSubmissions ===');
    const fs2 = await client.forms.listSubmissions(f.id, { limit: 3 });
    console.log('✓ submissions total:', fs2.pagination.total);
  }

  console.log('\n=== team.get ===');
  const team = await client.team.get();
  console.log('✓ team:', team.name, '| id:', team.id);

  console.log('\n=== team.listMembers ===');
  const members = await client.team.listMembers(team.id);
  console.log('✓ members:', members.data.length);

  console.log('\n✅ All TypeScript SDK live tests passed');
}

run().catch(e => { console.error('\n❌', (e as Error).message); process.exit(1); });

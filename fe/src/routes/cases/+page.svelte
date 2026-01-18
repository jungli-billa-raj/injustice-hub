<script lang="ts">
  export let data;

  const columns = [
//  'id',
//  'source_article_id',
  'blamed_entity',
  'entity_type',
// 'location',
  'crime_description',
  'severity',
  'blame_status',
  'justice_status',
  'confidence_score',
//  'created_at'
];
</script>

<h2>Cases</h2>

<p>
  Page {data.page} of {data.totalPages}
</p>

<table border="1">

<thead>
  <tr>
    {#each columns as col}
      <th>{col}</th>
    {/each}
  </tr>
</thead>

<tbody>
  {#each data.data.items as row}
    <tr>
      {#each columns as col}
        <td>{row[col] ?? '-'}</td>
      {/each}
    </tr>
  {/each}
</tbody>
</table>

<hr />

<nav>
  {#if data.page > 1}
    <a href="?page={data.page - 1}">Prev</a>
  {/if}

  {#each Array(Math.min(3, data.totalPages)) as _, i}
  {@const p = data.page + i}
  {#if p <= data.totalPages}
    | <a href="?page={p}">{p}</a>
  {/if}
  {/each}


  {#if data.page < data.totalPages}
    {#if data.page > 1} | {/if}
    <a href="?page={data.page + 1}">Next</a>
  {/if}
</nav>


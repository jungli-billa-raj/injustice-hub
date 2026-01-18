<script lang="ts">
  export let data;
  const columns = [
  { key: 'id', label: 'ID' },
  { key: 'source', label: 'Source' },
  { key: 'headline', label: 'Headline' },
  { key: 'published_at', label: 'Published' },
  { key: 'scraped_at', label: 'Scraped At' },
  { key: 'url', label: 'URL' }
  // { key: 'full_text', label: 'Full Text' }  // optional (very long)
];
</script>

<h2>Raw Articles</h2>

<p>
  Page {data.page} of {data.totalPages}
</p>

<table border="1">
  <thead>
    <tr>
      <th>ID</th>
      <th>Headline</th>
      <th>Source</th>
      <th>Published</th>
    </tr>
  </thead>

  <tbody>
    {#each data.data.items as row}
      <tr
        style="cursor: pointer"
        on:click={() => window.open(row.url, '_blank')}
      >
        <td>{row.id}</td>
        <td>{row.headline}</td>
        <td>{row.source}</td>
        <td>{row.published_at}</td>
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


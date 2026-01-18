<script lang="ts">
  export let data;
</script>

<h2>Cases</h2>

<p>
  Page {data.page} of {data.totalPages}
</p>

<table border="1">
  <thead>
    <tr>
      <th>ID</th>
      <th>Blamed Entity</th>
      <th>Entity Type</th>
      <th>Location</th>
    </tr>
  </thead>

  <tbody>
    {#each data.data.items as row}
      <tr
        style="cursor: pointer"
        on:click={() => row.article_url && window.open(row.article_url, '_blank')}
      >
        <td>{row.id}</td>
        <td>{row.blamed_entity}</td>
        <td>{row.entity_type}</td>
        <td>{row.location ?? '-'}</td>
      </tr>
    {/each}
  </tbody>
</table>

<hr />

<nav>
  {#if data.page > 1}
    <a href="?page={data.page - 1}">Prev</a>
  {/if}

  {#if data.page < data.totalPages}
    {#if data.page > 1} | {/if}
    <a href="?page={data.page + 1}">Next</a>
  {/if}
</nav>


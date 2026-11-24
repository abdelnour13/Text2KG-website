<script lang="ts" >

    let data : { items : string[], maxVisible : number } = $props();

    let visible = $derived(data.items.slice(0, data.maxVisible));
    let numHidden = $derived(Math.max(0, data.items.length - data.maxVisible));

</script>

<div class="flex flex-wrap gap-1">

    {#each data.items.slice(0, data.maxVisible) as item}
        <span class="tag truncate hover:overflow-auto hover:text-wrap">{item}</span>
    {/each}

    {#if numHidden > 0}
        <span class="tag bg-stone-100 text-stone-500">+{numHidden} more</span>
    {/if}

</div>
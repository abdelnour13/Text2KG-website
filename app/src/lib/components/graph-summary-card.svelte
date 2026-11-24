<script lang="ts" >

    import downloadIcon from '$lib/assets/download.svg';
	import type { MouseEventHandler } from 'svelte/elements';
    import TagList from './ui/taglist.svelte';
    import { downloadGraph } from '$lib/services/api';
    import { goto } from '$app/navigation';

    let summary : App.GraphSummary = $props();

    let downloading = $state(false);
    let downloadError : string | null = $state(null);

    let displayName = $derived(summary.id.split('_').join(' '));

    const handleDownload : MouseEventHandler<HTMLButtonElement> = async (e) => {

        e.stopPropagation();
        downloadError = null;
        downloading = true;

        try {
            await downloadGraph(summary.id)
        } catch (err) {
            downloadError = err instanceof Error ? err.message : 'Download failed'
        } finally {
            downloading = false;
        }
    };

</script>

<div
    class="card cursor-pointer group animate-fade-in"
    role="button"
    tabindex={0}   
    onclick={() => goto(`maps/${summary.id}`)}
    onkeydown={(ev) => { ev.key == 'Enter' && goto(`maps/${summary.id}`)}}
>
    <div class="flex items-start justify-between gap-2 mb-3">
        <div>
            <p class="section-label">Expertise map</p>
            <h3 class="text-sm font-semibold text-stone-800 capitalize leading-snug group-hover:text-accent transition-colors">
            {displayName}
            </h3>
        </div>
        <span class="shrink-0 text-xs font-mono bg-stone-100 text-stone-500 px-2 py-0.5 rounded">
            {summary.number_of_expertises} expertises
        </span>
    </div>

    <p class="text-xs text-stone-500 leading-relaxed mb-4 line-clamp-2">
        {summary.description || 'No description available.'}
    </p>

    <!-- {#if summary.labs.length > 0}
        <div class="mb-3">
          <p class="section-label">Labs</p>
          <TagList items={summary.labs} maxVisible={3} />
        </div>
    {/if}

    {#if summary.subdomains.length > 0}
        <div class="mb-4">
          <p class="section-label">Domains</p>
          <TagList items={summary.domains} maxVisible={4} />
        </div>
    {/if} -->

    <div class="flex items-center justify-between pt-3 border-t border-stone-100">
        <span class="text-xs text-accent font-medium group-hover:underline">
          View details →
        </span>
        <button
          onclick={handleDownload}
          disabled={downloading}
          class="btn-ghost text-xs"
          title="Download graph JSON dump"
        >
          <img src={downloadIcon} alt="" />
          {downloading ? 'Downloading…' : 'Download'}
        </button>
    </div>

    {#if downloadError}
        <p class="mt-2 text-xs text-red-600">{downloadError}</p>
    {/if}

</div>
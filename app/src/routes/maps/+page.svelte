<script lang="ts" >

	import GraphSummaryCard from "$lib/components/graph-summary-card.svelte";
    import Spinner from "$lib/components/ui/spinner.svelte";
    import ErrorMessage from "$lib/components/ui/error-message.svelte";
    import searchIcone from '$lib/assets/search.svg';
    import ChevronIcon from "$lib/components/ui/chevron-icon.svelte";
    import { listGraphs } from "$lib/services/api";

    const INITIAL_COUNT = 4

    let loading = $state(true);
    let error : string | null = $state(null);
    let expanded = $state(false);
    let graphs : App.GraphSummary[] = $state([]);
    let query = $state('');

    let hiddenCount = $derived(Math.max(0, graphs.length - INITIAL_COUNT));
    let visible = $derived(graphs);

    $effect(() => {
        listGraphs()
            .then(g => graphs = g)
            .catch((err) => error = err instanceof Error ? err.message : 'Failed to load graphs')
            .finally(() => loading = false)
    })

</script>

<main class="flex-1 max-w-6xl mx-auto px-4 sm:px-6 py-14 animate-fade-in">

    <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4 mb-8">
        <div>
          <p class="section-label mb-1">Knowledge graphs</p>
          <h1 class="text-2xl font-semibold text-stone-900 tracking-tight">
            Expertise Maps
          </h1>
        </div>

        <div class="relative w-full sm:w-64">
          <span class="absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none">
            <img src={searchIcone} alt="" />
          </span>
          <input
            type="search"
            placeholder="Search maps…"
            class="input pl-8"
          />
        </div>
    </div>

    {#if loading}
        <div class="flex items-center gap-3 py-16 justify-center text-stone-400">
          <Spinner size="md" />
          <span class="text-sm">Loading expertise maps…</span>
        </div>
    {:else}
        {#if graphs.length == 0}
            <div class="py-16 text-center text-sm text-stone-400">
                {query ? `No maps match "${query}".` : 'No expertise maps found.'}
            </div>
        {:else}

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-2 gap-5">
                {#each visible as graph }
                    <GraphSummaryCard {...graph} />
                {/each}
            </div>


            {#if hiddenCount > 0}
                <div class="mt-6 flex justify-center">
                    <button
                        onclick={() => expanded = !expanded}
                        class="btn-secondary"
                    >
                        <ChevronIcon open={expanded} />
                        {expanded
                            ? 'Show less'
                            : `Show ${hiddenCount} more map${hiddenCount !== 1 ? 's' : ''}`
                        }
                    </button>
                </div>
            {/if}

        {/if}
    {/if}
    
    {#if error}
        <ErrorMessage message={error} />
    {/if}

</main>
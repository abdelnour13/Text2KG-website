<script lang="ts">

    import GraphSummaryCard from '$lib/components/graph-summary-card.svelte';
    import { listGraphs } from '$lib/services/api';
    import { i18n } from '$lib/i18n/index.svelte';

    const INITIAL_COUNT = 6;

    let loading = $state(true);
    let error: string | null = $state(null);
    let expanded = $state(false);
    let graphs: App.GraphSummary[] = $state([]);
    let query = $state('');

    // Search matches the map name, description, labs, domains and subdomains.
    const haystack = (g: App.GraphSummary) =>
        [g.name, g.description, ...(g.labs ?? []), ...(g.domains ?? []), ...(g.subdomains ?? [])]
            .join(' ')
            .toLowerCase();

    let filtered = $derived.by(() => {
        const terms = query.trim().toLowerCase().split(/\s+/).filter(Boolean);
        if (terms.length === 0) return graphs;
        return graphs.filter((g) => {
            const text = haystack(g);
            return terms.every((t) => text.includes(t));
        });
    });

    let searching = $derived(query.trim().length > 0);
    let visible = $derived(expanded || searching ? filtered : filtered.slice(0, INITIAL_COUNT));
    let hiddenCount = $derived(filtered.length - visible.length);

    function load() {
        loading = true;
        error = null;
        listGraphs()
            .then((g) => (graphs = g))
            .catch((err) => (error = err instanceof Error ? err.message : 'Unknown error'))
            .finally(() => (loading = false));
    }

    $effect(() => {
        load();
    });

    let t = $derived(i18n.t.maps);

</script>

<svelte:head>
    <title>{t.metaTitle}{i18n.t.titleSuffix}</title>
    <meta name="description" content={t.metaDescription} />
</svelte:head>

<main class="flex-1">

    <header class="border-b border-line bg-white">
        <div class="mx-auto flex max-w-7xl flex-col gap-8 px-5 py-16 sm:px-8 sm:py-20 lg:flex-row lg:items-end lg:justify-between">
            <div>
                <h1 class="text-4xl font-semibold tracking-[-0.025em] text-ink sm:text-5xl">{t.title}</h1>
                <p class="mt-5 max-w-2xl text-xl leading-relaxed text-pretty text-ink-soft">
                    {t.lead}
                </p>
            </div>

            <div class="w-full lg:w-80">
                <label for="map-search" class="sr-only">{t.searchLabel}</label>
                <div class="relative">
                    <svg viewBox="0 0 24 24" class="pointer-events-none absolute top-1/2 left-4 size-5 -translate-y-1/2 text-ink-faint" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
                        <circle cx="10.5" cy="10.5" r="6" /><path d="m15 15 5 5" />
                    </svg>
                    <input
                        id="map-search"
                        type="search"
                        bind:value={query}
                        placeholder={t.searchPlaceholder}
                        autocomplete="off"
                        class="h-12 w-full rounded-full border border-line bg-paper pr-4 pl-12 text-base text-ink placeholder:text-ink-faint focus:border-accent-light focus:bg-white focus:ring-4 focus:ring-accent-light/15 focus:outline-none"
                    />
                </div>
            </div>
        </div>
    </header>

    <section class="mx-auto max-w-7xl px-5 py-12 sm:px-8 sm:py-16" aria-busy={loading}>

        {#if loading}
            <!-- Placeholders in the shape of the cards -->
            <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3" aria-hidden="true">
                {#each { length: 3 } as _}
                    <div class="animate-pulse rounded-3xl bg-white p-7 ring-1 ring-line">
                        <div class="h-6 w-2/3 rounded-full bg-line"></div>
                        <div class="mt-4 h-4 w-full rounded-full bg-paper"></div>
                        <div class="mt-2 h-4 w-5/6 rounded-full bg-paper"></div>
                        <div class="mt-8 h-5 w-1/2 rounded-full bg-paper"></div>
                        <div class="mt-6 h-10 border-t border-line"></div>
                    </div>
                {/each}
            </div>
            <p class="sr-only" role="status">{t.loading}</p>

        {:else if error}
            <div class="mx-auto max-w-lg rounded-3xl bg-white p-8 text-center ring-1 ring-line" role="alert">
                <h2 class="text-xl font-semibold text-ink">{t.errorTitle}</h2>
                <p class="mt-2 text-base leading-relaxed text-ink-soft">
                    {i18n.t.serverReturned} <span class="text-ink">{error}</span>. {t.errorHint}
                </p>
                <button type="button" onclick={load} class="mt-6 inline-flex h-12 items-center rounded-full bg-accent px-6 text-base font-medium text-white transition-colors hover:bg-accent-light">
                    {i18n.t.tryAgain}
                </button>
            </div>

        {:else if graphs.length === 0}
            <div class="mx-auto max-w-lg rounded-3xl bg-white p-8 text-center ring-1 ring-line">
                <h2 class="text-xl font-semibold text-ink">{t.emptyTitle}</h2>
                <p class="mt-2 text-base leading-relaxed text-ink-soft">
                    {t.emptyText}
                </p>
            </div>

        {:else}
            <p class="mb-6 text-base text-ink-faint" aria-live="polite">
                {searching ? t.matchCount(filtered.length, graphs.length, query.trim()) : t.count(graphs.length)}
            </p>

            {#if filtered.length === 0}
                <div class="rounded-3xl bg-white p-8 text-center ring-1 ring-line">
                    <h2 class="text-xl font-semibold text-ink">{t.noMatchTitle(query.trim())}</h2>
                    <p class="mt-2 text-base text-ink-soft">{t.noMatchText}</p>
                    <button type="button" onclick={() => (query = '')} class="mt-6 inline-flex h-11 items-center rounded-full px-5 text-base font-medium text-ink ring-1 ring-line transition-colors hover:bg-paper">
                        {t.clearSearch}
                    </button>
                </div>
            {:else}
                <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
                    {#each visible as graph (graph.id)}
                        <GraphSummaryCard {...graph} />
                    {/each}
                </div>

                {#if hiddenCount > 0 || (expanded && !searching && filtered.length > INITIAL_COUNT)}
                    <div class="mt-10 flex justify-center">
                        <button
                            type="button"
                            onclick={() => (expanded = !expanded)}
                            aria-expanded={expanded}
                            class="inline-flex h-12 items-center gap-2 rounded-full bg-white px-6 text-base font-medium text-ink ring-1 ring-line transition-colors hover:bg-paper"
                        >
                            {expanded ? t.showFewer : t.showMore(hiddenCount)}
                            <svg viewBox="0 0 24 24" class={['size-5 transition-transform', expanded && 'rotate-180']} fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                                <path d="m6 9 6 6 6-6" />
                            </svg>
                        </button>
                    </div>
                {/if}
            {/if}
        {/if}
    </section>

</main>

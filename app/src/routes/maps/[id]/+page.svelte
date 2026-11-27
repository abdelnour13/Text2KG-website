<script lang="ts">

    import { onMount, tick } from 'svelte';
    import { replaceState } from '$app/navigation';
    import { page } from '$app/state';
    import ExpertiseBrowser from '$lib/components/expertise-browser.svelte';
    import VisPanel from '$lib/components/vis-panel.svelte';
    import FilterPanel from '$lib/components/filter-panel.svelte';
    import ExpertiseDetailPanel from '$lib/components/expertise-detail-panel.svelte';
    import Spinner from '$lib/components/ui/spinner.svelte';
    import { getGraph, visTaxonomy, visExpertises, visSummary } from '$lib/services/api';
    import { i18n } from '$lib/i18n/index.svelte';

    let { params } = $props();

    // A derived value only changes when the ID itself changes. Reading params.id
    // directly would refetch the whole map each time the tab updates the URL hash.
    let mapId = $derived(params.id);

    // ── Map data ──────────────────────────────────────────────────────────────
    let loading = $state(true);
    let error: string | null = $state(null);
    let detail: App.GraphDetail | null = $state(null);

    function load(id: string) {
        loading = true;
        error = null;
        getGraph(id)
            .then((d) => (detail = d))
            .catch((err) => (error = err instanceof Error ? err.message : 'Unknown error'))
            .finally(() => (loading = false));
    }

    $effect(() => {
        load(mapId);
    });

    let t = $derived(i18n.t.map);

    let figures = $derived.by(() => {
        const d = detail as App.GraphDetail | null;
        return [
            { label: t.figures.expertises, value: d?.expertises.length },
            { label: t.figures.domains,    value: d?.domains.length },
            { label: t.figures.subdomains, value: d?.subdomains.length },
            { label: t.figures.labs,       value: d?.labs.length },
        ];
    });

    // ── Tabs ──────────────────────────────────────────────────────────────────
    const TAB_IDS = ['list', 'hierarchy', 'charts', 'network', 'detail'] as const;
    type TabId = (typeof TAB_IDS)[number];

    let tab = $state<TabId>('list');
    let tabButtons: HTMLButtonElement[] = $state([]);

    // The open tab is kept in the URL (#network…) so it survives reloads and can be shared.
    onMount(() => {
        const fromHash = page.url.hash.slice(1);
        if ((TAB_IDS as readonly string[]).includes(fromHash)) tab = fromHash as TabId;
    });

    function selectTab(id: TabId) {
        tab = id;
        replaceState(`#${id}`, {});
    }

    async function onTabKeydown(e: KeyboardEvent, i: number) {
        const keys: Record<string, number> = { ArrowRight: i + 1, ArrowLeft: i - 1, Home: 0, End: TAB_IDS.length - 1 };
        if (!(e.key in keys)) return;
        e.preventDefault();
        const next = (keys[e.key] + TAB_IDS.length) % TAB_IDS.length;
        selectTab(TAB_IDS[next]);
        await tick();
        tabButtons[next]?.focus();
    }

    // ── Expertise network filters ─────────────────────────────────────────────
    let networkFilters: { domains?: string[]; subdomains?: string[]; labs?: string[] } = {};

    function onNetworkFilterChange(mode: 'domain' | 'subdomain', labs: Set<string>, domains: Set<string>, subdomains: Set<string>) {
        networkFilters = {
            domains: mode === 'domain' && domains.size > 0 ? [...domains] : undefined,
            subdomains: mode === 'subdomain' && subdomains.size > 0 ? [...subdomains] : undefined,
            labs: labs.size > 0 ? [...labs] : undefined,
        };
    }

    // ── Expertise details ─────────────────────────────────────────────────────
    let selectedExpertiseId: string | null = $state(null);

    function viewExpertise(ex: App.Expertise) {
        selectedExpertiseId = ex.id;
        selectTab('detail');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

</script>

<svelte:head>
    <title>{mapId}{i18n.t.titleSuffix}</title>
</svelte:head>

<main class="flex-1">

    <!-- The header is always shown: the title comes from the URL, and the
         figures show placeholders until the map data arrives. -->
    <header class="bg-white">
        <div class="mx-auto max-w-7xl px-5 pt-14 pb-10 sm:px-8 sm:pt-20 sm:pb-12">
            {#if detail?.name}
                <h1 class="text-[2.75rem] leading-[1.05] font-semibold tracking-[-0.03em] text-balance text-ink capitalize sm:text-6xl lg:text-5xl">
                    {detail?.name}
                </h1>
            {:else if loading}
                <div class="h-5 w-1/3 animate-pulse rounded-full bg-paper"></div>
            {/if}

            {#if detail?.description}
                <p class="mt-6 max-w-3xl text-xl leading-relaxed text-pretty text-ink-soft">{detail.description}</p>
            {:else if loading}
                <div class="mt-7 max-w-3xl space-y-3" aria-hidden="true">
                    <div class="h-5 w-full animate-pulse rounded-full bg-paper"></div>
                    <div class="h-5 w-2/3 animate-pulse rounded-full bg-paper"></div>
                </div>
            {/if}

            {#if !error}
                <dl class="mt-10 grid grid-cols-2 gap-x-10 gap-y-6 sm:flex sm:flex-wrap" aria-busy={loading}>
                    {#each figures as f}
                        <div>
                            <dt class="text-sm text-ink-faint">{f.label}</dt>
                            <dd class="mt-0.5 text-3xl font-semibold tabular-nums text-ink">
                                {#if f.value === undefined}
                                    <span class="mt-1.5 block h-8 w-12 animate-pulse rounded-lg bg-paper" aria-hidden="true"></span>
                                {:else}
                                    {i18n.num(f.value)}
                                {/if}
                            </dd>
                        </div>
                    {/each}
                </dl>
            {/if}
        </div>
    </header>

    {#if error && !detail}
        <div class="border-t border-line px-5 py-20">
            <div class="mx-auto max-w-lg rounded-3xl bg-white p-8 text-center ring-1 ring-line" role="alert">
                <h2 class="text-xl font-semibold text-ink">{t.errorTitle}</h2>
                <p class="mt-2 text-base leading-relaxed text-ink-soft">
                    {i18n.t.serverReturned} <span class="text-ink">{error}</span>
                </p>
                <div class="mt-6 flex flex-wrap justify-center gap-3">
                    <button type="button" onclick={() => load(mapId)} class="inline-flex h-12 items-center rounded-full bg-accent px-6 text-base font-medium text-white transition-colors hover:bg-accent-light">
                        {i18n.t.tryAgain}
                    </button>
                    <a href="/maps" class="inline-flex h-12 items-center rounded-full px-6 text-base font-medium text-ink ring-1 ring-line transition-colors hover:bg-paper">
                        {t.allMaps}
                    </a>
                </div>
            </div>
        </div>

    {:else}
        <!-- Tab bar, pinned under the site header while scrolling -->
        <div class="sticky top-18 z-20 border-y border-line bg-white/90 backdrop-blur-md">
            <div class="mx-auto max-w-7xl overflow-x-auto px-5 sm:px-8 [scrollbar-width:none]">
                <div role="tablist" aria-label={t.tabsAria} class="flex min-w-max gap-1">
                    {#each TAB_IDS as id, i}
                        <button
                            bind:this={tabButtons[i]}
                            type="button"
                            role="tab"
                            id="tab-{id}"
                            aria-selected={tab === id}
                            aria-controls="panel-{id}"
                            tabindex={tab === id ? 0 : -1}
                            onclick={() => selectTab(id)}
                            onkeydown={(e) => onTabKeydown(e, i)}
                            class={[
                                'relative h-14 px-4 text-base whitespace-nowrap transition-colors focus-visible:outline-offset-[-4px]',
                                tab === id
                                    ? 'font-semibold text-accent after:absolute after:inset-x-3 after:bottom-0 after:h-[3px] after:rounded-full after:bg-accent'
                                    : 'text-ink-soft hover:text-ink',
                            ]}
                        >
                            {t.tabs[id]}
                        </button>
                    {/each}
                </div>
            </div>
        </div>

        <div class="mx-auto max-w-7xl px-5 py-12 sm:px-8 sm:py-14">
            {#if !detail}
                <div class="flex flex-col items-center justify-center gap-4 py-24" role="status">
                    <Spinner size="lg" />
                    <p class="text-base text-ink-soft">{t.loading}</p>
                </div>
            {:else}
                <!-- Panels stay mounted so each tab keeps its state when you switch away -->
                <div role="tabpanel" id="panel-list" aria-labelledby="tab-list" hidden={tab !== 'list'}>
                    <ExpertiseBrowser
                        graphId={mapId}
                        expertises={detail.expertises}
                        domains={detail.domains}
                        subdomains={detail.subdomains}
                        labs={detail.labs}
                        onView={viewExpertise}
                    />
                </div>

                <div role="tabpanel" id="panel-hierarchy" aria-labelledby="tab-hierarchy" hidden={tab !== 'hierarchy'}>
                    <VisPanel
                        title={t.hierarchy.title}
                        description={t.hierarchy.description}
                        frameTitle={t.tabs.hierarchy}
                        active={tab === 'hierarchy'}
                        autoLoad
                        onGenerate={() => visTaxonomy(mapId)}
                    />
                </div>

                <div role="tabpanel" id="panel-charts" aria-labelledby="tab-charts" hidden={tab !== 'charts'}>
                    <VisPanel
                        title={t.charts.title}
                        description={t.charts.description}
                        frameTitle={t.tabs.charts}
                        active={tab === 'charts'}
                        autoLoad
                        onGenerate={() => visSummary(mapId)}
                    />
                </div>

                <div role="tabpanel" id="panel-network" aria-labelledby="tab-network" hidden={tab !== 'network'}>
                    <VisPanel
                        title={t.network.title}
                        description={t.network.description}
                        frameTitle={t.tabs.network}
                        active={tab === 'network'}
                        actionLabel={t.network.show}
                        updateLabel={t.network.update}
                        emptyText={t.network.empty}
                        onGenerate={() => visExpertises(mapId, networkFilters)}
                    >
                        {#snippet controls()}
                            <FilterPanel
                                domains={detail!.domains}
                                subdomains={detail!.subdomains}
                                labs={detail!.labs}
                                onInputChange={onNetworkFilterChange}
                            />
                        {/snippet}
                    </VisPanel>
                </div>

                <div role="tabpanel" id="panel-detail" aria-labelledby="tab-detail" hidden={tab !== 'detail'}>
                    <ExpertiseDetailPanel
                        graphId={mapId}
                        expertises={detail.expertises}
                        selectedId={selectedExpertiseId}
                        onSelect={(id) => (selectedExpertiseId = id)}
                    />
                </div>
            {/if}
        </div>
    {/if}
</main>

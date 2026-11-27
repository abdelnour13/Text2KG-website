<script lang="ts">

    import { i18n } from '$lib/i18n/index.svelte';

    type FilterMode = 'domain' | 'subdomain';

    interface FilterPanelProps {
        domains: string[];
        subdomains: string[];
        labs: string[];
        onInputChange: (mode: FilterMode, labs: Set<string>, domains: Set<string>, subdomains: Set<string>) => void;
    }

    // Long chip lists are collapsed after this many items.
    const COLLAPSED_COUNT = 12;

    let { domains, labs, subdomains, onInputChange }: FilterPanelProps = $props();

    let filterMode = $state<FilterMode>('domain');
    let selectedDomains = $state(new Set<string>());
    let selectedSubdomains = $state(new Set<string>());
    let selectedLabs = $state(new Set<string>());
    let showAllTopics = $state(false);
    let showAllLabs = $state(false);

    let topics = $derived(filterMode === 'domain' ? domains : subdomains);
    let selectedTopics = $derived(filterMode === 'domain' ? selectedDomains : selectedSubdomains);
    let visibleTopics = $derived(showAllTopics ? topics : topics.slice(0, COLLAPSED_COUNT));
    let visibleLabs = $derived(showAllLabs ? labs : labs.slice(0, COLLAPSED_COUNT));

    let selectionCount = $derived(selectedTopics.size + selectedLabs.size);

    const emit = () => onInputChange(filterMode, selectedLabs, selectedDomains, selectedSubdomains);

    function toggle(set: Set<string>, item: string): Set<string> {
        const next = new Set(set);
        if (next.has(item)) next.delete(item);
        else next.add(item);
        return next;
    }

    function toggleTopic(item: string) {
        if (filterMode === 'domain') selectedDomains = toggle(selectedDomains, item);
        else selectedSubdomains = toggle(selectedSubdomains, item);
        emit();
    }

    function toggleLab(item: string) {
        selectedLabs = toggle(selectedLabs, item);
        emit();
    }

    function setMode(mode: FilterMode) {
        if (mode === filterMode) return;
        filterMode = mode;
        selectedDomains = new Set();
        selectedSubdomains = new Set();
        showAllTopics = false;
        emit();
    }

    function clearAll() {
        selectedDomains = new Set();
        selectedSubdomains = new Set();
        selectedLabs = new Set();
        emit();
    }

    const chipClass = (on: boolean) => [
        'inline-flex min-h-9 items-center rounded-full px-3.5 py-1.5 text-left text-sm leading-snug transition-colors',
        on
            ? 'bg-accent text-white'
            : 'bg-paper text-ink-soft ring-1 ring-line hover:bg-accent-muted hover:text-accent hover:ring-accent-light/30',
    ];

</script>

<div class="rounded-2xl bg-white p-5 ring-1 ring-line sm:p-6">

    <div class="flex flex-wrap items-center justify-between gap-4">
        <div class="flex items-center gap-3">
            <span class="text-sm font-medium text-ink" id="filter-mode-label">{i18n.t.filters.filterBy}</span>
            <div class="inline-flex rounded-full bg-paper p-1 ring-1 ring-line" role="group" aria-labelledby="filter-mode-label">
                {#each [['domain', i18n.t.filters.domain], ['subdomain', i18n.t.filters.subdomain]] as [mode, label]}
                    <button
                        type="button"
                        onclick={() => setMode(mode as FilterMode)}
                        aria-pressed={filterMode === mode}
                        class={[
                            'h-8 rounded-full px-4 text-sm font-medium transition-colors',
                            filterMode === mode ? 'bg-white text-ink shadow-sm ring-1 ring-line' : 'text-ink-soft hover:text-ink',
                        ]}
                    >
                        {label}
                    </button>
                {/each}
            </div>
        </div>

        {#if selectionCount > 0}
            <button type="button" onclick={clearAll} class="text-sm font-medium text-accent-light hover:underline hover:underline-offset-4">
                {i18n.t.filters.clear(selectionCount)}
            </button>
        {/if}
    </div>

    {#if topics.length > 0}
        <div class="mt-4 flex flex-wrap gap-2">
            {#each visibleTopics as item}
                <button type="button" onclick={() => toggleTopic(item)} aria-pressed={selectedTopics.has(item)} class={chipClass(selectedTopics.has(item))}>
                    {item}
                </button>
            {/each}
            {#if topics.length > COLLAPSED_COUNT}
                <button type="button" onclick={() => (showAllTopics = !showAllTopics)} class="min-h-9 px-2 text-sm font-medium text-accent-light hover:underline hover:underline-offset-4">
                    {showAllTopics ? i18n.t.filters.showFewer : i18n.t.filters.showAll(topics.length)}
                </button>
            {/if}
        </div>
    {/if}

    {#if labs.length > 0}
        <div class="mt-5 border-t border-line pt-5">
            <p class="text-sm font-medium text-ink">{i18n.t.filters.labs}</p>
            <div class="mt-3 flex flex-wrap gap-2">
                {#each visibleLabs as lab}
                    <button type="button" onclick={() => toggleLab(lab)} aria-pressed={selectedLabs.has(lab)} class={chipClass(selectedLabs.has(lab))}>
                        {lab}
                    </button>
                {/each}
                {#if labs.length > COLLAPSED_COUNT}
                    <button type="button" onclick={() => (showAllLabs = !showAllLabs)} class="min-h-9 px-2 text-sm font-medium text-accent-light hover:underline hover:underline-offset-4">
                        {showAllLabs ? i18n.t.filters.showFewer : i18n.t.filters.showAll(labs.length)}
                    </button>
                {/if}
            </div>
        </div>
    {/if}
</div>

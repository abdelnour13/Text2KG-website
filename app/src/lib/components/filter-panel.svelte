<script lang="ts" >

    type FilterMode = 'domain' | 'subdomain';

    interface FilterPanelProps {
        domains : string[]
        subdomains : string[]
        labs : string[]
        onInputChange : (mode: FilterMode, labs : Set<string>, domains : Set<string>, subdomains : Set<string>) => void
    };

    const MODES : FilterMode[] = ['domain', 'subdomain'];

    let { domains, labs, subdomains, onInputChange } : FilterPanelProps = $props();

    let filterMode = $state('domain' as FilterMode);
    let selectedDomains = $state(new Set<string>());
    let selectedSubdomains = $state(new Set<string>());
    let selectedLabs = $state(new Set<string>());

    let hasFilters = $derived(
        (filterMode === 'domain' && selectedDomains.size > 0)       ||
        (filterMode === 'subdomain' && selectedSubdomains.size > 0) ||
        (selectedLabs.size > 0)
    );

    const toggleDomainsSet = (item : string) => {

        if (selectedDomains.has(item)) {
            selectedDomains.delete(item);
        }

        else
        {
            selectedDomains.add(item);
        }

        selectedDomains = new Set(selectedDomains);
        onInputChange(filterMode, selectedLabs, selectedDomains, selectedSubdomains);

    }

    const toggleSubdomainsSet = (item : string) => {

        if (selectedSubdomains.has(item)) {
            selectedSubdomains.delete(item);
        }

        else 
        {
            selectedSubdomains.add(item);
        }

        selectedSubdomains = new Set(selectedSubdomains);
        onInputChange(filterMode, selectedLabs, selectedDomains, selectedSubdomains);

    }

    const toggleLabsSet = (item : string) => {

        if (selectedLabs.has(item)) {
            selectedLabs.delete(item);
        }

        else 
        {
            selectedLabs.add(item);
        }

        selectedLabs = new Set(selectedLabs);
        onInputChange(filterMode, selectedLabs, selectedDomains, selectedSubdomains);

    }

    // $effect(() => {
    //     onInputChange(filterMode, selectedLabs, selectedDomains, selectedLabs);
    // })

</script>

<div class="border border-stone-200 rounded-lg p-4 space-y-4 bg-stone-50 mb-4">

    <div class="space-y-2">
        <div class="flex items-center gap-4">
            <span class="text-xs font-medium text-stone-600 w-24 shrink-0">Filter by</span>
            <div class="flex items-center gap-1 bg-white border border-stone-200 rounded p-0.5">
                {#each MODES as mode}
                    <button
                        onclick={() => {
                            console.log('clicked');
                            filterMode = mode;
                            selectedDomains = new Set();
                            selectedSubdomains = new Set();
                        }}
                        class={[
                        'px-3 py-1 text-xs rounded transition-colors capitalize',
                        filterMode === mode
                            ? 'bg-accent text-white font-medium'
                            : 'text-stone-500 hover:text-stone-800',
                        ].join(' ')}
                    >
                        {mode}
                    </button>
                {/each}
            </div>
        </div>

        {#if filterMode === 'domain' && domains.length > 0}
            <div class="flex items-start gap-4">
                <span class="text-xs text-stone-400 w-24 shrink-0 pt-1">Domains</span>
                <div class="flex flex-wrap gap-1.5">
                {#each domains as domain}
                    <button
                        onclick={() => toggleDomainsSet(domain)}
                        class={[
                            'px-2.5 py-1 text-xs rounded border transition-colors',
                            selectedDomains.has(domain)
                            ? 'bg-accent text-white border-accent'
                            : 'bg-white text-stone-600 border-stone-200 hover:border-accent hover:text-accent',
                        ].join(' ')}
                    >
                    {domain}
                    </button>
                {/each}
                </div>
            </div>
        {/if}

        {#if filterMode == 'subdomain' && subdomains.length > 0}
            <div class="flex items-start gap-4">
                <span class="text-xs text-stone-400 w-24 shrink-0 pt-1">Subdomains</span>
                <div class="flex flex-wrap gap-1.5">
                {#each subdomains as subdomain}
                    <button
                        onclick={() => toggleSubdomainsSet(subdomain)}
                        class={[
                            'px-2.5 py-1 text-xs rounded border transition-colors',
                            selectedSubdomains.has(subdomain)
                            ? 'bg-accent text-white border-accent'
                            : 'bg-white text-stone-600 border-stone-200 hover:border-accent hover:text-accent',
                        ].join(' ')}
                    >
                    {subdomain}
                    </button>
                {/each}
                </div>
            </div>
        {/if}

    </div>

    {#if labs.length}

        <div class="flex items-start gap-4 pt-2 border-t border-stone-200">
            <span class="text-xs font-medium text-stone-600 w-24 shrink-0 pt-1">Labs</span>
            <div class="flex flex-wrap gap-1.5">
                {#each labs as lab}
                    <button
                        onclick={() => toggleLabsSet(lab)}
                        class={[
                            'px-2.5 py-1 text-xs rounded border transition-colors',
                            selectedLabs.has(lab)
                            ? 'bg-accent text-white border-accent'
                            : 'bg-white text-stone-600 border-stone-200 hover:border-accent hover:text-accent',
                        ].join(' ')}
                    >
                    {lab}
                    </button>
                {/each}
            </div>
        </div>

    {/if}


    {#if hasFilters}
        <div class="flex items-center justify-between pt-1">
            <span class="text-xs text-stone-400">
                {[
                    filterMode === 'domain'    && selectedDomains.size > 0    && `${selectedDomains.size} domain${selectedDomains.size > 1 ? 's' : ''}`,
                    filterMode === 'subdomain' && selectedSubdomains.size > 0 && `${selectedSubdomains.size} subdomain${selectedSubdomains.size > 1 ? 's' : ''}`,
                    selectedLabs.size > 0 && `${selectedLabs.size} lab${selectedLabs.size > 1 ? 's' : ''}`,
                ].filter(Boolean).join(', ')} selected
            </span>
            <button
                onclick={() => { 
                    selectedDomains = new Set<string>();
                    selectedSubdomains = new Set<string>();
                    selectedLabs = new Set<string>();
                }}
                class="text-xs text-stone-400 hover:text-stone-700 transition-colors"
            >
                Clear filters
            </button>
        </div>
    {/if} 

</div>
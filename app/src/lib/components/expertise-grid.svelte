<script lang="ts" >

	import FilterPanel from "./filter-panel.svelte";
  import Taglist from "./ui/taglist.svelte";

  interface ExpertiseGridProps {
    expertises: App.GraphDetail['expertises']
    domains:    App.GraphDetail['domains']
    subdomains: App.GraphDetail['subdomains']
    labs:       App.GraphDetail['labs']
  };

  const PAGE_SIZE = 20;

  const { domains, expertises, labs, subdomains } : ExpertiseGridProps = $props();

  let filtered = $state([] as App.Expertise[]);
  let page = $state(0);

  let totalPages = $derived(Math.max(1, Math.ceil(filtered.length / PAGE_SIZE)));
  let slice = $derived(filtered.slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE));

  $effect(() => {
    filtered = expertises;
  })

  const onTogglePanelInputChange = (
    mode : 'domain' | 'subdomain',
    labs : Set<string>, 
    domains : Set<string>, 
    subdomains : Set<string>
  ) => {
      filtered = expertises.filter((value) => {
          return (
            (labs.size > 0 ? value.labs.some((v) => labs.has(v)) : true) &&
            (mode == 'domain' && domains.size > 0 ? value.domains.some((v) => domains.has(v)) : true) &&
            (mode == 'subdomain' && subdomains.size > 0 ? value.subdomains.some((v) => subdomains.has(v)) : true)
          )
      })
      page = 0
  }

</script>

<div class="mt-6">

  <div class="flex items-center justify-between mb-3">

    <h2 class="text-base font-semibold text-stone-800 border-b border-stone-100 pb-2 mb-4">
        Expertise Communities
    </h2>

    <div class="flex items-center gap-2 shrink-0">
      <span class="text-xs font-mono text-black font-semibold"> 
        <!--text-stone-500-->
        {filtered.length} result{filtered.length !== 1 ? 's' : ''} · {page + 1} / {totalPages}
      </span>

      <button
        onclick={() => page = page - 1}
        disabled={page === 0}
        aria-label="Previous page"
        class="w-7 h-7 flex items-center justify-center rounded border border-stone-200
                    text-stone-500 hover:bg-stone-100 hover:text-stone-800
                    disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
      >
        <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
          <path d="M7.5 2L4 6l3.5 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>

      <button
        onclick={() => page = page + 1}
        disabled={page === totalPages - 1}
        aria-label="Next page"
        class="w-7 h-7 flex items-center justify-center rounded border border-stone-200
                    text-stone-500 hover:bg-stone-100 hover:text-stone-800
                    disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
      >
        <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
          <path d="M4.5 2L8 6l-3.5 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
    </div>
  </div>

<FilterPanel 
  domains={domains}
  subdomains={subdomains}
  labs={labs}
  onInputChange={onTogglePanelInputChange}
/>

{#if slice.length == 0}
  <p class="text-sm text-stone-400 py-8 text-center">No expertises match the selected filters.</p>
{:else}
  <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
    {#each slice as ex}
      <div class="border border-stone-200 rounded px-3 py-2.5 bg-white">
          <div class="flex items-center justify-between gap-2 mb-1">
            <!-- <p class="text-sm font-medium text-stone-800 truncate">Id : {ex.id.split('_').pop()}</p> 
            <span class="text-xs font-mono text-stone-400 shrink-0">{ex.size} nodes</span> -->
          </div>
          <div class="text-xs text-black font-medium font-mono" >
            <span class="font-medium" >Name: </span>
            <span>{ex.llm_label}</span>
          </div>
          {#if ex.subdomains.length}
            <div class="mt-2">
              <Taglist items={ex.subdomains} maxVisible={2} />
            </div>
          {/if}
        </div>
    {/each}
  </div>
{/if}

</div>
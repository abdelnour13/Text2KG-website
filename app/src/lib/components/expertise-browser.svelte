<script lang="ts">

    import FilterPanel from './filter-panel.svelte';
    import { expertiseName, normalize, shortId, splitMatch } from '$lib/expertise';
    import { i18n } from '$lib/i18n/index.svelte';

    interface ExpertiseBrowserProps {
        graphId: string;
        expertises: App.Expertise[];
        domains: string[];
        subdomains: string[];
        labs: string[];
        /** Opens the "Expertise details" tab for this expertise. */
        onView: (ex: App.Expertise) => void;
    }

    type View = 'cards' | 'table';
    type SortKey = 'name' | 'size';

    const PAGE_SIZE = 24;
    const VIEW_KEY = 'expertise-map:view';

    let { graphId, expertises, domains, subdomains, labs, onView }: ExpertiseBrowserProps = $props();

    // ── View mode (remembered per browser) ────────────────────────────────────
    let view = $state<View>('cards');
    $effect(() => {
        try {
            const saved = localStorage.getItem(VIEW_KEY);
            if (saved === 'cards' || saved === 'table') view = saved;
        } catch { /* storage unavailable */ }
    });
    function setView(v: View) {
        view = v;
        try { localStorage.setItem(VIEW_KEY, v); } catch { /* storage unavailable */ }
    }

    // ── Filters, search and sort ─────────────────────────────────────────────
    let search = $state('');
    let filter = $state({
        mode: 'domain' as 'domain' | 'subdomain',
        labs: new Set<string>(),
        domains: new Set<string>(),
        subdomains: new Set<string>(),
    });
    let sortKey = $state<SortKey>('name');
    let sortDir = $state<1 | -1>(1);
    let page = $state(0);

    function onFilterChange(mode: 'domain' | 'subdomain', l: Set<string>, d: Set<string>, s: Set<string>) {
        filter = { mode, labs: new Set(l), domains: new Set(d), subdomains: new Set(s) };
        page = 0;
    }

    let filtered = $derived.by(() => {
        const q = normalize(search.trim());
        const { mode, labs: fl, domains: fd, subdomains: fs } = filter;
        const rows = expertises.filter((ex) =>
            (fl.size === 0 || ex.labs.some((v) => fl.has(v))) &&
            (mode !== 'domain' || fd.size === 0 || ex.domains.some((v) => fd.has(v))) &&
            (mode !== 'subdomain' || fs.size === 0 || ex.subdomains.some((v) => fs.has(v))) &&
            (!q || normalize(expertiseName(ex)).includes(q))
        );
        return rows.sort((a, b) =>
            sortKey === 'size'
                ? (a.size - b.size) * sortDir || i18n.compare(expertiseName(a), expertiseName(b))
                : i18n.compare(expertiseName(a), expertiseName(b)) * sortDir
        );
    });

    let totalPages = $derived(Math.max(1, Math.ceil(filtered.length / PAGE_SIZE)));
    let current = $derived(Math.min(page, totalPages - 1));
    let slice = $derived(filtered.slice(current * PAGE_SIZE, (current + 1) * PAGE_SIZE));
    let rangeStart = $derived(filtered.length === 0 ? 0 : current * PAGE_SIZE + 1);
    let rangeEnd = $derived(Math.min(filtered.length, (current + 1) * PAGE_SIZE));

    // Sort options for the cards view; the table uses clickable headers.
    let t = $derived(i18n.t.browser);
    let sorts = $derived([
        { value: 'name:1',  label: t.sorts.nameAsc },
        { value: 'name:-1', label: t.sorts.nameDesc },
        { value: 'size:-1', label: t.sorts.sizeDesc },
        { value: 'size:1',  label: t.sorts.sizeAsc },
    ]);
    let sortValue = $derived(`${sortKey}:${sortDir}`);
    function setSort(value: string) {
        const [k, d] = value.split(':');
        sortKey = k as SortKey;
        sortDir = Number(d) as 1 | -1;
        page = 0;
    }
    function toggleSort(key: SortKey) {
        if (sortKey === key) sortDir = sortDir === 1 ? -1 : 1;
        else { sortKey = key; sortDir = key === 'size' ? -1 : 1; }
        page = 0;
    }
    const ariaSort = (key: SortKey) => (sortKey !== key ? 'none' : sortDir === 1 ? 'ascending' : 'descending');

    let listTop: HTMLElement;
    function goTo(p: number) {
        page = p;
        listTop?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    const more = (items: string[], max: number) => ({ shown: items.slice(0, max), rest: Math.max(0, items.length - max) });

</script>

{#snippet viewButton(v: View, label: string)}
    <button
        type="button"
        onclick={() => setView(v)}
        aria-pressed={view === v}
        class={[
            'inline-flex h-9 items-center gap-2 rounded-full px-4 text-sm font-medium transition-colors',
            view === v ? 'bg-white text-ink shadow-sm ring-1 ring-line' : 'text-ink-soft hover:text-ink',
        ]}
    >
        <svg viewBox="0 0 24 24" class="size-4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            {#if v === 'cards'}
                <rect x="4" y="4" width="7" height="7" rx="1.5" /><rect x="13" y="4" width="7" height="7" rx="1.5" /><rect x="4" y="13" width="7" height="7" rx="1.5" /><rect x="13" y="13" width="7" height="7" rx="1.5" />
            {:else}
                <path d="M4 6h16M4 12h16M4 18h16" />
            {/if}
        </svg>
        {label}
    </button>
{/snippet}

{#snippet highlighted(text: string)}
    {@const [before, match, after] = splitMatch(text, search)}
    {before}{#if match}<mark class="rounded-sm bg-cluster-amber/25 text-inherit">{match}</mark>{/if}{after}
{/snippet}

{#snippet viewButtonFor(ex: App.Expertise)}
    <button
        type="button"
        onclick={() => onView(ex)}
        class="inline-flex h-9 shrink-0 items-center rounded-full px-3.5 text-sm font-medium whitespace-nowrap text-accent-light ring-1 ring-line transition-colors hover:bg-accent-muted"
        aria-label={t.viewGraphAria(expertiseName(ex))}
    >
        {t.viewGraph}
    </button>
{/snippet}

<section class="space-y-6">

    <div class="max-w-2xl">
        <h2 class="text-2xl font-semibold tracking-[-0.015em] text-ink sm:text-3xl">{t.title}</h2>
        <p class="mt-2 text-lg leading-relaxed text-ink-soft">
            {t.description}
        </p>
    </div>

    <FilterPanel {domains} {subdomains} {labs} onInputChange={onFilterChange} />

    <!-- Toolbar -->
    <div bind:this={listTop} class="flex scroll-mt-40 flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div class="relative w-full lg:max-w-sm">
            <label for="expertise-search" class="sr-only">{t.searchLabel}</label>
            <svg viewBox="0 0 24 24" class="pointer-events-none absolute top-1/2 left-4 size-5 -translate-y-1/2 text-ink-faint" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
                <circle cx="10.5" cy="10.5" r="6" /><path d="m15 15 5 5" />
            </svg>
            <input
                id="expertise-search"
                type="search"
                bind:value={search}
                oninput={() => (page = 0)}
                placeholder={t.searchPlaceholder}
                autocomplete="off"
                class="h-11 w-full rounded-full border border-line bg-white pr-4 pl-12 text-base text-ink placeholder:text-ink-faint focus:border-accent-light focus:ring-4 focus:ring-accent-light/15 focus:outline-none"
            />
        </div>

        <div class="flex flex-wrap items-center gap-3">
            {#if view === 'cards'}
                <label class="flex items-center gap-2 text-sm text-ink-soft">
                    {t.sort}
                    <select
                        value={sortValue}
                        onchange={(e) => setSort((e.target as HTMLSelectElement).value)}
                        class="h-10 rounded-full border border-line bg-white pr-9 pl-4 text-sm font-medium text-ink focus:border-accent-light focus:outline-none"
                    >
                        {#each sorts as s}
                            <option value={s.value}>{s.label}</option>
                        {/each}
                    </select>
                </label>
            {/if}
            <div class="inline-flex rounded-full bg-paper p-1 ring-1 ring-line" role="group" aria-label={t.displayAs}>
                {@render viewButton('cards', t.cards)}
                {@render viewButton('table', t.table)}
            </div>
        </div>
    </div>

    <p class="text-base text-ink-faint" aria-live="polite">
        {filtered.length === 0 ? t.none : t.showing(rangeStart, rangeEnd, filtered.length)}{#if filtered.length !== expertises.length}{t.outOf(expertises.length)}{/if}
    </p>

    {#if slice.length === 0}
        <div class="rounded-2xl border-2 border-dashed border-line p-10 text-center">
            <p class="text-lg font-semibold text-ink">{t.noMatchTitle}</p>
            <p class="mt-1 text-base text-ink-soft">{t.noMatchText}</p>
        </div>

    {:else if view === 'cards'}
        <ul class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {#each slice as ex (ex.id)}
                {@const subs = more(ex.subdomains, 4)}
                <li class="flex flex-col rounded-2xl bg-white p-6 ring-1 ring-line transition-shadow hover:shadow-[0_8px_30px_-12px_rgb(21_32_51/0.18)]">
                    <p class="flex items-center gap-2 text-sm font-medium text-accent-light">
                        <span class="size-2 rounded-full bg-accent-light" aria-hidden="true"></span>
                        {t.cardLabel}
                    </p>
                    <h3 class="mt-2 text-xl leading-snug font-semibold tracking-[-0.01em] text-ink">
                        {@render highlighted(expertiseName(ex))}
                    </h3>

                    {#if ex.subdomains.length}
                        <ul class="mt-4 flex flex-wrap gap-2" aria-label={t.columns.subdomains}>
                            {#each subs.shown as sub}
                                <li class="inline-flex items-center gap-1.5 rounded-lg bg-paper py-1 pr-2.5 pl-2 text-sm leading-snug text-ink-soft ring-1 ring-line ring-inset">
                                    <svg viewBox="0 0 16 16" class="size-3.5 shrink-0 text-ink-faint" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                                        <path d="M4 2.5v5a2 2 0 0 0 2 2h6.5M10 7l2.5 2.5L10 12" />
                                    </svg>
                                    {sub}
                                </li>
                            {/each}
                            {#if subs.rest}
                                <li class="inline-flex items-center px-1 py-1 text-sm text-ink-faint">{t.andMore(subs.rest)}</li>
                            {/if}
                        </ul>
                    {/if}

                    <div class="mt-auto pt-5">
                        <div class="border-t border-line pt-4">
                            <button
                                type="button"
                                onclick={() => onView(ex)}
                                class="group/btn inline-flex items-center gap-1.5 text-base font-medium text-accent-light hover:underline hover:underline-offset-4"
                                aria-label={t.viewGraphAria(expertiseName(ex))}
                            >
                                {t.viewGraph}
                                <svg viewBox="0 0 24 24" class="size-4 transition-transform group-hover/btn:translate-x-0.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 6 6 6-6 6" /></svg>
                            </button>
                        </div>
                    </div>
                </li>
            {/each}
        </ul>

    {:else}
        <div class="overflow-x-auto rounded-2xl bg-white ring-1 ring-line">
            <table class="w-full min-w-[900px] text-left text-sm">
                <thead class="border-b border-line bg-paper text-ink-soft">
                    <tr>
                        <th scope="col" class="px-5 py-3.5 font-medium" aria-sort={ariaSort('name')}>
                            <button type="button" onclick={() => toggleSort('name')} class="inline-flex items-center gap-1 hover:text-ink">
                                {t.columns.name}
                                <span aria-hidden="true" class={sortKey === 'name' ? 'text-ink' : 'text-line'}>{sortKey === 'name' && sortDir === -1 ? '↓' : '↑'}</span>
                            </button>
                        </th>
                        <th scope="col" class="px-5 py-3.5 font-medium">{t.columns.domain}</th>
                        <th scope="col" class="px-5 py-3.5 font-medium">{t.columns.subdomains}</th>
                        <th scope="col" class="px-5 py-3.5 font-medium">{t.columns.labs}</th>
                        <th scope="col" class="px-5 py-3.5 text-right font-medium" aria-sort={ariaSort('size')}>
                            <button type="button" onclick={() => toggleSort('size')} class="inline-flex items-center gap-1 hover:text-ink">
                                {t.columns.entities}
                                <span aria-hidden="true" class={sortKey === 'size' ? 'text-ink' : 'text-line'}>{sortKey === 'size' && sortDir === 1 ? '↑' : '↓'}</span>
                            </button>
                        </th>
                        <th scope="col" class="px-5 py-3.5 font-medium">{t.columns.id}</th>
                        <th scope="col" class="px-5 py-3.5"><span class="sr-only">{t.columns.actions}</span></th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-line">
                    {#each slice as ex (ex.id)}
                        <tr class="align-top hover:bg-paper/60">
                            <th scope="row" class="max-w-[16rem] px-5 py-4 text-base font-semibold text-ink">
                                {@render highlighted(expertiseName(ex))}
                            </th>
                            <td class="px-5 py-4 text-ink-soft">{ex.domains.join(', ') || '—'}</td>
                            <td class="max-w-[16rem] px-5 py-4 leading-relaxed text-ink-soft">{ex.subdomains.join(', ') || '—'}</td>
                            <td class="px-5 py-4 text-ink-soft">{ex.labs.join(', ') || '—'}</td>
                            <td class="px-5 py-4 text-right text-base font-semibold tabular-nums text-ink">{i18n.num(ex.size)}</td>
                            <td class="px-5 py-4 text-ink-faint tabular-nums">{shortId(ex, graphId)}</td>
                            <td class="px-5 py-3 text-right">{@render viewButtonFor(ex)}</td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    {/if}

    {#if totalPages > 1}
        <nav class="flex items-center justify-center gap-3 pt-2" aria-label={t.pagesAria}>
            <button
                type="button"
                onclick={() => goTo(current - 1)}
                disabled={current === 0}
                class="inline-flex h-11 items-center gap-1.5 rounded-full bg-white px-5 text-base font-medium text-ink ring-1 ring-line transition-colors hover:bg-paper disabled:cursor-not-allowed disabled:opacity-40"
            >
                <svg viewBox="0 0 24 24" class="size-4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m15 6-6 6 6 6" /></svg>
                {t.previous}
            </button>
            <span class="px-2 text-base text-ink-soft tabular-nums">{t.pageOf(current + 1, totalPages)}</span>
            <button
                type="button"
                onclick={() => goTo(current + 1)}
                disabled={current >= totalPages - 1}
                class="inline-flex h-11 items-center gap-1.5 rounded-full bg-white px-5 text-base font-medium text-ink ring-1 ring-line transition-colors hover:bg-paper disabled:cursor-not-allowed disabled:opacity-40"
            >
                {t.next}
                <svg viewBox="0 0 24 24" class="size-4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 6 6 6-6 6" /></svg>
            </button>
        </nav>
    {/if}
</section>
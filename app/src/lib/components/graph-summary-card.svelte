<script lang="ts">

    import { i18n } from '$lib/i18n/index.svelte';

    let summary: App.GraphSummary = $props();


    let displayName = $derived(summary.name);
    let href = $derived(`/maps/${encodeURIComponent(summary.id)}`);

    let figures = $derived([
        { value: summary.number_of_expertises ?? 0, label: i18n.t.maps.card.expertises },
        { value: summary.domains?.length ?? 0,      label: i18n.t.maps.card.domains },
        { value: summary.labs?.length ?? 0,         label: i18n.t.maps.card.labs },
    ]);


</script>

<!-- The whole card is clickable through the title link's stretched hit area. -->
<article class="group relative flex flex-col rounded-3xl bg-white p-7 ring-1 ring-line transition-shadow duration-200 focus-within:ring-2 focus-within:ring-accent-light hover:shadow-[0_8px_30px_-12px_rgb(21_32_51/0.18)] hover:ring-ink-faint/40">

    <h2 class="text-xl leading-snug font-semibold text-ink capitalize">
        <a {href} class="outline-none after:absolute after:inset-0 after:rounded-3xl after:content-['']">
            {displayName}
        </a>
    </h2>

    <p class="mt-2 line-clamp-3 text-base leading-relaxed text-ink-soft">
        {summary.description || i18n.t.maps.card.noDescription}
    </p>

    <dl class="mt-6 mb-6 flex flex-wrap gap-x-6 gap-y-2">
        {#each figures as f}
            <div class="flex items-baseline gap-1.5">
                <dt class="order-2 text-sm text-ink-faint">{f.label(f.value)}</dt>
                <dd class="order-1 text-lg font-semibold tabular-nums text-ink">{i18n.num(f.value)}</dd>
            </div>
        {/each}
    </dl>

    <div class="mt-auto flex items-center justify-between gap-4 border-t border-line pt-5">
        <span class="text-base font-medium text-accent-light group-hover:underline group-hover:underline-offset-4">
            {i18n.t.maps.card.open}
        </span>
        <svg viewBox="0 0 24 24" class="size-5 text-accent-light transition-transform group-hover:translate-x-0.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 6 6 6-6 6" /></svg>
    </div>

</article>

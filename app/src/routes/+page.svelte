<script lang="ts">

    import HeroGraph from '$lib/components/hero-graph.svelte';
    import { listGraphs } from '$lib/services/api';
    import { i18n } from '$lib/i18n/index.svelte';

    // Live figures for the hero. Hidden if the API is unavailable.
    let stats: { maps: number; expertises: number; labs: number } | null = $state(null);

    $effect(() => {
        listGraphs()
            .then((graphs) => {
                if (graphs.length === 0) return;
                stats = {
                    maps: graphs.length,
                    expertises: graphs.reduce((sum, g) => sum + (g.number_of_expertises ?? 0), 0),
                    labs: new Set(graphs.flatMap((g) => g.labs ?? [])).size,
                };
            })
            .catch(() => (stats = null));
    });

    const FEATURE_ICONS = ['graph', 'filter', 'detail'] as const;

    let t = $derived(i18n.t.home);

</script>

<svelte:head>
    <title>{t.metaTitle}</title>
    <meta name="description" content={t.metaDescription} />
</svelte:head>

<main class="flex-1">

    <!-- Hero -->
    <section class="border-b border-line bg-white">
        <div class="mx-auto grid max-w-7xl items-center gap-12 px-5 py-16 sm:px-8 sm:py-20 lg:grid-cols-[1.05fr_1fr] lg:gap-16 lg:py-24">

            <div>
                <h1 class="text-[2rem] leading-[1.08] font-semibold tracking-[-0.025em] text-balance text-ink sm:text-5xl lg:text-[2.5rem]">
                    {t.heroTitle}
                </h1>
                <p class="mt-6 max-w-[36rem] text-lg leading-relaxed text-pretty text-ink-soft">
                    {t.heroText}
                </p>

                <div class="mt-9 flex flex-wrap items-center gap-3">
                    <a href="/maps" class="inline-flex h-12 items-center rounded-full bg-accent px-6 text-base font-medium text-white transition-colors hover:bg-accent-light">
                        {t.browseMaps}
                    </a>
                    <a href="#how-it-works" class="inline-flex h-12 items-center rounded-full border border-line px-6 text-base font-medium text-ink transition-colors hover:border-ink-faint hover:bg-paper">
                        {t.howBuilt}
                    </a>
                </div>

                {#if stats}
                    <dl class="mt-12 flex flex-wrap gap-x-10 gap-y-4 border-t border-line pt-6">
                        <div>
                            <dt class="text-sm text-ink-faint">{t.stats.maps}</dt>
                            <dd class="text-2xl font-semibold tabular-nums text-ink">{i18n.num(stats.maps)}</dd>
                        </div>
                        <div>
                            <dt class="text-sm text-ink-faint">{t.stats.expertises}</dt>
                            <dd class="text-2xl font-semibold tabular-nums text-ink">{i18n.num(stats.expertises)}</dd>
                        </div>
                        {#if stats.labs > 0}
                            <div>
                                <dt class="text-sm text-ink-faint">{t.stats.labs}</dt>
                                <dd class="text-2xl font-semibold tabular-nums text-ink">{i18n.num(stats.labs)}</dd>
                            </div>
                        {/if}
                    </dl>
                {/if}
            </div>

            <div class="rounded-[1.75rem] bg-paper p-2 ring-1 ring-line sm:p-4">
                <HeroGraph />
            </div>
        </div>
    </section>

    <!-- How a map is built: a real sequence, so the steps are numbered -->
    <section id="how-it-works" class="scroll-mt-24">
        <div class="mx-auto max-w-7xl px-5 py-20 sm:px-8 sm:py-24">
            <h2 class="max-w-xl text-3xl font-semibold tracking-[-0.02em] text-ink sm:text-[2.25rem] sm:leading-tight">
                {t.stepsTitle}
            </h2>
            <p class="mt-4 max-w-xl text-lg leading-relaxed text-ink-soft">{t.stepsIntro}</p>

            <ol class="mt-14 grid gap-10 sm:grid-cols-2 lg:grid-cols-4 lg:gap-8">
                {#each t.steps as step, i}
                    <li class="relative">
                        <div class="flex items-center gap-4">
                            <span class="flex size-10 shrink-0 items-center justify-center rounded-full bg-accent text-base font-semibold text-white tabular-nums">
                                {i + 1}
                            </span>
                            {#if i < t.steps.length - 1}
                                <span class="hidden h-px flex-1 bg-line lg:block" aria-hidden="true"></span>
                            {/if}
                        </div>
                        <h3 class="mt-5 text-lg font-semibold text-ink">{step.title}</h3>
                        <p class="mt-2 text-base leading-relaxed text-ink-soft">{step.text}</p>
                    </li>
                {/each}
            </ol>
        </div>
    </section>

    <!-- What you can do -->
    <section class="border-y border-line bg-white">
        <div class="mx-auto grid max-w-7xl gap-12 px-5 py-20 sm:px-8 sm:py-24 lg:grid-cols-[1fr_1.6fr] lg:gap-20">
            <div>
                <h2 class="text-3xl font-semibold tracking-[-0.02em] text-ink sm:text-[2.25rem] sm:leading-tight">
                    {t.featuresTitle}
                </h2>
                <p class="mt-4 max-w-md text-lg leading-relaxed text-ink-soft">{t.featuresIntro}</p>
            </div>

            <ul class="divide-y divide-line">
                {#each t.features as f, i}
                    <li class="flex gap-5 py-7 first:pt-0 last:pb-0">
                        <span class="flex size-12 shrink-0 items-center justify-center rounded-2xl bg-accent-muted text-accent">
                            <svg viewBox="0 0 24 24" class="size-6" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                                {#if FEATURE_ICONS[i] === 'graph'}
                                    <circle cx="5" cy="12" r="2.5" /><circle cx="18" cy="5.5" r="2.5" /><circle cx="18" cy="18.5" r="2.5" />
                                    <path d="M7.3 11 15.7 6.6M7.3 13l8.4 4.4" />
                                {:else if FEATURE_ICONS[i] === 'filter'}
                                    <path d="M4 5h16l-6 7.5V19l-4-2v-4.5L4 5Z" />
                                {:else}
                                    <circle cx="10.5" cy="10.5" r="6" /><path d="m15 15 5 5M8 10.5h5M10.5 8v5" />
                                {/if}
                            </svg>
                        </span>
                        <div>
                            <h3 class="text-lg font-semibold text-ink">{f.title}</h3>
                            <p class="mt-1.5 text-base leading-relaxed text-ink-soft">{f.text}</p>
                        </div>
                    </li>
                {/each}
            </ul>
        </div>
    </section>

    <!-- Closing call to action -->
    <section>
        <div class="mx-auto max-w-7xl px-5 py-20 sm:px-8 sm:py-24">
            <div class="flex flex-col items-start justify-between gap-8 rounded-[1.75rem] bg-accent px-8 py-12 text-white sm:px-12 md:flex-row md:items-center">
                <div>
                    <h2 class="text-2xl font-semibold tracking-[-0.015em] sm:text-3xl">{t.ctaTitle}</h2>
                    <p class="mt-2 max-w-lg text-lg leading-relaxed text-white/75">{t.ctaText}</p>
                </div>
                <a href="/maps" class="inline-flex h-12 shrink-0 items-center rounded-full bg-white px-6 text-base font-medium text-accent transition-colors hover:bg-accent-muted">
                    {t.browseMaps}
                </a>
            </div>
        </div>
    </section>

</main>

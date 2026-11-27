<script lang="ts">

    import { i18n } from '$lib/i18n/index.svelte';

    let t = $derived(i18n.t.about);

</script>

<svelte:head>
    <title>{t.metaTitle}{i18n.t.titleSuffix}</title>
    <meta name="description" content={t.metaDescription} />
</svelte:head>

<main class="flex-1">

    <header class="border-b border-line bg-white">
        <div class="mx-auto max-w-7xl px-5 py-16 sm:px-8 sm:py-20">
            <h1 class="text-4xl font-semibold tracking-[-0.025em] text-ink sm:text-5xl">{t.title}</h1>
            <p class="mt-5 max-w-2xl text-xl leading-relaxed text-pretty text-ink-soft">{t.lead}</p>
        </div>
    </header>

    <section class="mx-auto grid max-w-7xl gap-14 px-5 py-16 sm:px-8 sm:py-20 lg:grid-cols-[1.7fr_1fr] lg:gap-20">

        <div class="max-w-[40rem] space-y-6 text-lg leading-relaxed text-ink-soft">
            <h2 class="text-2xl font-semibold tracking-[-0.015em] text-ink">{t.whatTitle}</h2>
            {#each t.paragraphs as p}
                <p>{p}</p>
            {/each}
            <p>
                <a href="/#how-it-works" class="font-medium text-accent-light underline decoration-accent-light/30 underline-offset-4 hover:decoration-accent-light">
                    {t.howLink}
                </a>
            </p>
        </div>

        <aside class="h-fit rounded-3xl bg-white p-7 ring-1 ring-line">
            <h2 class="text-lg font-semibold text-ink">{t.detailsTitle}</h2>
            <dl class="mt-5 divide-y divide-line">
                {#each t.facts as { label, value }}
                    <div class="py-3.5 first:pt-0 last:pb-0">
                        <dt class="text-sm text-ink-faint">{label}</dt>
                        <dd class="mt-0.5 text-base font-medium text-ink">{value}</dd>
                    </div>
                {/each}
            </dl>
        </aside>
    </section>

    <section class="border-t border-line bg-white">
        <div class="mx-auto max-w-7xl px-5 py-16 sm:px-8 sm:py-20">
            <h2 class="text-2xl font-semibold tracking-[-0.015em] text-ink sm:text-3xl">{t.audienceTitle}</h2>
            <ul class="mt-10 grid gap-x-12 gap-y-8 sm:grid-cols-2">
                {#each t.audiences as { who, why }}
                    <li class="border-l-2 border-accent-muted pl-5">
                        <h3 class="text-lg font-semibold text-ink">{who}</h3>
                        <p class="mt-1.5 text-base leading-relaxed text-ink-soft">{why}</p>
                    </li>
                {/each}
            </ul>
        </div>
    </section>

    <section class="mx-auto max-w-7xl px-5 py-16 sm:px-8 sm:py-20">
        <div class="flex flex-col items-start justify-between gap-6 rounded-[1.75rem] bg-accent px-8 py-10 text-white sm:px-12 lg:flex-row lg:items-center">
            <div>
                <h2 class="text-2xl font-semibold tracking-[-0.015em]">{t.ctaTitle}</h2>
                <p class="mt-2 max-w-lg text-lg leading-relaxed text-white/75">{t.ctaText}</p>
            </div>
            <div class="flex flex-wrap gap-3">
                <a href="/contact" class="inline-flex h-12 items-center rounded-full bg-white px-6 text-base font-medium text-accent transition-colors hover:bg-accent-muted">
                    {t.ctaContact}
                </a>
                <a href="/maps" class="inline-flex h-12 items-center rounded-full px-6 text-base font-medium text-white ring-1 ring-white/35 transition-colors hover:bg-white/10">
                    {t.ctaMaps}
                </a>
            </div>
        </div>
    </section>

</main>

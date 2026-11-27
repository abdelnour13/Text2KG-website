<script lang="ts">

    import { i18n } from '$lib/i18n/index.svelte';

    let { data } = $props();

    let t = $derived(i18n.t.contact);

    let copied = $state(false);
    let copyTimer: ReturnType<typeof setTimeout> | undefined;

    let telHref = $derived('tel:' + data.phone.replace('(0)', '').replace(/[^\d+]/g, ''));
    let mapHref = $derived('https://www.openstreetmap.org/search?query=' + encodeURIComponent(data.address));

    async function copyEmail() {
        try {
            await navigator.clipboard.writeText(data.email);
            copied = true;
            clearTimeout(copyTimer);
            copyTimer = setTimeout(() => (copied = false), 2000);
        } catch {
            // Clipboard unavailable (e.g. insecure context): the mailto link still works.
        }
    }

</script>

<svelte:head>
    <title>{t.metaTitle}{i18n.t.titleSuffix}</title>
    <meta name="description" content={t.metaDescription} />
</svelte:head>

<main class="flex-1">

    <header class="border-b border-line bg-white">
        <div class="mx-auto max-w-7xl px-5 py-16 sm:px-8 sm:py-20">
            <h1 class="text-4xl font-semibold tracking-[-0.025em] text-ink sm:text-5xl">{t.title}</h1>
            <p class="mt-5 max-w-2xl text-xl leading-relaxed text-pretty text-ink-soft">
                {t.lead}
            </p>
        </div>
    </header>

    <section class="mx-auto grid max-w-7xl gap-6 px-5 py-16 sm:px-8 sm:py-20 lg:grid-cols-[1.4fr_1fr]">

        <!-- Primary: email -->
        <div class="flex flex-col justify-between gap-10 rounded-3xl bg-accent p-8 text-white sm:p-10">
            <div>
                <h2 class="text-lg font-medium text-white/75">{t.email}</h2>
                <p class="mt-2 text-2xl font-semibold tracking-[-0.01em] break-all sm:text-3xl">{data.email}</p>
            </div>
            <div class="flex flex-wrap gap-3">
                <a href="mailto:{data.email}" class="inline-flex h-12 items-center rounded-full bg-white px-6 text-base font-medium text-accent transition-colors hover:bg-accent-muted">
                    {t.writeEmail}
                </a>
                <button
                    type="button"
                    onclick={copyEmail}
                    class="inline-flex h-12 items-center rounded-full px-6 text-base font-medium text-white ring-1 ring-white/35 transition-colors hover:bg-white/10"
                >
                    {copied ? t.copied : t.copy}
                </button>
                <span class="sr-only" aria-live="polite">{copied ? t.copiedAnnouncement : ''}</span>
            </div>
        </div>

        <!-- Secondary: phone and address -->
        <div class="grid gap-6">
            <div class="rounded-3xl bg-white p-7 ring-1 ring-line">
                <h2 class="text-sm text-ink-faint">{t.phone}</h2>
                <a href={telHref} class="mt-1 block text-xl font-semibold text-ink hover:text-accent-light">{data.phone}</a>
            </div>

            <div class="rounded-3xl bg-white p-7 ring-1 ring-line">
                <h2 class="text-sm text-ink-faint">{t.address}</h2>
                <address class="mt-1 text-lg leading-relaxed font-medium text-ink not-italic">{data.address}</address>
                <a href={mapHref} target="_blank" rel="noopener noreferrer" class="mt-3 inline-block text-base font-medium text-accent-light underline decoration-accent-light/30 underline-offset-4 hover:decoration-accent-light">
                    {t.openMap}
                </a>
            </div>
        </div>

        {#if data.lab}
            <div class="rounded-3xl bg-white p-7 ring-1 ring-line lg:col-span-2">
                <h2 class="text-sm text-ink-faint">{t.team}</h2>
                <p class="mt-1 text-lg leading-relaxed font-medium text-ink" lang="fr">{data.lab}</p>
            </div>
        {/if}
    </section>

</main>

<script lang="ts">
    import { page } from '$app/state';
    import { i18n } from '$lib/i18n/index.svelte';

    let notFound = $derived(page.status === 404);
    let t = $derived(i18n.t.error);
</script>

<svelte:head>
    <title>{notFound ? t.notFoundMeta : t.otherMeta}{i18n.t.titleSuffix}</title>
</svelte:head>

<main class="flex flex-1 items-center justify-center px-5 py-24">
    <div class="max-w-lg text-center">
        <p class="text-8xl font-semibold tracking-[-0.04em] text-line tabular-nums select-none" aria-hidden="true">{page.status}</p>
        <h1 class="mt-4 text-3xl font-semibold tracking-[-0.02em] text-ink">
            {notFound ? t.notFoundTitle : t.otherTitle}
        </h1>
        <p class="mt-3 text-lg leading-relaxed text-ink-soft">
            {notFound ? t.notFoundText : t.otherText(page.error?.message ?? '')}
        </p>
        <div class="mt-8 flex flex-wrap justify-center gap-3">
            <a href="/" class="inline-flex h-12 items-center rounded-full bg-accent px-6 text-base font-medium text-white transition-colors hover:bg-accent-light">
                {t.home}
            </a>
            <a href={notFound ? '/maps' : '/contact'} class="inline-flex h-12 items-center rounded-full px-6 text-base font-medium text-ink ring-1 ring-line transition-colors hover:bg-paper">
                {notFound ? t.maps : t.contact}
            </a>
        </div>
    </div>
</main>

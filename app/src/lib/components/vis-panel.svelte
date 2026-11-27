<script lang="ts">

    import type { Snippet } from 'svelte';
    import VisualisationFrame from './ui/visualisation-frame.svelte';
    import { i18n } from '$lib/i18n/index.svelte';

    interface VisPanelProps {
        title: string;
        description: string;
        /** Name of the visualisation, shown in the frame's title bar. */
        frameTitle: string;
        onGenerate: () => Promise<App.VisualisationResponse>;
        /** Whether this panel's tab is visible. */
        active: boolean;
        /** Build the visualisation automatically the first time the tab is opened. */
        autoLoad?: boolean;
        /** Label of the build button when not auto-loading, e.g. "Show network". */
        actionLabel?: string;
        /** Label of the same button once a visualisation exists, e.g. "Update network". */
        updateLabel?: string;
        /** Text shown before anything is built (only when not auto-loading). */
        emptyText?: string;
        /** Extra controls (filters) shown above the button. */
        controls?: Snippet;
    }

    let {
        title, description, frameTitle, onGenerate, active,
        autoLoad = false, actionLabel = '', updateLabel = '',
        emptyText = '', controls,
    }: VisPanelProps = $props();

    let vis: App.VisualisationResponse | null = $state(null);
    let error: string | null = $state(null);
    let loading = $state(false);
    let attempted = $state(false);

    async function generate() {
        attempted = true;
        error = null;
        loading = true;
        try {
            vis = await onGenerate();
        } catch (err) {
            error = err instanceof Error ? err.message : 'Unknown error';
        } finally {
            loading = false;
        }
    }

    $effect(() => {
        if (active && autoLoad && !attempted) generate();
    });

</script>

<section class="space-y-6">
    <div class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div class="max-w-2xl">
            <h2 class="text-2xl font-semibold tracking-[-0.015em] text-ink sm:text-3xl">{title}</h2>
            <p class="mt-2 text-lg leading-relaxed text-ink-soft">{description}</p>
        </div>
        {#if autoLoad}
            <button
                type="button"
                onclick={generate}
                disabled={loading}
                class="inline-flex h-11 shrink-0 items-center gap-2 self-start rounded-full bg-white px-5 text-base font-medium text-ink ring-1 ring-line transition-colors hover:bg-paper disabled:cursor-wait disabled:opacity-50 sm:self-auto"
            >
                <svg viewBox="0 0 24 24" class={['size-4', loading && 'animate-spin']} fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 11a8 8 0 1 0-2.3 5.7M20 4v7h-7" /></svg>
                {i18n.t.vis.refresh}
            </button>
        {/if}
    </div>

    {#if controls}
        {@render controls()}
    {/if}

    {#if !autoLoad}
        <button
            type="button"
            onclick={generate}
            disabled={loading}
            class="inline-flex h-12 items-center gap-2 rounded-full bg-accent px-6 text-base font-medium text-white transition-colors hover:bg-accent-light disabled:cursor-wait disabled:opacity-70"
        >
            {vis ? updateLabel : actionLabel}
        </button>
    {/if}

    <VisualisationFrame
        title={frameTitle}
        url={vis?.url ?? null}
        {loading}
        {error}
        onRetry={generate}
        empty={!attempted && !autoLoad}
        {emptyText}
    />
</section>

<script lang="ts">
    // A visualisation area with a title bar that stays put while the graph is
    // being built, so the layout doesn't jump when the result arrives.

    import Spinner from './spinner.svelte';
    import { i18n } from '$lib/i18n/index.svelte';

    interface VisualisationFrameProps {
        title: string;
        url: string | null;
        loading: boolean;
        error: string | null;
        onRetry: () => void;
        /** Nothing requested yet: show a placeholder with this text instead of the frame. */
        empty?: boolean;
        emptyText?: string;
    }

    let { title, url, loading, error, onRetry, empty = false, emptyText = '' }: VisualisationFrameProps = $props();

</script>

{#if empty && !loading && !error}
    <div class="flex min-h-[240px] items-center justify-center rounded-2xl border-2 border-dashed border-line p-8 text-center">
        <p class="max-w-md text-base leading-relaxed text-ink-faint">{emptyText}</p>
    </div>
{:else}
    <div class="overflow-hidden rounded-2xl bg-white ring-1 ring-line">
        <div class="flex min-h-14 items-center justify-between gap-4 border-b border-line px-5 py-2.5">
            <p class="truncate text-sm font-medium text-ink">{title}</p>
            {#if url && !loading && !error}
                <a
                    href={url}
                    target="_blank"
                    rel="noopener noreferrer"
                    class="inline-flex h-9 shrink-0 items-center gap-2 rounded-full px-3.5 text-sm font-medium text-ink-soft ring-1 ring-line transition-colors hover:bg-paper hover:text-ink"
                >
                    <svg viewBox="0 0 24 24" class="size-4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                        <path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5" />
                    </svg>
                    {i18n.t.vis.openFull}
                </a>
            {/if}
        </div>

        <div class="relative h-[70vh] min-h-[520px]">
            {#if loading}
                <div class="absolute inset-0 flex flex-col items-center justify-center gap-4 bg-white text-center" role="status">
                    <Spinner size="lg" />
                    <p class="max-w-sm px-6 text-base text-ink-soft">{i18n.t.vis.building}</p>
                </div>
            {:else if error}
                <div class="absolute inset-0 flex flex-col items-center justify-center gap-2 p-8 text-center" role="alert">
                    <p class="text-lg font-semibold text-ink">{i18n.t.vis.errorTitle}</p>
                    <p class="max-w-md text-base text-ink-soft">{i18n.t.serverReturned} <span class="text-ink">{error}</span></p>
                    <button type="button" onclick={onRetry} class="mt-4 inline-flex h-11 items-center rounded-full bg-accent px-5 text-base font-medium text-white transition-colors hover:bg-accent-light">
                        {i18n.t.tryAgain}
                    </button>
                </div>
            {:else if url}
                <iframe src={url} {title} class="block h-full w-full border-0" sandbox="allow-scripts allow-same-origin"></iframe>
            {/if}
        </div>
    </div>
{/if}

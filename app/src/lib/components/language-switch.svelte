<script lang="ts">
    // Two-option switch between French and English. The choice is saved in the browser.
    import { i18n, LOCALES, type Locale } from '$lib/i18n/index.svelte';

    const NAMES: Record<Locale, string> = { fr: 'Français', en: 'English' };
</script>

<div class="inline-flex rounded-full bg-paper p-1 ring-1 ring-line" role="group" aria-label={i18n.t.language.label}>
    {#each LOCALES as l}
        <button
            type="button"
            lang={l}
            onclick={() => i18n.set(l)}
            aria-pressed={i18n.locale === l}
            aria-label={NAMES[l]}
            title={i18n.locale === l ? NAMES[l] : i18n.t.language.switchTo}
            class={[
                'h-8 min-w-11 rounded-full px-3 text-sm font-semibold tracking-wide transition-colors',
                i18n.locale === l ? 'bg-white text-ink shadow-sm ring-1 ring-line' : 'text-ink-faint hover:text-ink',
            ]}
        >
            {i18n.t.language.short[l]}
        </button>
    {/each}
</div>

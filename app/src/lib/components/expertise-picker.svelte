<script lang="ts">
    // Combobox: focusing the field drops down every expertise name; typing keeps
    // only the names that contain the typed characters (case and accents ignored).

    import { expertiseName, normalize, splitMatch } from '$lib/expertise';
    import { i18n } from '$lib/i18n/index.svelte';

    interface ExpertisePickerProps {
        expertises: App.Expertise[];
        selected: App.Expertise | null;
        onSelect: (ex: App.Expertise) => void;
    }

    let { expertises, selected, onSelect }: ExpertisePickerProps = $props();

    const uid = $props.id();
    const listId = `${uid}-list`;
    const optionId = (i: number) => `${uid}-opt-${i}`;

    let query = $state('');
    let open = $state(false);
    let activeIndex = $state(-1);
    let input: HTMLInputElement;
    let list: HTMLUListElement | undefined = $state();

    // Show the chosen name in the field, including when chosen from another tab.
    $effect(() => {
        query = selected ? expertiseName(selected) : '';
    });

    let sorted = $derived(
        [...expertises].sort((a, b) => i18n.compare(expertiseName(a), expertiseName(b)))
    );

    // When the field still shows the current selection, list everything.
    let filterText = $derived(selected && query === expertiseName(selected) ? '' : query.trim());

    let options = $derived.by(() => {
        const q = normalize(filterText);
        return q ? sorted.filter((ex) => normalize(expertiseName(ex)).includes(q)) : sorted;
    });

    function openList() {
        open = true;
        activeIndex = selected ? options.findIndex((o) => o.id === selected!.id) : -1;
        scrollActive();
    }

    function choose(ex: App.Expertise) {
        open = false;
        activeIndex = -1;
        query = expertiseName(ex);
        onSelect(ex);
    }

    function scrollActive() {
        requestAnimationFrame(() => {
            if (activeIndex < 0 || !list) return;
            list.querySelector(`#${CSS.escape(optionId(activeIndex))}`)?.scrollIntoView({ block: 'nearest' });
        });
    }

    function onKeydown(e: KeyboardEvent) {
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            if (!open) return openList();
            activeIndex = Math.min(options.length - 1, activeIndex + 1);
            scrollActive();
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            if (!open) return openList();
            activeIndex = Math.max(0, activeIndex - 1);
            scrollActive();
        } else if (e.key === 'Enter') {
            if (open && activeIndex >= 0 && options[activeIndex]) {
                e.preventDefault();
                choose(options[activeIndex]);
            } else if (open && options.length === 1) {
                e.preventDefault();
                choose(options[0]);
            }
        } else if (e.key === 'Escape') {
            if (open) {
                e.preventDefault();
                open = false;
            }
        }
    }

    function onInput() {
        open = true;
        activeIndex = options.length > 0 ? 0 : -1;
        scrollActive();
    }

    function clear() {
        query = '';
        input.focus();
        openList();
    }

</script>

<div class="relative w-full max-w-xl">
    <label for="{uid}-input" class="mb-2 block text-sm font-medium text-ink">{i18n.t.picker.label}</label>
    <div class="relative">
        <svg viewBox="0 0 24 24" class="pointer-events-none absolute top-1/2 left-4 size-5 -translate-y-1/2 text-ink-faint" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
            <circle cx="10.5" cy="10.5" r="6" /><path d="m15 15 5 5" />
        </svg>
        <input
            bind:this={input}
            id="{uid}-input"
            type="text"
            role="combobox"
            aria-expanded={open}
            aria-controls={listId}
            aria-autocomplete="list"
            aria-activedescendant={open && activeIndex >= 0 ? optionId(activeIndex) : undefined}
            autocomplete="off"
            spellcheck="false"
            placeholder={i18n.t.picker.placeholder}
            bind:value={query}
            oninput={onInput}
            onfocus={openList}
            onclick={() => !open && openList()}
            onblur={() => (open = false)}
            onkeydown={onKeydown}
            class={[
                'h-12 w-full border border-line bg-white pr-20 pl-12 text-base text-ink placeholder:text-ink-faint focus:border-accent-light focus:outline-none',
                open ? 'rounded-t-3xl rounded-b-none' : 'rounded-full focus:ring-4 focus:ring-accent-light/15',
            ]}
        />
        <div class="absolute top-1/2 right-2 flex -translate-y-1/2 items-center">
            {#if query}
                <button type="button" onmousedown={(e) => e.preventDefault()} onclick={clear} class="flex size-9 items-center justify-center rounded-full text-ink-faint hover:bg-paper hover:text-ink" aria-label={i18n.t.picker.clear}>
                    <svg viewBox="0 0 24 24" class="size-4" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18" /></svg>
                </button>
            {/if}
            <button
                type="button"
                tabindex="-1"
                onmousedown={(e) => e.preventDefault()}
                onclick={() => (open ? (open = false) : (input.focus(), openList()))}
                class="flex size-9 items-center justify-center rounded-full text-ink-faint hover:bg-paper hover:text-ink"
                aria-label={open ? i18n.t.picker.hide : i18n.t.picker.showAll}
            >
                <svg viewBox="0 0 24 24" class={['size-5 transition-transform', open && 'rotate-180']} fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6" /></svg>
            </button>
        </div>
    </div>

    {#if open}
        <div class="absolute inset-x-0 top-full z-20 overflow-hidden rounded-b-3xl border border-t-0 border-accent-light bg-white shadow-[0_16px_40px_-16px_rgb(21_32_51/0.35)]">
            <p class="border-b border-line px-5 py-2.5 text-sm text-ink-faint" aria-live="polite">
                {filterText ? i18n.t.picker.matching(options.length, expertises.length, filterText) : i18n.t.picker.total(expertises.length)}
            </p>
            <ul bind:this={list} id={listId} role="listbox" aria-label={i18n.t.picker.listAria} class="max-h-80 overflow-y-auto py-1.5">
                {#each options as ex, i (ex.id)}
                    {@const [before, match, after] = splitMatch(expertiseName(ex), filterText)}
                    <!-- Keyboard selection is handled on the input (aria-activedescendant). -->
                    <!-- svelte-ignore a11y_click_events_have_key_events -->
                    <li
                        id={optionId(i)}
                        role="option"
                        aria-selected={selected?.id === ex.id}
                        onmousedown={(e) => e.preventDefault()}
                        onclick={() => choose(ex)}
                        onmousemove={() => (activeIndex = i)}
                        class={[
                            'mx-1.5 flex cursor-pointer items-baseline justify-between gap-4 rounded-xl px-3.5 py-2.5',
                            i === activeIndex ? 'bg-accent-muted' : '',
                        ]}
                    >
                        <span class={['text-base', selected?.id === ex.id ? 'font-semibold text-accent' : 'text-ink']}>
                            {before}{#if match}<strong class="font-semibold text-accent">{match}</strong>{/if}{after}
                        </span>
                        <span class="shrink-0 text-sm text-ink-faint tabular-nums">{i18n.t.picker.entities(ex.size)}</span>
                    </li>
                {:else}
                    <li class="px-5 py-6 text-center text-base text-ink-soft">{i18n.t.picker.none(filterText)}</li>
                {/each}
            </ul>
        </div>
    {/if}
</div>

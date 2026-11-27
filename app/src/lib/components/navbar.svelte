<script lang="ts">

    import { page } from '$app/state';
    import logo from '$lib/assets/logo.png';
    import ls2n from '$lib/assets/ls2n.webp';
    import LanguageSwitch from './language-switch.svelte';
    import { i18n } from '$lib/i18n/index.svelte';

    let links = $derived([
        { to: '/',        label: i18n.t.nav.home    },
        { to: '/maps',    label: i18n.t.nav.maps    },
        { to: '/about',   label: i18n.t.nav.about   },
        { to: '/contact', label: i18n.t.nav.contact },
    ]);

    let menuOpen = $state(false);

    const trim = (to: string) => to.replace(/^\/+|\/+$/g, '');

    // "/maps/abc" keeps "Expertise maps" highlighted.
    const isActive = (to: string) => {
        const current = trim(page.url.pathname);
        const target = trim(to);
        return target === '' ? current === '' : current === target || current.startsWith(target + '/');
    };

    // Close the mobile menu after navigating.
    $effect(() => {
        page.url.pathname;
        menuOpen = false;
    });

</script>

<header class="sticky top-0 z-30 border-b border-line bg-white/85 backdrop-blur-md">

    <div class="mx-auto flex h-18 max-w-7xl items-center justify-between gap-6 px-5 sm:px-8">

        <a href="/" class="flex shrink-0 items-center gap-4" aria-label={i18n.t.nav.homeAria}>
            <img src={logo} alt="" class="h-8 w-auto sm:h-9" />
            <span class="h-7 w-px bg-line" aria-hidden="true"></span>
            <img src={ls2n} alt="LS2N" class="h-7 w-auto sm:h-8" />
        </a>

        <div class="flex items-center gap-3">
            <nav class="hidden items-center gap-1 lg:flex" aria-label={i18n.t.nav.mainAria}>
                {#each links as { label, to }}
                    <a
                        href={to}
                        aria-current={isActive(to) ? 'page' : undefined}
                        class={[
                            'rounded-full px-4 py-2 text-[0.95rem] whitespace-nowrap transition-colors duration-150',
                            isActive(to)
                                ? 'bg-accent-muted font-medium text-accent'
                                : 'text-ink-soft hover:bg-paper hover:text-ink',
                        ]}
                    >
                        {label}
                    </a>
                {/each}
            </nav>

            <span class="hidden h-6 w-px bg-line lg:block" aria-hidden="true"></span>
            <LanguageSwitch />

            <button
                type="button"
                class="-me-2 inline-flex size-11 items-center justify-center rounded-full text-ink hover:bg-paper lg:hidden"
                aria-expanded={menuOpen}
                aria-controls="mobile-nav"
                aria-label={menuOpen ? i18n.t.nav.closeMenu : i18n.t.nav.openMenu}
                onclick={() => (menuOpen = !menuOpen)}
            >
                <svg viewBox="0 0 24 24" class="size-6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true">
                    {#if menuOpen}
                        <path d="M6 6l12 12M18 6L6 18" />
                    {:else}
                        <path d="M4 7h16M4 12h16M4 17h16" />
                    {/if}
                </svg>
            </button>
        </div>
    </div>

    {#if menuOpen}
        <nav id="mobile-nav" class="border-t border-line bg-white px-5 pt-2 pb-4 lg:hidden" aria-label={i18n.t.nav.mainAria}>
            {#each links as { label, to }}
                <a
                    href={to}
                    aria-current={isActive(to) ? 'page' : undefined}
                    class={[
                        'block rounded-lg px-3 py-3 text-base',
                        isActive(to) ? 'bg-accent-muted font-medium text-accent' : 'text-ink-soft hover:bg-paper',
                    ]}
                >
                    {label}
                </a>
            {/each}
        </nav>
    {/if}
</header>

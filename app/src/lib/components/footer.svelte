<script lang="ts">

    import { i18n } from '$lib/i18n/index.svelte';

    interface IProps {
        email: string;
        phone: string;
        address: string;
        lab?: string;
    }

    let props: IProps = $props();

    let links = $derived([
        { to: '/',        label: i18n.t.footer.links.home },
        { to: '/maps',    label: i18n.t.footer.links.maps },
        { to: '/about',   label: i18n.t.footer.links.about },
        { to: '/contact', label: i18n.t.footer.links.contact },
    ]);

</script>

<footer class="mt-auto border-t border-line bg-white">

    <div class="mx-auto grid max-w-7xl grid-cols-1 gap-10 px-5 py-14 sm:px-8 md:grid-cols-[1.4fr_1fr_1fr]">

        <div class="max-w-sm">
            <p class="text-lg font-semibold text-ink">{i18n.t.siteName}</p>
            <p class="mt-2 text-[0.95rem] leading-relaxed text-ink-soft">{i18n.t.footer.tagline}</p>
            {#if props.lab}
                <p class="mt-4 text-sm leading-relaxed text-ink-faint" lang="fr">{props.lab}</p>
            {/if}
        </div>

        <div>
            <h2 class="text-sm font-semibold text-ink">{i18n.t.footer.contact}</h2>
            <ul class="mt-3 space-y-2 text-[0.95rem] text-ink-soft">
                <li><a href="mailto:{props.email}" class="break-all hover:text-accent-light">{props.email}</a></li>
                <li><a href="tel:{props.phone.replace('(0)', '').replace(/[^\d+]/g, '')}" class="hover:text-accent-light">{props.phone}</a></li>
                <li class="leading-relaxed">{props.address}</li>
            </ul>
        </div>

        <nav aria-label={i18n.t.footer.footerAria}>
            <h2 class="text-sm font-semibold text-ink">{i18n.t.footer.pages}</h2>
            <ul class="mt-3 space-y-2 text-[0.95rem] text-ink-soft">
                {#each links as { to, label }}
                    <li><a href={to} class="hover:text-accent-light">{label}</a></li>
                {/each}
            </ul>
        </nav>
    </div>

    <div class="border-t border-line">
        <p class="mx-auto max-w-7xl px-5 py-5 text-sm text-ink-faint sm:px-8">
            © {new Date().getFullYear()} Nantes Université
        </p>
    </div>
</footer>

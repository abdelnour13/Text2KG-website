<script lang="ts" >

    import { page } from '$app/state';
    import logo from '$lib/assets/logo.png';
    import ls2n from '$lib/assets/ls2n.webp';

    const NAV_LINKS = [
        { to: '/',       label: 'Home'           },
        { to: '/about',  label: 'About Project'  },
        { to: '/maps', label: 'Expertise Maps' },
        { to: '/contact',label: 'Contacts'       },
    ]

    const trim = (to : string) => {
        
        if (to.at(0) === '/') {
            to = to.slice(1)
        }

        if (to.at(to.length-1) == '/') {
            to = to.slice(0, to.length - 1)
        }

        return to;

    }

    const isActive = (to: string) => {
        return trim(page.url.pathname) == trim(to);
    }

</script>


<header class="sticky top-0 z-30 bg-white border-b border-stone-200">

    <div class="max-w-6xl mx-auto px-4 sm:px-6 flex items-center justify-between h-14 mb-2 mt-4">

        <a href="/" class="flex items-center gap-2.5 shrink-0" aria-label="home" >
            <span class="w-32 flex items-center justify-center me-6">
                <img src={logo} alt="" />
            </span>
            <span class="w-20 flex items-center justify-center">
                <img src={ls2n} alt="" />
            </span>
        </a>

        <nav class="flex items-center gap-1">
            {#each NAV_LINKS as { label, to } }
                <a
                    href={to}
                    class={
                        [
                            'px-3 py-1.5 text-sm rounded transition-colors duration-150',
                            isActive(to)
                            ? 'text-accent font-medium bg-accent-muted'
                            : 'text-stone-600 hover:text-stone-900 hover:bg-stone-100',
                        ].join(' ')
                    }
                >
                    {label}
                </a>
            {/each}
            
        </nav>
    </div>
</header>
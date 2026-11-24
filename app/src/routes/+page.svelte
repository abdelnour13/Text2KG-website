<script lang="ts" >

    import graph from '$lib/assets/graph.svg';
    import search from '$lib/assets/search.svg';
    import download from '$lib/assets/download.svg';

    interface Feature {
        icon: string;
        title: string;
        description: string;
    }

    const FEATURES : Feature[] = [
        {
            icon: graph,
            title: 'Interactive Graph Exploration',
            description:
                'Visualise expertise communities, subdomains, and research entities as interactive network graphs powered by Neo4j.',
        },
        {
            icon: search,
            title: 'Taxonomy Browsing',
            description:
                'Navigate domain and subdomain hierarchies to quickly understand the structure of any expertise map.',
        },
        {
            icon: download,
            title: 'Data Export',
            description:
                'Download full graph data as structured JSON for integration into your own analysis pipeline.',
        },
    ]

</script>

<main class="flex-1">

    <section class="border-b border-stone-200 bg-white">
        <div class="max-w-6xl mx-auto px-4 sm:px-6 py-20 sm:py-28">
            <div class="max-w-2xl animate-slide-up">
                <p class="section-label mb-3">Research Knowledge Platform</p>
                <h1 class="text-3xl sm:text-4xl font-semibold text-stone-900 leading-tight mb-4 tracking-tight">
                    Explore academic expertise through graph intelligence
                </h1>
                <p class="text-stone-500 text-base leading-relaxed mb-8">
                    The Expertise Map platform enables researchers, institutions, and industry partners
                    to navigate, visualise, and understand the landscape of scientific knowledge
                    structured as an interconnected graph.
                </p>
                <div class="flex items-center gap-3">
                    <a href="/graphs" class="btn-primary px-5 py-2.5">
                    Browse Expertise Maps
                    </a>
                    <a href="/about" class="btn-secondary px-5 py-2.5">
                    Learn more
                    </a>
                </div>
            </div>
        </div>
    </section>

    <section class="max-w-6xl mx-auto px-4 sm:px-6 py-16">
        <p class="section-label mb-8">What you can do</p>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
            {#each FEATURES as f}
                <div class="space-y-2">
                    <div class="w-8 h-8 rounded bg-accent-muted flex items-center justify-center text-accent">
                        <img src={f.icon} alt=""  />
                    </div>
                    <h3 class="text-sm font-semibold text-stone-800">{f.title}</h3>
                    <p class="text-xs text-stone-500 leading-relaxed">{f.description}</p>
                </div>
            {/each}
        </div>
    </section>

</main>
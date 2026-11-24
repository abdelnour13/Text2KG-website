<script lang="ts" >

    const SIDE_ITEMS = [
        { label: 'Institution',   value: 'Université de Nantes' },
        { label: 'Data Source',   value: 'Scientific publication corpus' },
        { label: 'Graph Backend', value: 'Neo4j' },
        { label: 'Status',        value: 'Active research project' },
    ]

</script>

<main class="flex-1 max-w-6xl mx-auto px-4 sm:px-6 py-14 animate-fade-in">

    <p class="section-label mb-2">About</p>
    <h1 class="text-2xl font-semibold text-stone-900 mb-6 tracking-tight">About the Project</h1>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-10">

        <div class="md:col-span-2 space-y-6 text-sm text-stone-600 leading-relaxed">
            <p>
            The <strong class="text-stone-800 font-medium">Expertise Map</strong> project
            is a research initiative aimed at structuring and visualising the collective
            scientific knowledge produced within academic institutions.
            </p>
            <p>
            Using a knowledge graph approach, scientific publications are processed to extract
            entities, concepts, and relational knowledge. These are then organised into
            communities of expertise, linked to thematic subdomains and broader research domains.
            </p>
            <p>
            The platform is designed for use by researchers, research administrators, industry
            partners, and funding agencies who need to understand where expertise lies, how it
            clusters, and how it connects across disciplines.
            </p>

            <div class="border-l-2 border-accent-muted pl-4">
            <p class="text-xs text-stone-500 italic">
                "Making the invisible structure of scientific knowledge navigable and explorable."
            </p>
            </div>
        </div>

        <div class="space-y-6">
            {#each SIDE_ITEMS as { label, value }}
                <div>
                    <p class="section-label">{label}</p>
                    <p class="text-sm text-stone-700">{value}</p>
                </div>
            {/each}
        </div>
    </div>

</main>
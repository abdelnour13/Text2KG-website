<script lang="ts" >

    let { data } = $props();

    let contacts = $derived(Object.entries(data).map(([key, value]) => {
        return {
            'label': key.charAt(0).toUpperCase() + key.slice(1),
            'value': value
        }
    }))

</script>

<main class="flex-1 max-w-6xl mx-auto px-4 sm:px-6 py-14 animate-fade-in">

    <p class="section-label mb-2">Get in touch</p>
    <h1 class="text-2xl font-semibold text-stone-900 mb-8 tracking-tight">Contacts</h1>

    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {#each contacts as { label, value }}
            <div class="card">
                <p class="section-label mb-1">{label}</p>
                <p class="text-sm text-stone-700">{value}</p>
            </div>
        {/each}
    </div>

    <div class="mt-10 max-w-md">
    <p class="section-label mb-2">Send a message</p>
    <p class="text-xs text-stone-400">
        Contact form — coming soon. In the meantime, please reach out by email.
    </p>
    </div>
</main>
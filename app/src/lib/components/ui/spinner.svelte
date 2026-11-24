<script lang="ts" >

    const data : { size : 'sm' | 'md' | 'lg' } = $props();
    const dim = $derived({ sm: 'w-4 h-4', md: 'w-6 h-6', lg: 'w-8 h-8' }[data.size]);

</script>

<span
    class={`${dim} border-2 border-stone-200 border-t-accent rounded-full animate-spin inline-block`}
    role="status"
    aria-label="Loading"
></span>
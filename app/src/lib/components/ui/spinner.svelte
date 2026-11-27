<script lang="ts">

    const data: { size: 'sm' | 'md' | 'lg' } = $props();
    const dim = $derived({ sm: 'size-4', md: 'size-6', lg: 'size-9' }[data.size]);

</script>

<span class={[dim, 'inline-block animate-spin rounded-full border-[3px] border-line border-t-accent-light']} aria-hidden="true"></span>

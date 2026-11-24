<script lang="ts" >

    let data : { open : boolean } = $props();

</script>

<svg
    width="14" height="14" viewBox="0 0 16 16" fill="none"
    class={`shrink-0 transition-transform duration-200 ${data.open ? 'rotate-180' : ''}`}
>
    <path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
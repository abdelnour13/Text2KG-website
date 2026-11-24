<script lang="ts" >

    let data : { message : string } = $props();

</script>

<div class="rounded border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
    {data.message}
</div>
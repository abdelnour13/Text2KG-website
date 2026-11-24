<script lang="ts">

	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';
	import Navbar from '$lib/components/navbar.svelte';
	import Footer from '$lib/components/footer.svelte';

	let { children, data }= $props();
	
</script>

<svelte:head><link rel="icon" href={favicon} /></svelte:head>

<div class="min-h-screen flex flex-col">
	<Navbar />
	{@render children()}
	<Footer address={data.address} email={data.email} phone={data.phone} />
</div>

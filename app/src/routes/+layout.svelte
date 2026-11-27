<script lang="ts">

	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';
	import Navbar from '$lib/components/navbar.svelte';
	import Footer from '$lib/components/footer.svelte';
	import { i18n } from '$lib/i18n/index.svelte';

	let { children, data } = $props();

	// Keep <html lang> in step with the chosen language (screen readers, hyphenation).
	$effect(() => {
		document.documentElement.lang = i18n.locale;
	});

</script>

<svelte:head><link rel="icon" href={favicon} /></svelte:head>

<div class="min-h-screen flex flex-col">
	<Navbar />
	{@render children()}
	<Footer address={data.address} email={data.email} phone={data.phone} lab={data.lab} />
</div>

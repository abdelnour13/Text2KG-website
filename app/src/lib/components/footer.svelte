<script lang="ts" >

    interface IProps {
        email: string;
        phone: string;
        address: string;
    };

    let props : IProps = $props();

</script>

<footer class="border-t border-stone-200 bg-white mt-auto">

    <div class="max-w-6xl mx-auto px-4 sm:px-6 py-10 grid grid-cols-1 sm:grid-cols-3 gap-8">

    <div>
        <p class="text-sm font-semibold text-stone-800 mb-2">Expertise Map</p>
        <p class="text-xs text-stone-500 leading-relaxed">
        A knowledge graph platform for exploring research expertise and academic networks.
        </p>
    </div>

    <div>
        <p class="section-label">Contact</p>
        <ul class="space-y-1 text-xs text-stone-500">
        <li>{props.email}</li>
        <li>{props.phone}</li>
        <li>{props.address}</li>
        </ul>
    </div>

    <div>
        <p class="section-label">Links</p>
        <ul class="space-y-1 text-xs text-stone-500">
        <li><a href="/" class="hover:text-accent transition-colors">Home</a></li>
        <li><a href="/about" class="hover:text-accent transition-colors">About Project</a></li>
        <li><a href="/graphs" class="hover:text-accent transition-colors">Expertise Maps</a></li>
        </ul>
    </div>
    </div>

    <div class="border-t border-stone-100 py-4 text-center text-xs text-stone-400">
    © {new Date().getFullYear()} Nantes University. All rights reserved.
    </div>
</footer>
<script lang="ts" >
    import { page } from '$app/state';
</script>

{page.error?.message}
{#if page.status == 404}

    <main class="flex-1 flex items-center justify-center py-24 animate-fade-in">
        <div class="text-center max-w-sm">
            <p class="text-7xl font-mono font-semibold text-stone-200 mb-4 select-none">404</p>
            <h1 class="text-lg font-semibold text-stone-800 mb-2">Page not found</h1>
            <p class="text-sm text-stone-500 mb-6">
                The page you're looking for doesn't exist or has been moved.
            </p>
            <a href="/" class="btn-primary">
                ← Back to Home
            </a>
        </div>
    </main>

{:else}
    <main class="flex-1 flex items-center justify-center py-24 animate-fade-in">
        <div class="text-center max-w-sm">
            <p class="text-7xl font-mono font-semibold text-stone-200 mb-4 select-none">{page.status}</p>
            <h1 class="text-lg font-semibold text-stone-800 mb-2">Unexpected error happened</h1>
            <p class="text-sm text-stone-500 mb-6">
                If you think that this a technical error please don't hesitate to contact us.
            </p>
            <div>
                <a href="/" class="btn-primary">
                    ← Back to Home
                </a>
                <a href="/contact" class="btn-primary">
                    Contact form
                </a>
            </div>
        </div>
    </main>
{/if}
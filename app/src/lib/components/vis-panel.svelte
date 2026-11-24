<script lang="ts" >

    import Spinner from "./ui/spinner.svelte";
    import ErrorMessage from "./ui/error-message.svelte";
    import VisualisationFrame from "./ui/visualisation-frame.svelte";

    interface VisPanelProps {
        title: string;
        description: string;
        onGenerate: () => Promise<App.VisualisationResponse>
    };

    let { title, description, onGenerate } : VisPanelProps = $props();
    let vis : App.VisualisationResponse | null = $state(null);
    let error : string | null = $state(null);
    let loading : boolean = $state(false);

    const handleGenerate = async () => {

        error = null;
        loading = true;

        try {
            vis = await onGenerate()
        } catch (err) {
           error = err instanceof Error ? err.message : 'Failed to generate visualisation';
        } finally {
            loading = false;
        }
    }

</script>

<section class="space-y-4">

    <h2 class="text-base font-semibold text-stone-800 border-b border-stone-100 pb-2 mb-4">
        {title}
    </h2>

    {#if description}
        <p class="text-sm text-stone-500">{description}</p>
    {/if}

    {#if !vis}
        <button
            onclick={handleGenerate}
            disabled={loading}
            class="btn-primary"
        >
            {#if loading}
                <Spinner size="sm" />
                Generating…
            {:else}
                Generate Visualisation
            {/if}
        </button>
    {/if}


    {#if error}
        <ErrorMessage message={error} />
    {/if}

    {#if vis}
        <div class="animate-fade-in">
            <VisualisationFrame url={vis.url} filename={vis.filename} title={title} />
            <button
                onclick={handleGenerate}
                class="btn-ghost text-xs mt-2"
            >
                ↺ Regenerate
            </button>
        </div>
    {/if}

</section>
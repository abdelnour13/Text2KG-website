<script lang='ts'>

	import type { EventHandler } from "svelte/elements";
    import { visExpertiseDetail } from "$lib/services/api";
    import ErrorMessage from "./ui/error-message.svelte";
    import VisualisationFrame from "./ui/visualisation-frame.svelte";
    import Spinner from "./ui/spinner.svelte";

    interface CommunityVisPanelProps {
        graphId : string;
    }


    let { graphId } : CommunityVisPanelProps = $props();

    let communityId : string = $state('');
    let loading : boolean = $state(false);
    let error : string | null = $state(null);
    let vis : App.VisualisationResponse | null = $state(null);

    const handleSubmit : EventHandler<SubmitEvent, HTMLFormElement> = async (e) => {

        e.preventDefault()

        if(!communityId) return;

        const trimmed = communityId.trim();

        if (!trimmed) return;

        error = null;
        vis = null;
        loading = true;

        try {
            vis = await visExpertiseDetail(graphId, `${graphId}_${trimmed}`)
        } catch (err) {
           error = err instanceof Error ? err.message : 'Failed to generate visualisation'
        } finally {
            loading = false;
        }

    }

</script>

<section class="space-y-4">

    <h2 class="text-base font-semibold text-stone-800 border-b border-stone-100 pb-2 mb-4">
        Community Visualisation
    </h2>

    <p class="text-sm text-stone-500">
        Enter a community (expertise) ID to visualise its entities, subdomains, and domain connections.
    </p>

    <form onsubmit={handleSubmit} class="flex items-center gap-2 max-w-sm">
        <input
            type="text"
            value={communityId}
            oninput={(e) => {
                let target = e.target as HTMLInputElement;
                console.log(`Value ${target.value}`)
                communityId = target.value;
            }}
            placeholder="Community ID"
            class="input"
            required
        />
        <button
            type="submit"
            disabled={loading || !communityId.trim()}
            class="btn-primary shrink-0"
        >
            {#if loading}
            <Spinner size="sm" /> 
            {:else} 
            Visualize
            {/if}
        </button>
    </form>

        {#if error}
            <ErrorMessage message={error} />
        {/if}

        {#if vis}
            <div class="animate-fade-in">
            <VisualisationFrame
                url={vis.url}
                filename={vis.filename}
                title={`Community ${communityId}`}
            />
            </div>  
        {/if}
    </section>
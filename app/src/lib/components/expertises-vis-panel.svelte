<script lang="ts" >

    import Spinner from "./ui/spinner.svelte";
    import ErrorMessage from "./ui/error-message.svelte";
    import VisualisationFrame from "./ui/visualisation-frame.svelte";
    import FilterPanel from "./filter-panel.svelte";
    import { visExpertises } from "$lib/services/api";

    interface VisPanelProps {
        title: string;
        description: string;
        domains: string[]
        subdomains: string[]
        labs: string[]
        graphId : string;
    };

    let { title, description, graphId, domains, labs, subdomains } : VisPanelProps = $props();
    let vis : App.VisualisationResponse | null = $state(null);
    let error : string | null = $state(null);
    let loading : boolean = $state(false);
    
    let getExpertiseVisualization = $state(async () => {
        return visExpertises(graphId, {
            domains: undefined,
            subdomains: undefined,
            labs: undefined
        })
    })

    const onTogglePanelInputChange = (
        mode : 'domain' | 'subdomain',
        labs : Set<string>, 
        domains : Set<string>, 
        subdomains : Set<string>
    ) => {
        getExpertiseVisualization = () => visExpertises(graphId, {
            subdomains: (mode == 'subdomain' && subdomains.size > 0) ? [...subdomains] : undefined,
            domains: (mode == 'domain' && domains.size > 0) ? [...domains] : undefined,
            labs: (labs.size > 0) ? [...labs] : undefined
        })
    }

    const handleGenerate = async () => {

        error = null;
        loading = true;

        try {
            vis = await getExpertiseVisualization()
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

    <FilterPanel 
        domains={domains}
        subdomains={subdomains}
        labs={labs}
        onInputChange={onTogglePanelInputChange}
    /> 

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
<script lang="ts" >

    import downloadIcon from '$lib/assets/download.svg';
    import type { PageData, RouteParams } from "../$types";
    import Spinner from "$lib/components/ui/spinner.svelte";
    import ErrorMessage from "$lib/components/ui/error-message.svelte";
    import { getGraph, downloadGraph, visTaxonomy, visExpertises, visSummary } from "$lib/services/api";
    import ExpertiseGrid from '$lib/components/expertise-grid.svelte';
    import VisPanel from '$lib/components/vis-panel.svelte';
    import ExpertisesVisPanel from '$lib/components/expertises-vis-panel.svelte';
    import CommunityVisPanel from '$lib/components/community-vis-panel.svelte';

    interface GraphPageProps {
        params : RouteParams & { id : string };
        data : PageData
    };

    let { params } : GraphPageProps = $props();

    let loading = $state(false);
    let error : string | null = $state(null);
    let downloading = $state(false);
    let downloadingError : string | null = $state(null);
    let detail : App.GraphDetail | null = $state(null);

    let displayName = $derived(params.id.split('_').join(' '));

    let getExpertiseVisualization = $state(async () => {
        return visExpertises(params.id, {
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
        getExpertiseVisualization = () => visExpertises(params.id, {
            subdomains: (mode == 'subdomain' && subdomains.size > 0) ? [...subdomains] : undefined,
            domains: (mode == 'domain' && domains.size > 0) ? [...domains] : undefined,
            labs: (labs.size > 0) ? [...labs] : undefined
        })
    }

    $effect(() => {
        loading = true;
        error = null;
        getGraph(params.id)
            .then(d => {
                detail = d;
                loading = false;
            })
            .catch((err) => {
                error = err instanceof Error ? err.message : 'Failed to load graph';
                loading = false;
            })
            .finally(() => loading = false)
    })

    const handleDownload = async () => {
        
        downloadingError = null;
        downloading = true;

        try {
            await downloadGraph(params.id)
        } catch (err) {
            downloadingError = err instanceof Error ? err.message : 'Download failed'
        } finally {
            downloading = false;
        }
    }

</script>

{#if loading}
    <main class="flex-1 flex items-center justify-center py-24">
        <div class="flex items-center gap-3 text-stone-400">
            <Spinner size="md" />
            <span class="text-sm">Loading…</span>
        </div>
    </main>
{/if}

{#if error}
    <main class="flex-1 flex items-center justify-center py-24">
        <ErrorMessage message={error} />
        <a href="/graphs" class="btn-ghost mt-4 inline-flex">← Back to Expertise Maps</a>
    </main>
{/if}

{#if detail}

    <main class="flex-1 max-w-6xl mx-auto px-4 sm:px-6 py-14 space-y-12 animate-fade-in">

        <nav class="text-xs text-stone-400 flex items-center gap-1.5">
            <a href="/graphs" class="hover:text-accent transition-colors">Expertise Maps</a>
            <span>/</span>
            <span class="text-stone-600 capitalize">{displayName}</span>
        </nav>

        <section>

            <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4 mb-6">
                <div>
                    <p class="section-label mb-1">Expertise map</p>
                    <h1 class="text-2xl font-semibold text-stone-900 capitalize tracking-tight">
                    {displayName}
                    </h1>
                </div>
                <div class="flex items-center gap-2 shrink-0">
                    <button
                        onclick={handleDownload}
                        disabled={downloading}
                        class="btn-secondary"
                    >
                        <img src={downloadIcon} alt="" />
                    {downloading ? 'Downloading…' : 'Download JSON'}
                    </button>
                </div>
            </div>

            {#if downloadingError}
                <ErrorMessage message={downloadingError} />
            {/if}

            <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4 mb-12" >

                <div>
                    <p class="text-sm text-stone-500 leading-relaxed mb-6 max-w-2xl">
                        {detail.description || 'No description available.'}
                    </p>
                </div>

                <div class="card">
                    <p class="section-label">Expertises</p>
                    <p class="text-2xl font-semibold text-stone-900 font-mono">
                    {detail.expertises.length}
                    </p>
                </div>

            </div>

            <!-- <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">

                <div class="card">
                    <p class="section-label">Expertises</p>
                    <p class="text-2xl font-semibold text-stone-900 font-mono">
                    {detail.expertises.length}
                    </p>
                </div>

                <div class="card">
                    <p class="section-label">Entities</p>
                    <p class="text-2xl font-semibold text-stone-900 font-mono">
                    {detail.entity_count}
                    </p>
                </div>

                <div class="card sm:col-span-1">
                    <p class="section-label mb-2">Domains</p>
                    <Taglist items={detail.domains} maxVisible={3} />
                </div>

                <div class="card">
                    <p class="section-label mb-2">Subdomains</p>
                    <Taglist items={detail.subdomains} maxVisible={3} />
                </div>

            </div> -->

            {#if detail.expertises.length > 0}
                <ExpertiseGrid
                    expertises={detail.expertises}
                    domains={detail.domains}
                    subdomains={detail.subdomains}
                    labs={detail.labs}
                />
            {/if}

        </section>

        <hr class="border-stone-100" />

        <!-- ── B: Taxonomy Visualisation ──────────────────────────────────────  -->
        <VisPanel
            title="Taxonomy Visualisation"
            description="Interactive graph showing the Domain → SubDomain hierarchy for this expertise map."
            onGenerate={() => visTaxonomy(params.id)}
        />

        <!-- ── C: Summary Statistics ────────────────────────────────────────── -->
        <VisPanel
            title="Summary Statistics"
            description="Bar charts showing distribution of articles and expertises across labs, domains, and subdomains."
            onGenerate={() => visSummary(params.id)}
        />

        <hr class="border-stone-100" />

        <!-- ── D: Expertises Visualisation ──────────────────────────────────── -->

        <ExpertisesVisPanel
            domains={detail.domains}
            subdomains={detail.subdomains}
            labs={detail.labs}
            title="Expertises Visualisation"
            description="Interactive graph showing all Expertise communities linked to their Subdomains and Domains."
            graphId={params.id}
        />

        <!-- ── E: Community Visualisation Form ───────────────────────────────  -->
        <CommunityVisPanel graphId={params.id} />

    </main>
{/if}
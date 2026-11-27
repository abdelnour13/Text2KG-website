<script lang="ts">

    import ExpertisePicker from './expertise-picker.svelte';
    import VisualisationFrame from './ui/visualisation-frame.svelte';
    import { visExpertiseDetail } from '$lib/services/api';
    import { expertiseName } from '$lib/expertise';
    import { i18n } from '$lib/i18n/index.svelte';

    interface ExpertiseDetailPanelProps {
        graphId: string;
        expertises: App.Expertise[];
        /** ID of the expertise to show; can be set from the expertise list. */
        selectedId: string | null;
        onSelect: (id: string) => void;
    }

    let { graphId, expertises, selectedId, onSelect }: ExpertiseDetailPanelProps = $props();

    let selected = $derived(expertises.find((e) => e.id === selectedId) ?? null);

    let vis: App.VisualisationResponse | null = $state(null);
    let error: string | null = $state(null);
    let loading = $state(false);
    let shownId: string | null = null;
    let requestNo = 0;

    async function generate(id: string) {
        const n = ++requestNo;
        shownId = id;
        error = null;
        loading = true;
        try {
            const res = await visExpertiseDetail(graphId, id);
            if (n === requestNo) vis = res;
        } catch (err) {
            if (n === requestNo) error = err instanceof Error ? err.message : 'Unknown error';
        } finally {
            if (n === requestNo) loading = false;
        }
    }

    // Build the graph whenever a different expertise is chosen.
    $effect(() => {
        if (selectedId && selectedId !== shownId) generate(selectedId);
    });

    let t = $derived(i18n.t.map.detail);

</script>

<section class="space-y-6">
    <div class="max-w-2xl">
        <h2 class="text-2xl font-semibold tracking-[-0.015em] text-ink sm:text-3xl">{t.title}</h2>
        <p class="mt-2 text-lg leading-relaxed text-ink-soft">{t.description}</p>
    </div>

    <ExpertisePicker {expertises} {selected} onSelect={(ex) => onSelect(ex.id)} />

    <VisualisationFrame
        title={selected ? expertiseName(selected) : ''}
        url={vis?.url ?? null}
        {loading}
        {error}
        onRetry={() => selectedId && generate(selectedId)}
        empty={!selected}
        emptyText={t.empty}
    />
</section>

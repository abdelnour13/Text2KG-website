<script lang="ts">
    import { i18n } from '$lib/i18n/index.svelte';
    // Decorative illustration of an expertise map: four groups of
    // expertises, each a hub with member nodes, linked by a few cross-domain edges.
    // Layout is generated from a fixed seed so it is identical on every render.

    interface Cluster {
        label: string;
        color: string;
        cx: number;
        cy: number;
        count: number;
        spread: number;
        labelDx: number;
        labelDy: number;
        anchor: 'start' | 'middle' | 'end';
    }

    const CLUSTERS: Cluster[] = [
        { label: 'Knowledge graphs',      color: 'var(--color-cluster-blue)',  cx: 190, cy: 150, count: 12, spread: 118, labelDx: 0, labelDy: -26, anchor: 'middle' },
        { label: 'Language models',       color: 'var(--color-cluster-teal)',  cx: 440, cy: 110, count: 8,  spread: 92,  labelDx: 0, labelDy: -26, anchor: 'middle' },
        { label: 'Data management',       color: 'var(--color-cluster-amber)', cx: 135, cy: 370, count: 9,  spread: 100, labelDx: 0, labelDy: 40,  anchor: 'middle' },
        { label: 'Information retrieval', color: 'var(--color-cluster-plum)',  cx: 415, cy: 345, count: 10, spread: 108, labelDx: 0, labelDy: 40,  anchor: 'middle' },
    ];

    // Small deterministic PRNG (mulberry32).
    function rng(seed: number) {
        return () => {
            seed |= 0; seed = (seed + 0x6d2b79f5) | 0;
            let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
            t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
            return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
        };
    }

    type Node = { x: number; y: number; r: number; c: number };
    type Edge = { a: Node; b: Node; cross: boolean };

    const rand = rng(7);
    const hubs: Node[] = CLUSTERS.map((cl, c) => ({ x: cl.cx, y: cl.cy, r: 9, c }));
    const members: Node[][] = CLUSTERS.map((cl, c) =>
        Array.from({ length: cl.count }, (_, i) => {
            const angle = (i / cl.count) * Math.PI * 2 + rand() * 0.5;
            const dist = cl.spread * (0.6 + rand() * 0.4);
            return { x: cl.cx + Math.cos(angle) * dist, y: cl.cy + Math.sin(angle) * dist * 0.85, r: 4.5 + rand() * 4.5, c };
        })
    );

    const edges: Edge[] = [];
    members.forEach((group, c) => {
        group.forEach((m, i) => {
            edges.push({ a: hubs[c], b: m, cross: false });
            if (rand() < 0.45) edges.push({ a: m, b: group[(i + 1) % group.length], cross: false });
        });
    });
    // A few links between groups: shared entities across domains.
    const CROSS: [number, number, number, number][] = [
        [0, 2, 1, 4], [0, 5, 2, 1], [0, 8, 3, 6], [1, 6, 3, 1], [2, 3, 3, 7],
    ];
    CROSS.forEach(([c1, i1, c2, i2]) => edges.push({ a: members[c1][i1], b: members[c2][i2], cross: true }));

</script>

<svg viewBox="0 0 560 480" class="h-auto w-full" role="img" aria-label={i18n.t.home.graphAria}>
    <g class="edges">
        {#each edges as e}
            <line
                x1={e.a.x} y1={e.a.y} x2={e.b.x} y2={e.b.y}
                stroke={e.cross ? 'var(--color-ink-faint)' : CLUSTERS[e.a.c].color}
                stroke-opacity={e.cross ? 0.35 : 0.3}
                stroke-width={e.cross ? 1.25 : 1.5}
                stroke-dasharray={e.cross ? '3 4' : undefined}
            />
        {/each}
    </g>

    {#each CLUSTERS as cl, c}
        <g class="cluster" style="--delay: {c * 140}ms; transform-origin: {cl.cx}px {cl.cy}px">
            {#each members[c] as m}
                <circle cx={m.x} cy={m.y} r={m.r} fill={cl.color} fill-opacity="0.85" />
            {/each}
            <circle cx={cl.cx} cy={cl.cy} r="22" fill={cl.color} fill-opacity="0.14" />
            <circle cx={cl.cx} cy={cl.cy} r="12" fill={cl.color} stroke="white" stroke-width="3" />
            <text
                x={cl.cx + cl.labelDx}
                y={cl.cy + cl.labelDy}
                text-anchor={cl.anchor}
                class="label"
            >{i18n.t.home.graphLabels[c]}</text>
        </g>
    {/each}
</svg>

<style>
    .label {
        font-family: var(--font-sans);
        font-size: 18px;
        font-weight: 600;
        fill: var(--color-ink);
        paint-order: stroke;
        stroke: var(--color-paper);
        stroke-width: 6px;
        stroke-linejoin: round;
    }

    .edges {
        animation: appear 900ms ease-out 300ms both;
    }

    .cluster {
        animation: grow 700ms cubic-bezier(0.2, 0.8, 0.2, 1) var(--delay) both;
    }

    @keyframes appear {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes grow {
        from { opacity: 0; transform: scale(0.6); }
        to { opacity: 1; transform: scale(1); }
    }

    @media (prefers-reduced-motion: reduce) {
        .edges, .cluster { animation: none; }
    }
</style>

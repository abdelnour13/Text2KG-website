<script lang="ts" >

    import DownloadIcon from '$lib/assets/download.svg';
    import OpenIcon from '$lib/assets/open.svg';
    import { downloadURL } from '$lib/services/api';
    import { error } from '@sveltejs/kit';

    interface VisualisationFrameProps {
        filename: string;
        url: string;
        title: string;
    }

    let { filename, url, title } : VisualisationFrameProps = $props();

    const openInNewTab = () => {
        const a    = document.createElement('a')
        a.href     = url;
        a.target   = '_blank';
        a.click();
    }

    const download = async () => {
        
        try {

            const res = await fetch(downloadURL(filename));

            if (!res.ok) {
                throw new Error(`Server error: ${res.status}`);
            }

            const blob = await res.blob();
            const url = URL.createObjectURL(blob);

            const a = document.createElement('a');
            a.href = url;
            a.download = filename;

            a.click();
            URL.revokeObjectURL(url);

        } catch (err) {
            alert(`failed to download file ${filename} : file doesn't exist.`)
        }

    }

</script>

<div class="space-y-2">
    <div class="flex items-center justify-between">
    <p class="text-xs text-stone-400 font-mono truncate max-w-xs">{filename}</p>
    <div>
        <button onclick={download} class="btn-ghost text-xs">
            <img src={DownloadIcon} alt="" />
            Download
        </button>
        <button onclick={openInNewTab} class="btn-ghost text-xs">
            <img src={OpenIcon} alt="" />
            Open in new tab
        </button>
    </div>
    </div>
    <div class="rounded border border-stone-200 overflow-hidden bg-white">
    <iframe
        src={url}
        title={title}
        class="w-full h-130 border-[none]"
        sandbox="allow-scripts allow-same-origin"
    ></iframe>
    </div>
</div>
import type { LayoutLoad } from './$types';

export const load: LayoutLoad = async ({ fetch }) => {
    return await fetch('/data.json').then((res) => res.json()) as Promise<App.ContactInfo>
};
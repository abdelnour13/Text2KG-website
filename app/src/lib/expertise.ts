// Helpers shared by the expertise list, table and picker.

/** Display name of an expertise: the generated label, falling back to its raw name or ID. */
export function expertiseName(ex: App.Expertise): string {
	return (ex.llm_label || ex.name || ex.id).trim();
}

/** Short ID of an expertise within its map (the part after the map ID). */
export function shortId(ex: App.Expertise, graphId: string): string {
	return ex.id.startsWith(graphId + '_') ? ex.id.slice(graphId.length + 1) : ex.id;
}

/** Lower-cases and strips accents so "Modèle" matches "modele". */
export function normalize(text: string): string {
	return text.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
}

/**
 * Splits `text` around the first case- and accent-insensitive match of `query`,
 * so the match can be highlighted. Works because NFD-stripping keeps one
 * character per original precomposed character for Latin text.
 */
export function splitMatch(text: string, query: string): [string, string, string] {
	const q = normalize(query.trim());
	if (!q) return [text, '', ''];
	const plain = normalize(text);
	const i = plain.indexOf(q);
	if (i < 0 || plain.length !== text.length) return [text, '', ''];
	return [text.slice(0, i), text.slice(i, i + q.length), text.slice(i + q.length)];
}

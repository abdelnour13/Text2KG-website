// Site-wide language state.
//
// Usage in components:  import { i18n } from '$lib/i18n/index.svelte';
//                       {i18n.t.nav.home}   {i18n.num(1234)}
// Everything that reads i18n.t updates as soon as the language changes.

import { en, type Dict } from './en';
import { fr } from './fr';

export type Locale = 'en' | 'fr';

export const LOCALES: Locale[] = ['fr', 'en'];

const DICTS: Record<Locale, Dict> = { en, fr };
const STORAGE_KEY = 'expertise-map:locale';

/** Saved choice first, then the browser's language, then English. */
function initialLocale(): Locale {
	if (typeof window === 'undefined') return 'en';
	try {
		const saved = localStorage.getItem(STORAGE_KEY);
		if (saved === 'en' || saved === 'fr') return saved;
	} catch {
		/* storage unavailable */
	}
	return navigator.language?.toLowerCase().startsWith('fr') ? 'fr' : 'en';
}

class I18n {
	locale = $state<Locale>(initialLocale());

	get t(): Dict {
		return DICTS[this.locale];
	}

	/** BCP 47 tag used for number formatting and sorting. */
	get tag(): string {
		return this.locale === 'fr' ? 'fr-FR' : 'en-GB';
	}

	set(locale: Locale) {
		this.locale = locale;
		try {
			localStorage.setItem(STORAGE_KEY, locale);
		} catch {
			/* storage unavailable */
		}
	}

	num = (n: number) => n.toLocaleString(this.tag);

	/** Locale-aware, case-insensitive string comparison for sorting. */
	compare = (a: string, b: string) => a.localeCompare(b, this.locale, { sensitivity: 'base' });
}

export const i18n = new I18n();

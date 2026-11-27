// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces
declare global {
	namespace App {
		
		interface ContactInfo {
			email: string;
			phone: string;
			address: string;
			lab: string;
		};

		// ── Graph list ────────────────────────────────────────────────────────────────

		interface GraphSummary {
			id: string
			name: string
			description: string
			number_of_expertises: number
			labs: string[]
			domains: string[]
			subdomains: string[]
		}

		// ── Graph detail ──────────────────────────────────────────────────────────────

		interface Domain {
			id: string
			name: string
		}

		interface SubDomain {
			id: string
			name: string
			domain: string
		}

		interface Expertise {
			id: string
			name: string
			llm_label: string
			size: number
			labs: string[]
			domains: string[]
			subdomains: string[]
		}

		interface GraphDetail {
			id: string
			description: string
			labs: string[]
			domains: string[]
			subdomains: string[]
			expertises: Expertise[]
			entity_count: number
		}

		// ── Visualisation ─────────────────────────────────────────────────────────────

		export interface VisualisationResponse {
			url: string
			filename: string
		}

		// ── API error ─────────────────────────────────────────────────────────────────

		export interface ApiError {
			detail: string
		}


	}
}

export {};

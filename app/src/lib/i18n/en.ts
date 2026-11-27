// English strings. The French file (fr.ts) must have exactly the same shape:
// TypeScript reports any key that is missing or extra there.

const num = (n: number) => n.toLocaleString('en-GB');
const plural = (n: number, one: string, many: string) => (n === 1 ? one : many);

export const en = {
	siteName: 'Expertise Map',
	titleSuffix: ' | Expertise Map',
	serverReturned: 'The server returned:',
	tryAgain: 'Try again',

	language: {
		label: 'Language',
		switchTo: 'Lire le site en français',
		short: { en: 'EN', fr: 'FR' }
	},

	nav: {
		home: 'Home',
		maps: 'Expertise maps',
		about: 'About',
		contact: 'Contact',
		homeAria: 'Expertise Map, home',
		mainAria: 'Main',
		openMenu: 'Open menu',
		closeMenu: 'Close menu'
	},

	footer: {
		tagline: 'Research expertise drawn from scientific publications and organised as an explorable knowledge graph.',
		contact: 'Contact',
		pages: 'Pages',
		footerAria: 'Footer',
		links: { home: 'Home', maps: 'Expertise maps', about: 'About the project', contact: 'Contact' }
	},

	home: {
		metaTitle: 'Expertise Map: research expertise as a knowledge graph',
		metaDescription: 'Explore the research expertise of Nantes Université labs, extracted from scientific publications and organised as an interactive knowledge graph.',
		heroTitle: 'See what your institution’s researchers know, mapped as a graph',
		heroText: 'Expertise Map reads scientific publications, finds the topics each team works on, and groups them into expertises you can explore by domain, subdomain and lab.',
		browseMaps: 'Browse expertise maps',
		howBuilt: 'How a map is built',
		stats: { maps: 'Maps', expertises: 'Expertises', labs: 'Labs covered' },
		graphAria: 'Illustration of an expertise map: areas of research expertise linked together',
		graphLabels: ['Knowledge graphs', 'Language models', 'Data management', 'Information retrieval'],
		stepsTitle: 'How a map is built',
		stepsIntro: 'From a stack of papers to a map you can navigate, in four steps.',
		steps: [
			{ title: 'Collect publications', text: 'Each map starts from a corpus of scientific publications written in the institution’s labs.' },
			{ title: 'Extract what papers talk about', text: 'Language models pick out the concepts, methods and entities in every paper, and how they relate.' },
			{ title: 'Group into expertises', text: 'Related entities are grouped together. Each group is one expertise, sized by how much work it covers.' },
			{ title: 'Place in the taxonomy', text: 'Every expertise is filed under a domain and subdomain, and linked to the labs that work on it.' }
		],
		featuresTitle: 'What you can do with a map',
		featuresIntro: 'For researchers looking for collaborators, labs reviewing their strengths, and partners looking for the right team.',
		features: [
			{ title: 'Explore the graph', text: 'See every expertise as an interactive network and follow how its topics connect to the rest of the map.' },
			{ title: 'Filter by domain, subdomain or lab', text: 'Narrow a map down to one field or one team to see who works on what.' },
			{ title: 'Look at one expertise in detail', text: 'Pick any expertise by name to see the entities it contains and how it links to its subdomains and domains.' }
		],
		ctaTitle: 'Start with a map',
		ctaText: 'Pick an expertise map, then filter it down to the domain or lab you care about.'
	},

	about: {
		metaTitle: 'About the project',
		metaDescription: 'Expertise Map is a research project at Nantes Université that turns scientific publications into an explorable knowledge graph of research expertise.',
		title: 'About the project',
		lead: 'Expertise Map makes the structure of scientific knowledge in an institution visible, so anyone can see who works on what and how fields connect.',
		whatTitle: 'What it is',
		paragraphs: [
			'Expertise Map is a research initiative that structures and visualises the scientific knowledge produced within academic institutions.',
			'Scientific publications are processed with a knowledge graph approach: entities, concepts and the relations between them are extracted from each paper. These are then grouped into expertises, each linked to thematic subdomains and broader research domains.',
			'The result is a map of the institution’s expertise that you can browse, filter by domain or lab, and explore as interactive graphs.'
		],
		howLink: 'See how a map is built, step by step',
		detailsTitle: 'Project details',
		facts: [
			{ label: 'Institution', value: 'Nantes Université' },
			{ label: 'Laboratory', value: 'LS2N, DUKe team' },
			{ label: 'Data source', value: 'Scientific publication corpus' },
			{ label: 'Graph backend', value: 'Neo4j' },
			{ label: 'Status', value: 'Active research project' }
		],
		audienceTitle: 'Who it’s for',
		audiences: [
			{ who: 'Researchers', why: 'Find colleagues working on related topics, inside or outside their own lab.' },
			{ who: 'Research administrators', why: 'See where the institution’s expertise lies and how it is distributed across labs.' },
			{ who: 'Industry partners', why: 'Identify the team with the right expertise for a collaboration.' },
			{ who: 'Funding agencies', why: 'Understand how research clusters and connects across disciplines.' }
		],
		ctaTitle: 'Questions about the project?',
		ctaText: 'Get in touch about the data, the method or a collaboration.',
		ctaContact: 'Contact the team',
		ctaMaps: 'Browse expertise maps'
	},

	contact: {
		metaTitle: 'Contact',
		metaDescription: 'Contact the Expertise Map team at LS2N, Nantes Université.',
		title: 'Contact',
		lead: 'Questions about the project, access to the data, or an idea for a collaboration? Email is the fastest way to reach the team.',
		email: 'Email',
		writeEmail: 'Write an email',
		copy: 'Copy address',
		copied: 'Copied',
		copiedAnnouncement: 'Email address copied',
		phone: 'Phone',
		address: 'Address',
		openMap: 'Open in a map',
		team: 'Research team'
	},

	maps: {
		metaTitle: 'Expertise maps',
		metaDescription: 'Browse the expertise maps built from Nantes Université scientific publications.',
		title: 'Expertise maps',
		lead: 'Each map is built from a corpus of publications. Open one to explore its expertises by domain, subdomain and lab.',
		searchLabel: 'Search maps',
		searchPlaceholder: 'Search by name, lab or domain',
		loading: 'Loading expertise maps',
		errorTitle: 'The expertise maps couldn’t be loaded',
		errorHint: 'Check your connection and try again.',
		emptyTitle: 'No expertise maps yet',
		emptyText: 'Maps appear here once a publication corpus has been processed.',
		count: (n: number) => `${num(n)} ${plural(n, 'map', 'maps')}`,
		matchCount: (shown: number, total: number, q: string) =>
			`${num(shown)} of ${num(total)} ${plural(total, 'map', 'maps')} match “${q}”`,
		noMatchTitle: (q: string) => `No maps match “${q}”`,
		noMatchText: 'Try a lab name, a domain, or fewer words.',
		clearSearch: 'Clear search',
		showMore: (n: number) => `Show ${num(n)} more ${plural(n, 'map', 'maps')}`,
		showFewer: 'Show fewer maps',
		card: {
			noDescription: 'No description yet.',
			expertises: (n: number) => plural(n, 'expertise', 'expertises'),
			domains: (n: number) => plural(n, 'domain', 'domains'),
			labs: (n: number) => plural(n, 'lab', 'labs'),
			open: 'Open map'
		}
	},

	map: {
		loading: 'Loading the expertise map',
		errorTitle: 'This expertise map couldn’t be loaded',
		noData: 'no data',
		allMaps: 'See all maps',
		figures: { expertises: 'Expertises', domains: 'Domains', subdomains: 'Subdomains', labs: 'Labs' },
		tabsAria: 'Ways to explore this map',
		tabs: {
			list: 'Expertise list',
			hierarchy: 'Domain hierarchy',
			charts: 'Statistics',
			network: 'Expertise network',
			detail: 'Expertise details'
		},
		hierarchy: {
			title: 'How domains break down into subdomains',
			description: 'An interactive graph of this map’s domains and the subdomains under each one.'
		},
		charts: {
			title: 'Articles and expertises in numbers',
			description: 'Bar charts of how articles and expertises are spread across labs, domains and subdomains.'
		},
		network: {
			title: 'How expertises connect',
			description: 'A network of expertises linked to their subdomains and domains. Narrow it down with the filters, then show the network.',
			show: 'Show network',
			update: 'Update network',
			empty: 'Pick filters if you want a smaller network, then select Show network. With no filters, every expertise in the map is included.'
		},
		detail: {
			title: 'Look at one expertise in detail',
			description: 'Choose an expertise to see the entities it contains and how it connects to its subdomains and domains.',
			empty: 'Open the list above and choose an expertise, or start typing part of its name.'
		}
	},

	browser: {
		title: 'All expertises in this map',
		description: 'Search by name, filter by domain, subdomain or lab, and switch between cards and a detailed table.',
		searchLabel: 'Search expertises by name',
		searchPlaceholder: 'Search expertises by name',
		sort: 'Sort',
		sorts: { nameAsc: 'Name, A to Z', nameDesc: 'Name, Z to A', sizeDesc: 'Largest first', sizeAsc: 'Smallest first' },
		displayAs: 'Display as',
		cards: 'Cards',
		table: 'Table',
		none: 'No expertises',
		showing: (from: number, to: number, total: number) =>
			`Showing ${num(from)}–${num(to)} of ${num(total)} ${plural(total, 'expertise', 'expertises')}`,
		outOf: (total: number) => ` (out of ${num(total)})`,
		noMatchTitle: 'No expertises match',
		noMatchText: 'Try another name, or remove some filters.',
		andMore: (n: number) => `and ${num(n)} more`,
		cardLabel: 'Expertise',
		viewGraph: 'View graph',
		viewGraphAria: (name: string) => `View the graph of ${name}`,
		columns: { name: 'Expertise', domain: 'Domain', subdomains: 'Subdomains', labs: 'Labs', entities: 'Entities', id: 'ID', actions: 'Actions' },
		pagesAria: 'Pages',
		previous: 'Previous',
		next: 'Next',
		pageOf: (p: number, total: number) => `Page ${num(p)} of ${num(total)}`
	},

	filters: {
		filterBy: 'Filter by',
		domain: 'Domain',
		subdomain: 'Subdomain',
		labs: 'Labs',
		clear: (n: number) => `Clear ${num(n)} ${plural(n, 'filter', 'filters')}`,
		showAll: (n: number) => `Show all ${num(n)}`,
		showFewer: 'Show fewer'
	},

	picker: {
		label: 'Expertise',
		placeholder: 'Type or pick an expertise name',
		clear: 'Clear',
		showAll: 'Show all expertises',
		hide: 'Hide the list',
		listAria: 'Expertises',
		total: (n: number) => `${num(n)} ${plural(n, 'expertise', 'expertises')}`,
		matching: (shown: number, total: number, q: string) =>
			`${num(shown)} of ${num(total)} ${plural(total, 'expertise', 'expertises')} contain “${q}”`,
		none: (q: string) => `No expertise name contains “${q}”.`,
		entities: (n: number) => `${num(n)} ${plural(n, 'entity', 'entities')}`
	},

	vis: {
		refresh: 'Refresh',
		building: 'Building the visualisation. This can take a few seconds.',
		errorTitle: 'The visualisation couldn’t be built',
		openFull: 'Open full screen'
	},

	error: {
		notFoundMeta: 'Page not found',
		otherMeta: 'Something went wrong',
		notFoundTitle: 'This page doesn’t exist',
		otherTitle: 'Something went wrong',
		notFoundText: 'The address may be mistyped, or the page may have moved.',
		otherText: (detail: string) =>
			`The page couldn’t be displayed${detail ? `: ${detail}` : '.'} If it keeps happening, let the team know.`,
		home: 'Go to the home page',
		maps: 'Browse expertise maps',
		contact: 'Contact the team'
	}
};

export type Dict = typeof en;
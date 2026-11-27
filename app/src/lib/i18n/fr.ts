import type { Dict } from './en';

// French strings. Uses a narrow no-break space ( ) before ? ! : ; as in
// French typography, and French number formatting (1 234).

const num = (n: number) => n.toLocaleString('fr-FR');
// In French, 0 and 1 take the singular.
const plural = (n: number, one: string, many: string) => (n < 2 ? one : many);
const nb = ' ';

export const fr: Dict = {
	siteName: 'Expertise Map',
	titleSuffix: ' | Expertise Map',
	serverReturned: `Le serveur a répondu${nb}:`,
	tryAgain: 'Réessayer',

	language: {
		label: 'Langue',
		switchTo: 'Read the site in English',
		short: { en: 'EN', fr: 'FR' }
	},

	nav: {
		home: 'Accueil',
		maps: 'Cartes d’expertise',
		about: 'À propos',
		contact: 'Contact',
		homeAria: 'Expertise Map, accueil',
		mainAria: 'Navigation principale',
		openMenu: 'Ouvrir le menu',
		closeMenu: 'Fermer le menu'
	},

	footer: {
		tagline: 'Les expertises de recherche extraites des publications scientifiques et organisées en un graphe de connaissances à explorer.',
		contact: 'Contact',
		pages: 'Pages',
		footerAria: 'Pied de page',
		links: { home: 'Accueil', maps: 'Cartes d’expertise', about: 'À propos du projet', contact: 'Contact' }
	},

	home: {
		metaTitle: 'Expertise Map : les expertises de recherche en graphe de connaissances',
		metaDescription: 'Explorez les expertises de recherche des laboratoires de Nantes Université, extraites des publications scientifiques et organisées en un graphe de connaissances interactif.',
		heroTitle: 'Découvrez les savoirs de vos chercheurs, cartographiés en graphe',
		heroText: 'Expertise Map analyse les publications scientifiques, repère les thèmes sur lesquels travaille chaque équipe et les regroupe en expertises à explorer par domaine, sous-domaine et laboratoire.',
		browseMaps: 'Parcourir les cartes d’expertise',
		howBuilt: 'Comment une carte est construite',
		stats: { maps: 'Cartes', expertises: 'Expertises', labs: 'Laboratoires' },
		graphAria: 'Illustration d’une carte d’expertise : des domaines d’expertise de recherche reliés entre eux',
		graphLabels: ['Graphes de connaissances', 'Modèles de langage', 'Gestion des données', 'Recherche d’information'],
		stepsTitle: 'Comment une carte est construite',
		stepsIntro: 'D’un ensemble d’articles à une carte navigable, en quatre étapes.',
		steps: [
			{ title: 'Rassembler les publications', text: 'Chaque carte part d’un corpus de publications scientifiques rédigées dans les laboratoires de l’établissement.' },
			{ title: 'Extraire le contenu des articles', text: 'Des modèles de langage repèrent les concepts, méthodes et entités de chaque article, ainsi que leurs relations.' },
			{ title: 'Regrouper en expertises', text: 'Les entités liées sont regroupées. Chaque groupe forme une expertise, dont la taille reflète le volume de travaux couverts.' },
			{ title: 'Classer dans la taxonomie', text: 'Chaque expertise est rattachée à un domaine et à un sous-domaine, et reliée aux laboratoires qui y travaillent.' }
		],
		featuresTitle: 'Ce que vous pouvez faire avec une carte',
		featuresIntro: 'Pour les chercheurs en quête de collaborateurs, les laboratoires qui font le point sur leurs forces et les partenaires qui cherchent la bonne équipe.',
		features: [
			{ title: 'Explorer le graphe', text: 'Affichez toutes les expertises sous forme de réseau interactif et suivez les liens entre leurs thèmes et le reste de la carte.' },
			{ title: 'Filtrer par domaine, sous-domaine ou laboratoire', text: 'Réduisez une carte à un seul domaine ou à une seule équipe pour voir qui travaille sur quoi.' },
			{ title: 'Examiner une expertise en détail', text: 'Choisissez une expertise par son nom pour voir les entités qu’elle contient et ses liens avec ses sous-domaines et domaines.' }
		],
		ctaTitle: 'Commencez par une carte',
		ctaText: 'Choisissez une carte d’expertise, puis filtrez-la selon le domaine ou le laboratoire qui vous intéresse.'
	},

	about: {
		metaTitle: 'À propos du projet',
		metaDescription: 'Expertise Map est un projet de recherche de Nantes Université qui transforme les publications scientifiques en un graphe de connaissances des expertises de recherche.',
		title: 'À propos du projet',
		lead: 'Expertise Map rend visible la structure des savoirs scientifiques d’un établissement, pour que chacun puisse voir qui travaille sur quoi et comment les disciplines se rejoignent.',
		whatTitle: 'Le projet',
		paragraphs: [
			'Expertise Map est une initiative de recherche qui structure et visualise les connaissances scientifiques produites au sein des établissements universitaires.',
			'Les publications scientifiques sont traitées selon une approche par graphe de connaissances : les entités, les concepts et leurs relations sont extraits de chaque article. Ils sont ensuite regroupés en expertises, chacune reliée à des sous-domaines thématiques et à des domaines de recherche plus larges.',
			'Le résultat est une carte des expertises de l’établissement, que l’on peut parcourir, filtrer par domaine ou par laboratoire, et explorer sous forme de graphes interactifs.'
		],
		howLink: 'Voir comment une carte est construite, étape par étape',
		detailsTitle: 'Le projet en bref',
		facts: [
			{ label: 'Établissement', value: 'Nantes Université' },
			{ label: 'Laboratoire', value: 'LS2N, équipe DUKe' },
			{ label: 'Source des données', value: 'Corpus de publications scientifiques' },
			{ label: 'Base de graphes', value: 'Neo4j' },
			{ label: 'Statut', value: 'Projet de recherche en cours' }
		],
		audienceTitle: 'À qui s’adresse le projet',
		audiences: [
			{ who: 'Chercheurs', why: 'Trouver des collègues qui travaillent sur des sujets proches, dans leur laboratoire ou ailleurs.' },
			{ who: 'Responsables de la recherche', why: 'Voir où se situent les expertises de l’établissement et comment elles se répartissent entre laboratoires.' },
			{ who: 'Partenaires industriels', why: 'Identifier l’équipe qui a l’expertise adaptée à une collaboration.' },
			{ who: 'Organismes de financement', why: 'Comprendre comment la recherche se regroupe et se relie d’une discipline à l’autre.' }
		],
		ctaTitle: `Des questions sur le projet${nb}?`,
		ctaText: 'Contactez-nous au sujet des données, de la méthode ou d’une collaboration.',
		ctaContact: 'Contacter l’équipe',
		ctaMaps: 'Parcourir les cartes d’expertise'
	},

	contact: {
		metaTitle: 'Contact',
		metaDescription: 'Contactez l’équipe Expertise Map au LS2N, Nantes Université.',
		title: 'Contact',
		lead: `Une question sur le projet, un accès aux données ou une idée de collaboration${nb}? Le courriel est le moyen le plus rapide de joindre l’équipe.`,
		email: 'Courriel',
		writeEmail: 'Écrire un courriel',
		copy: 'Copier l’adresse',
		copied: 'Copiée',
		copiedAnnouncement: 'Adresse électronique copiée',
		phone: 'Téléphone',
		address: 'Adresse',
		openMap: 'Ouvrir dans une carte',
		team: 'Équipe de recherche'
	},

	maps: {
		metaTitle: 'Cartes d’expertise',
		metaDescription: 'Parcourez les cartes d’expertise construites à partir des publications scientifiques de Nantes Université.',
		title: 'Cartes d’expertise',
		lead: 'Chaque carte est construite à partir d’un corpus de publications. Ouvrez-en une pour explorer ses expertises par domaine, sous-domaine et laboratoire.',
		searchLabel: 'Rechercher une carte',
		searchPlaceholder: 'Nom, laboratoire ou domaine',
		loading: 'Chargement des cartes d’expertise',
		errorTitle: 'Impossible de charger les cartes d’expertise',
		errorHint: 'Vérifiez votre connexion et réessayez.',
		emptyTitle: 'Aucune carte d’expertise pour le moment',
		emptyText: 'Les cartes apparaissent ici une fois qu’un corpus de publications a été traité.',
		count: (n: number) => `${num(n)} ${plural(n, 'carte', 'cartes')}`,
		matchCount: (shown: number, total: number, q: string) =>
			`${num(shown)} ${plural(shown, 'carte correspond', 'cartes correspondent')} à « ${q} » sur ${num(total)}`,
		noMatchTitle: (q: string) => `Aucune carte ne correspond à « ${q} »`,
		noMatchText: 'Essayez un nom de laboratoire, un domaine ou moins de mots.',
		clearSearch: 'Effacer la recherche',
		showMore: (n: number) => `Afficher ${num(n)} ${plural(n, 'carte de plus', 'cartes de plus')}`,
		showFewer: 'Afficher moins de cartes',
		card: {
			noDescription: 'Pas encore de description.',
			expertises: (n: number) => plural(n, 'expertise', 'expertises'),
			domains: (n: number) => plural(n, 'domaine', 'domaines'),
			labs: (n: number) => plural(n, 'laboratoire', 'laboratoires'),
			open: 'Ouvrir la carte'
		}
	},

	map: {
		loading: 'Chargement de la carte d’expertise',
		errorTitle: 'Impossible de charger cette carte d’expertise',
		noData: 'aucune donnée',
		allMaps: 'Voir toutes les cartes',
		figures: { expertises: 'Expertises', domains: 'Domaines', subdomains: 'Sous-domaines', labs: 'Laboratoires' },
		tabsAria: 'Façons d’explorer cette carte',
		tabs: {
			list: 'Liste des expertises',
			hierarchy: 'Hiérarchie des domaines',
			charts: 'Statistiques',
			network: 'Réseau des expertises',
			detail: 'Détail d’une expertise'
		},
		hierarchy: {
			title: 'Comment les domaines se divisent en sous-domaines',
			description: 'Un graphe interactif des domaines de cette carte et des sous-domaines qui les composent.'
		},
		charts: {
			title: 'Les articles et les expertises en chiffres',
			description: 'Des graphiques en barres montrant la répartition des articles et des expertises par laboratoire, domaine et sous-domaine.'
		},
		network: {
			title: 'Comment les expertises sont reliées',
			description: 'Un réseau des expertises reliées à leurs sous-domaines et domaines. Affinez-le avec les filtres, puis affichez le réseau.',
			show: 'Afficher le réseau',
			update: 'Mettre à jour le réseau',
			empty: 'Choisissez des filtres pour obtenir un réseau plus petit, puis sélectionnez Afficher le réseau. Sans filtre, toutes les expertises de la carte sont incluses.'
		},
		detail: {
			title: 'Examiner une expertise en détail',
			description: 'Choisissez une expertise pour voir les entités qu’elle contient et ses liens avec ses sous-domaines et domaines.',
			empty: 'Ouvrez la liste ci-dessus et choisissez une expertise, ou commencez à taper une partie de son nom.'
		}
	},

	browser: {
		title: 'Toutes les expertises de cette carte',
		description: 'Recherchez par nom, filtrez par domaine, sous-domaine ou laboratoire, et passez de l’affichage en cartes à un tableau détaillé.',
		searchLabel: 'Rechercher une expertise par son nom',
		searchPlaceholder: 'Rechercher une expertise par son nom',
		sort: 'Trier',
		sorts: { nameAsc: 'Nom, de A à Z', nameDesc: 'Nom, de Z à A', sizeDesc: 'Les plus grandes d’abord', sizeAsc: 'Les plus petites d’abord' },
		displayAs: 'Afficher en',
		cards: 'Cartes',
		table: 'Tableau',
		none: 'Aucune expertise',
		showing: (from: number, to: number, total: number) =>
			`${num(from)} à ${num(to)} sur ${num(total)} ${plural(total, 'expertise', 'expertises')}`,
		outOf: (total: number) => ` (sur ${num(total)} au total)`,
		noMatchTitle: 'Aucune expertise ne correspond',
		noMatchText: 'Essayez un autre nom ou retirez certains filtres.',
		andMore: (n: number) => `et ${num(n)} de plus`,
		cardLabel: 'Expertise',
		viewGraph: 'Voir le graphe',
		viewGraphAria: (name: string) => `Voir le graphe de ${name}`,
		columns: { name: 'Expertise', domain: 'Domaine', subdomains: 'Sous-domaines', labs: 'Laboratoires', entities: 'Entités', id: 'ID', actions: 'Actions' },
		pagesAria: 'Pages',
		previous: 'Précédente',
		next: 'Suivante',
		pageOf: (p: number, total: number) => `Page ${num(p)} sur ${num(total)}`
	},

	filters: {
		filterBy: 'Filtrer par',
		domain: 'Domaine',
		subdomain: 'Sous-domaine',
		labs: 'Laboratoires',
		clear: (n: number) => `Effacer ${plural(n, 'le filtre', `les ${num(n)} filtres`)}`,
		showAll: (n: number) => `Tout afficher (${num(n)})`,
		showFewer: 'Afficher moins'
	},

	picker: {
		label: 'Expertise',
		placeholder: 'Tapez ou choisissez le nom d’une expertise',
		clear: 'Effacer',
		showAll: 'Afficher toutes les expertises',
		hide: 'Masquer la liste',
		listAria: 'Expertises',
		total: (n: number) => `${num(n)} ${plural(n, 'expertise', 'expertises')}`,
		matching: (shown: number, total: number, q: string) =>
			`${num(shown)} ${plural(shown, 'expertise contient', 'expertises contiennent')} « ${q} » sur ${num(total)}`,
		none: (q: string) => `Aucun nom d’expertise ne contient « ${q} ».`,
		entities: (n: number) => `${num(n)} ${plural(n, 'entité', 'entités')}`
	},

	vis: {
		refresh: 'Actualiser',
		building: 'Construction de la visualisation. Cela peut prendre quelques secondes.',
		errorTitle: 'Impossible de construire la visualisation',
		openFull: 'Ouvrir en plein écran'
	},

	error: {
		notFoundMeta: 'Page introuvable',
		otherMeta: 'Une erreur est survenue',
		notFoundTitle: 'Cette page n’existe pas',
		otherTitle: 'Une erreur est survenue',
		notFoundText: 'L’adresse est peut-être mal saisie, ou la page a été déplacée.',
		otherText: (detail: string) =>
			`La page n’a pas pu s’afficher${detail ? ` : ${detail}` : '.'} Si le problème persiste, prévenez l’équipe.`,
		home: 'Aller à l’accueil',
		maps: 'Parcourir les cartes d’expertise',
		contact: 'Contacter l’équipe'
	}
};
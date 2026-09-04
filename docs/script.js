const DEFAULT_LANG = 'en';

const LOCALE_PATHS = {
	en: 'locale/en/en.json',
	es: 'locale/es/es.json',
};

const translations = {};

async function loadTranslations(lang) {
	const requestedLang = LOCALE_PATHS[lang] ? lang : DEFAULT_LANG;

	if (translations[requestedLang]) {
		return { lang: requestedLang, values: translations[requestedLang] };
	}

	try {
		const res = await fetch(LOCALE_PATHS[requestedLang]);
		if (!res.ok) throw new Error(`${LOCALE_PATHS[requestedLang]} returned ${res.status}`);

		const values = await res.json();
		translations[requestedLang] = values;
		return { lang: requestedLang, values };
	} catch (error) {
		console.error(`Unable to load locale for ${requestedLang}`, error);

		if (requestedLang !== DEFAULT_LANG) {
			return loadTranslations(DEFAULT_LANG);
		}

		return { lang: DEFAULT_LANG, values: {} };
	}
}

async function applyTranslations(lang) {
	const { lang: activeLang, values: t } = await loadTranslations(lang);
	document.documentElement.lang = activeLang;
	localStorage.setItem('neo-lang', activeLang);

	document.querySelectorAll('[data-i18n]').forEach(el => {
		const key = el.getAttribute('data-i18n');
		if (!(key in t)) return;
		if (el.tagName === 'TITLE') {
			document.title = t[key];
		} else if (el.tagName === 'META') {
			el.setAttribute('content', t[key]);
		} else {
			el.innerHTML = t[key];
		}
	});

	const btn = document.getElementById('lang-toggle');
	if (btn) btn.textContent = activeLang === 'en' ? 'ES' : 'EN';

	await renderRoadmap(activeLang);
}

async function getCurrentReleaseVersion() {
	try {
		const response = await fetch('changelog.json');

		if (!response.ok) throw new Error('HTTP error ' + response.status);

		const jsonData = await response.json();

		const version = jsonData[0]?.version || 'N/A';

		if (!version) throw new Error('Version not found in changelog.json');

		const field = document.getElementById('hero-badge-release');

		if (field) {
			field.textContent = version;

		}
	}
	catch (error) {
		console.error('Error fetching changelog.json:', error);
	}
}


document.addEventListener('DOMContentLoaded', async () => {
	const saved = localStorage.getItem('neo-lang') || 'en';
	applyTranslations(saved);
	getCurrentReleaseVersion();

	const btn = document.getElementById('lang-toggle');
	if (btn) {
		btn.addEventListener('click', async () => {
			const current = localStorage.getItem('neo-lang') || DEFAULT_LANG;
			await applyTranslations(current === 'en' ? 'es' : 'en');
		});
	}

	document.querySelectorAll('.code-block, details.code-details').forEach(block => {
		const header = block.querySelector('.code-header') || block.querySelector('summary');
		const body = block.querySelector('.code-body');
		if (!header || !body) return;

		const copyBtn = document.createElement('button');
		copyBtn.className = 'copy-btn';
		copyBtn.textContent = 'copy';
		copyBtn.addEventListener('click', e => {
			e.preventDefault();
			navigator.clipboard.writeText(body.innerText.trim()).then(() => {
				copyBtn.textContent = 'copied!';
				copyBtn.classList.add('copied');
				setTimeout(() => {
					copyBtn.textContent = 'copy';
					copyBtn.classList.remove('copied');
				}, 1500);
			});
		});
		header.appendChild(copyBtn);
	});

	await Promise.all([
		updateHeroBadgeRelease(),
		loadChangelog(),
	]);
});

const ROADMAP_STATUS_CLASSES = {
	done: 'tag-done',
	planned: 'tag-planned',
	working: 'tag-working',
	idea: 'tag-idea',
};

const ROADMAP_REPO = '4DRIAN0RTIZ/NeoComposer';
const ROADMAP_API = `https://api.github.com/repos/${ROADMAP_REPO}/issues?labels=roadmap&state=all&per_page=100`;
const ROADMAP_CACHE_KEY = 'neo-roadmap-cache';
const ROADMAP_CACHE_TTL = 30 * 60 * 1000; // 30 min

const ROADMAP_STATUS_LABELS = [
	['roadmap:working', 'working'],
	['roadmap:planned', 'planned'],
	['roadmap:idea', 'idea'],
];
const ROADMAP_STATUS_ORDER = ['working', 'planned', 'idea', 'done'];
const ROADMAP_SECTION_TITLES = {
	working: { en: 'In progress', es: 'En progreso' },
	planned: { en: 'Planned', es: 'Planeado' },
	idea: { en: 'Ideas', es: 'Ideas' },
	done: { en: 'Done', es: 'Hecho' },
};
const ROADMAP_LABELS = {
	done: { en: '✓ done', es: '✓ hecho' },
	planned: { en: 'planned', es: 'planeado' },
	idea: { en: 'idea', es: 'idea' },
	working: { en: 'in progress', es: 'en progreso' },
};
const ROADMAP_DONE_WINDOW_DAYS = 60;

function roadmapLabelNames(issue) {
	return (issue.labels || []).map(l => (typeof l === 'string' ? l : l.name || ''));
}

function roadmapResolveStatus(issue) {
	if ((issue.state || '').toLowerCase() === 'closed') return 'done';
	const names = roadmapLabelNames(issue);
	for (const [label, status] of ROADMAP_STATUS_LABELS) {
		if (names.includes(label)) return status;
	}
	return 'planned';
}

function roadmapStripPrefix(title) {
	return (title || '').replace(/^\[roadmap\]\s*/i, '').trim();
}

function roadmapWithinDoneWindow(issue) {
	const when = Date.parse(issue.closed_at || issue.updated_at || '');
	if (Number.isNaN(when)) return false;
	return Date.now() - when <= ROADMAP_DONE_WINDOW_DAYS * 86400000;
}

function issuesToRoadmap(issues) {
	const milestoneGroups = new Map();
	const statusGroups = new Map();

	for (const issue of issues) {
		if (issue.pull_request) continue;
		if (!roadmapLabelNames(issue).includes('roadmap')) continue;

		const status = roadmapResolveStatus(issue);
		const milestone = issue.milestone && issue.milestone.title;

		if (status === 'done' && !milestone && !roadmapWithinDoneWindow(issue)) continue;

		const item = {
			status,
			text: roadmapStripPrefix(issue.title),
			ref: { label: `Issue #${issue.number}`, url: issue.html_url },
			_updatedAt: issue.updated_at || '',
		};

		if (milestone) {
			if (!milestoneGroups.has(milestone)) {
				milestoneGroups.set(milestone, {
					title: milestone,
					due: (issue.milestone && issue.milestone.due_on) || '9999-12-31T00:00:00Z',
					items: [],
				});
			}
			milestoneGroups.get(milestone).items.push(item);
		} else {
			if (!statusGroups.has(status)) statusGroups.set(status, []);
			statusGroups.get(status).push(item);
		}
	}

	const sortItems = items => items.sort((a, b) =>
		(ROADMAP_STATUS_ORDER.indexOf(a.status) - ROADMAP_STATUS_ORDER.indexOf(b.status)) ||
		String(b._updatedAt).localeCompare(String(a._updatedAt)));
	const strip = item => {
		const { _updatedAt, ...rest } = item;
		return rest;
	};

	const sections = [];
	[...milestoneGroups.values()]
		.sort((a, b) => a.due.localeCompare(b.due) || a.title.localeCompare(b.title))
		.forEach(group => sections.push({ title: group.title, items: sortItems(group.items).map(strip) }));

	for (const status of ROADMAP_STATUS_ORDER) {
		const items = statusGroups.get(status);
		if (!items || items.length === 0) continue;
		sections.push({ title: ROADMAP_SECTION_TITLES[status], items: sortItems(items).map(strip) });
	}

	return { labels: ROADMAP_LABELS, sections };
}

function readRoadmapCache() {
	try {
		const raw = localStorage.getItem(ROADMAP_CACHE_KEY);
		if (!raw) return null;
		const cached = JSON.parse(raw);
		if (Date.now() - cached.ts > ROADMAP_CACHE_TTL) return null;
		return cached.data;
	} catch (error) {
		return null;
	}
}

function writeRoadmapCache(data) {
	try {
		localStorage.setItem(ROADMAP_CACHE_KEY, JSON.stringify({ ts: Date.now(), data }));
	} catch (error) {
		/* storage unavailable or full — cache is best-effort */
	}
}

let roadmapData = null;

async function loadRoadmap() {
	if (roadmapData) return roadmapData;

	const cached = readRoadmapCache();
	if (cached) {
		roadmapData = cached;
		return roadmapData;
	}

	try {
		const res = await fetch(ROADMAP_API, { headers: { Accept: 'application/vnd.github+json' } });
		if (!res.ok) throw new Error(`GitHub issues API returned ${res.status}`);
		roadmapData = issuesToRoadmap(await res.json());
		writeRoadmapCache(roadmapData);
		return roadmapData;
	} catch (error) {
		console.warn('Roadmap: live fetch failed, falling back to roadmap.json', error);
		const res = await fetch('roadmap.json');
		if (!res.ok) throw new Error(`roadmap.json returned ${res.status}`);
		roadmapData = await res.json();
		return roadmapData;
	}
}

function localizedValue(value, lang) {
	if (typeof value === 'string') return value;
	return value?.[lang] || value?.[DEFAULT_LANG] || '';
}

async function renderRoadmap(lang) {
	const container = document.getElementById('roadmap-content');
	if (!container) return;

	try {
		const roadmap = await loadRoadmap();
		const sections = roadmap.sections || [];

		if (sections.length === 0) {
			renderRoadmapEmpty(container, lang);
			return;
		}

		container.innerHTML = sections.map((section, sectionIndex) => {
			const title = localizedValue(section.title, lang);
			const margin = sectionIndex === 0
				? 'margin-bottom: 1rem;'
				: 'margin-top: 2rem; margin-bottom: 1rem;';
			const items = (section.items || []).map(item => {
				const status = item.status || 'planned';
				const tagClass = ROADMAP_STATUS_CLASSES[status] || ROADMAP_STATUS_CLASSES.planned;
				const statusLabel = localizedValue(roadmap.labels?.[status], lang) || status;
				const text = localizedValue(item.text, lang);
				const ref = item.ref?.url && item.ref?.label
					? `<span class="roadmap-ref"><a href="${escapeHtml(item.ref.url)}" target="_blank" rel="noopener">${escapeHtml(item.ref.label)}</a></span>`
					: '';

				return `
					<div class="roadmap-item">
						<span class="tag ${tagClass}">${escapeHtml(statusLabel)}</span>
						<span>${escapeHtml(text)}</span>
						${ref}
					</div>`;
			}).join('');

			return `
				<h3 style="${margin}">${escapeHtml(title)}</h3>
				<div class="roadmap">${items}</div>`;
		}).join('');
	} catch (error) {
		console.error('Unable to load roadmap', error);
		renderRoadmapEmpty(container, lang);
	}
}

function renderRoadmapEmpty(container, lang) {
	const t = translations[lang] || translations[DEFAULT_LANG] || {};
	const message = t['roadmap-empty-msg'] || 'Roadmap unavailable.';
	container.innerHTML = `<p class="changelog-empty">${message}</p>`;
}

const CHANGELOG_REPO = 'https://github.com/4DRIAN0RTIZ/NeoComposer';

let changelogData = null;

async function loadChangelogData() {
	if (changelogData) return changelogData;

	const res = await fetch('changelog.json');
	if (!res.ok) throw new Error('changelog.json not found');

	changelogData = await res.json();
	return changelogData;
}

async function updateHeroBadgeRelease() {
	const field = document.getElementById('hero-badge-release');
	if (!field) return;

	try {
		const releases = await loadChangelogData();
		const version = releases?.[0]?.version || 'N/A';
		field.textContent = version;
	} catch (error) {
		console.error('Error fetching changelog.json:', error);
		field.textContent = 'N/A';
	}
}

const CHANGELOG_GROUP_TAGS = {
	Features: 'tag-feat',
	'Bug Fixes': 'tag-fix',
	Documentation: 'tag-docs',
	Refactor: 'tag-refactor',
	Performance: 'tag-feat',
};

function changelogTagClass(group) {
	return CHANGELOG_GROUP_TAGS[group] || 'tag-chore';
}

function escapeHtml(str) {
	const div = document.createElement('div');
	div.textContent = str;
	return div.innerHTML;
}

async function loadChangelog() {
	const container = document.getElementById('changelog-content');
	if (!container) return;

	try {
		const releases = await loadChangelogData();

		const withCommits = (releases || []).filter(r => (r.commits || []).length > 0);
		if (withCommits.length === 0) {
			renderChangelogEmpty(container);
			return;
		}

		const unreleased = withCommits.filter(r => !r.version);
		const latestTagged = withCommits.find(r => r.version);
		const visible = [...unreleased, ...(latestTagged ? [latestTagged] : [])];

		const latestTimestamp = visible[0]?.commits?.[0]?.author?.timestamp;
		const footerUpdated = document.getElementById('footer-updated');
		if (footerUpdated && latestTimestamp) {
			const lang = localStorage.getItem('neo-lang') || DEFAULT_LANG;
			const t = translations[lang] || translations[DEFAULT_LANG] || {};
			const label = t['changelog-updated'] || 'Last updated: ';
			const date = new Date(latestTimestamp * 1000).toISOString().slice(0, 10);
			footerUpdated.textContent = `${label}${date}`;
		}

		container.innerHTML = visible.map(release => {
			const version = release.version || 'Unreleased';
			const date = release.timestamp
				? new Date(release.timestamp * 1000).toISOString().slice(0, 10)
				: '';

			const entries = (release.commits || []).map(c => {
				const tagClass = changelogTagClass(c.group);
				const label = c.group || 'Other';
				const sha = (c.id || '').slice(0, 7);
				const url = c.id ? `${CHANGELOG_REPO}/commit/${c.id}` : null;
				return `
          <div class="changelog-entry">
            <span class="tag ${tagClass}">${escapeHtml(label)}</span>
            <span>${escapeHtml(c.message || '')}</span>
            ${url ? `<a href="${url}" target="_blank" rel="noopener">${sha}</a>` : ''}
          </div>`;
			}).join('');

			return `
        <div class="changelog-version">
          <h3>${escapeHtml(version)} ${date ? `<span class="changelog-date">— ${date}</span>` : ''}</h3>
          ${entries}
        </div>`;
		}).join('');
	} catch (e) {
		renderChangelogEmpty(container);
	}
}

function renderChangelogEmpty(container) {
	const lang = localStorage.getItem('neo-lang') || DEFAULT_LANG;
	const t = translations[lang] || translations[DEFAULT_LANG] || {};
	const message = t['changelog-empty-msg'] || 'No changelog entries yet — check back after the next release.';
	container.innerHTML = `<p class="changelog-empty">${message}</p>`;
}

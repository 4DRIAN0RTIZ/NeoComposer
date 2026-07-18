const translations = {
	en: {
		'page-title': 'NeoComposer — Email from the terminal',
		'page-description': 'Send emails from your terminal using Neovim as your editor. Programmatic CLI support, attachments via Yazi, contact agenda, HTML signature and SMTP.',
		'nav-install': 'Install',
		'nav-config': 'Config',
		'nav-usage': 'Usage',
		'nav-cli': 'CLI',
		'nav-agenda': 'Agenda',
		'nav-roadmap': 'Roadmap',
		'nav-changelog': 'Changelog',
		'nav-github': 'GitHub',
		'hero-badge': 'v1.1.0 — stable',
		'hero-title-line1': 'Email from the',
		'hero-title-accent': 'terminal',
		'hero-title-line3': 'as it should be.',
		'hero-subtitle': 'NeoComposer is a minimalist email client for the terminal with programmatic support. Write with Neovim, attach with Yazi, or automate with CLI.',
		'hero-btn-install': 'Install',
		'hero-btn-blog': 'Read blog',
		'features-label': '// features',
		'features-title': 'For the dev who lives in the terminal',
		'features-subtitle': 'NeoComposer integrates the tools you already use, without friction. Now with CLI support for automation.',
		'feat-evim-title': 'Neovim as editor',
		'feat-evim-desc': 'Write your email with the editor you already master. Shortcuts, macros, plugins — all available. The temp file is deleted after sending.',
		'feat-ranger-title': 'Attachments via Yazi',
		'feat-ranger-desc': 'Navigate your filesystem with Yazi to select attachments. No full paths needed. Attach multiple files.',
		'feat-agenda-title': 'Contact agenda',
		'feat-agenda-desc': 'Save frequent recipients in a JSON. Manage with -a flag or use indexes with --agenda-index for scripting.',
		'feat-signature-title': 'HTML Signature',
		'feat-signature-desc': 'Define a custom HTML signature with images, links, and styles. Automatically injected into every email.',
		'feat-smtp-title': 'SMTP + TLS',
		'feat-smtp-desc': 'Secure connection via STARTTLS. Compatible with Gmail, Outlook, and any standard SMTP provider.',
		'feat-cli-title': 'Programmatic mode',
		'feat-cli-desc': 'Integrate in scripts with --recipient, --subject, --body, --attachments. Automate notifications and reports.',
		'install-label': '// installation',
		'install-title': 'Ready in 3 steps',
		'install-subtitle': 'The installer detects your distro, installs dependencies, and sets up the shortcut.',
		'install-oneliner-label': 'quick install',
		'install-oneliner-note': 'The installer downloads files directly from GitHub. For manual installation, clone the repository and run the script locally.',
		'install-step1': 'Clone the repository',
		'install-step1-desc': 'Download NeoComposer from GitHub.',
		'install-step2': 'Run the installer',
		'install-step2-desc': 'The script detects Arch, Debian/Ubuntu or Fedora and handles the rest: system dependencies, Python dependencies, and the symlink.',
		'install-step2-note': 'Supported distros: Arch, Ubuntu/Debian/Mint/Kali, Fedora/CentOS/RHEL. The installer installs yazi, neovim, jq, and python3 if not present.',
		'install-step3': 'Configure your credentials',
		'install-step3-desc': 'Edit the .env file the installer copied to ~/.config/neocomposer/.env.',
		'config-label': '// configuration',
		'config-title': 'SMTP and Gmail',
		'config-subtitle': 'Instructions to connect NeoComposer with Gmail using an app password.',
		'config-warning': 'Gmail requires an app password, not your regular password. Enable two-step verification first, then go to Google Account → Security → App Passwords.',
		'config-step1': 'Enable IMAP in Gmail',
		'config-step1-desc': 'In Gmail → Settings → See all settings → Forwarding and POP/IMAP → Enable IMAP.',
		'config-step2': 'Generate app password',
		'config-step2-desc': 'Google Account → Security → App Passwords → Select "Other" → generate and copy the 16-character key.',
		'config-step3': 'Configure .env',
		'config-signature-title': 'HTML Signature (optional)',
		'config-signature-desc': 'Create <code>~/.config/NeoComposer/signature.html</code> with your signature. Automatically added to every email.',
		'usage-label': '// usage',
		'usage-title': 'Interactive workflow',
		'usage-subtitle': 'NeoComposer guides the process step by step.',
		'usage-cmd-header': 'Command',
		'usage-desc-header': 'Description',
		'usage-cmd1': 'Starts the email composer',
		'usage-cmd2': 'Opens contact agenda management',
		'usage-cmd-title': "Step by step when running 'neocomposer'",
		'usage-step1': 'Choose recipient',
		'usage-step1-desc': 'Enter a one-time email or select one from your agenda.',
		'usage-step2': 'Write the subject',
		'usage-step2-desc': 'Free text in the terminal.',
		'usage-step3': 'Compose in Neovim',
		'usage-step3-desc': 'A temporary buffer opens. Write with all the power of Neovim. Save and quit (:wq) to continue the flow.',
		'usage-step4': 'Optional attachments',
		'usage-step4-desc': 'If you confirm with Y, Yazi opens to browse and select files. You can attach multiple.',
		'usage-step5': 'Automatic sending',
		'usage-step5-desc': 'NeoComposer connects to SMTP, adds the HTML signature if it exists, and sends. The temp file is deleted.',
		'cli-label': '// programmatic mode',
		'cli-title': 'Usage in scripts and automation',
		'cli-desc': 'Integrate NeoComposer in your workflows with CLI arguments. Perfect for notifications, automated reports, and CI/CD.',
		'cli-examples-title': 'Examples',
		'cli-ex-simple': 'Simple email',
		'cli-ex-attachments': 'Multiple attachments',
		'cli-ex-bodyfile': 'Body from file',
		'cli-ex-agenda': 'Using agenda contact',
		'cli-ex-monitor': 'Integration in monitoring script',
		'cli-script-title': 'Programmatic script (examples)',
		'cli-script-desc': 'Integrate NeoComposer in bash scripts to automate sends from cron, monitoring, or CI/CD.',
		'cli-summary-table': '📜 View programmatic examples (bash)',
		'cli-ex-row1': 'Simple email with recipient, subject, and direct body',
		'cli-ex-row2': 'Email with attachment',
		'cli-ex-row3': 'Multiple attachments and body from file',
		'cli-ex-row4': 'Using agenda contact by index',
		'cli-ex-row5': 'List agenda contacts',
		'cli-ex-row6': 'Send command output (e.g. <code>df -h</code>) by email',
		'cli-ex1-title': 'Example 1: Simple email',
		'cli-ex2-title': 'Example 2: Email with attachment',
		'cli-ex3-title': 'Example 3: Multiple attachments and body from file',
		'cli-ex4-title': 'Example 4: Using agenda contact (index 1)',
		'cli-ex5-title': 'Example 5: List agenda contacts',
		'cli-ex6-title': 'Example 6: Send command output by email',
		'cli-options': 'Available options',
		'cli-flag-recipient': 'Recipient email (required if not using --agenda-index)',
		'cli-flag-subject': 'Email subject',
		'cli-flag-body': 'Message body (direct text)',
		'cli-flag-body-file': 'File with message body',
		'cli-flag-attachments': 'Files to attach (space separated, multiple)',
		'cli-flag-agenda-index': 'Contact index in agenda (1-indexed)',
		'cli-flag-list-contacts': 'List agenda contacts and exit',
		'cli-flag-interactive': 'Interactive mode (default if no other args passed)',
		'cli-flag-agenda': 'Open contact agenda management',
		'cli-flag-help': 'Show full help',
		'agenda-label': '// agenda',
		'agenda-title': 'Contact management',
		'agenda-desc': 'The agenda is a JSON at <code>~/.config/neocomposer/agenda.json</code>. The <code>agenda.sh</code> script manages it interactively.',
		'agenda-tip': 'Run <code>neocomposer --agenda</code> to manage contacts without editing the JSON manually. You can add, modify, and delete from the interactive menu.',
		'roadmap-label': '// roadmap',
		'roadmap-title': "What's coming",
		'roadmap-subtitle': "What's implemented and what's planned.",
		'roadmap-v110': 'v1.1.0 — Programmatic mode',
		'roadmap-done1': 'CLI arguments (--recipient, --subject, --body, --attachments)',
		'roadmap-done2': 'Multiple attachments support',
		'roadmap-done3': 'Body from file (--body-file)',
		'roadmap-done4': 'Contact selection by index (--agenda-index)',
		'roadmap-done5': 'Contact listing (--list-contacts)',
		'roadmap-next': 'Upcoming versions',
		'roadmap-planned1': 'Multi-account support (switch accounts at runtime)',
		'roadmap-planned2': 'Sent email history',
		'roadmap-planned3': 'Reusable email templates',
		'roadmap-planned4': 'Markdown to HTML formatting',
		'roadmap-idea1': 'Integration with password managers (pass, 1Password CLI)',
		'changelog-label': '// changelog',
		'changelog-title': 'Version history',
		'changelog-subtitle': 'Auto-generated via <a href="https://github.com/orhun/git-cliff" target="_blank" rel="noopener">git-cliff</a>.',
		'changelog-loading': 'Loading changelog…',
		'changelog-full': 'Full history: ',
		'changelog-empty-msg': 'No changelog entries yet — check back after the next release.',
		'footer-tagline': 'Made from the terminal, for the terminal.',
		'term-select': 'Select an option:',
		'term-opt1': '1. Send to a one-time recipient',
		'term-opt2': '2. Choose a recipient from agenda',
		'term-option': 'Option: ',
		'term-contacts': 'Contacts in agenda:',
		'term-contact1': '1. Ada Lovelace (ada@example.com)',
		'term-contact-num': 'Contact number: ',
		'term-subject-label': 'Subject: ',
		'term-input-subject': 'Successful deploy to production',
		'term-editor': '&lt;opens Neovim — write with all the power of the editor&gt;',
		'term-attach': 'Do you want to attach a file? (Y/N): ',
		'term-sending': 'Sending email... |',
		'term-success': '✓ Email sent successfully',
	},
	es: {
		'page-title': 'NeoComposer — Email desde la terminal',
		'page-description': 'Envía correos desde tu terminal usando Neovim como editor. Soporte CLI programático, adjuntos via Yazi, agenda de contactos, firma HTML y SMTP.',
		'nav-install': 'Instalación',
		'nav-config': 'Configuración',
		'nav-usage': 'Uso',
		'nav-cli': 'CLI',
		'nav-agenda': 'Agenda',
		'nav-roadmap': 'Roadmap',
		'nav-changelog': 'Changelog',
		'nav-github': 'GitHub',
		'hero-badge': 'v1.1.0 — estable',
		'hero-title-line1': 'Email desde la',
		'hero-title-accent': 'terminal',
		'hero-title-line3': 'como debe ser.',
		'hero-subtitle': 'NeoComposer es un cliente de correo minimalista para la terminal con soporte programático. Escribe con Neovim, adjunta con Yazi o automatiza con CLI.',
		'hero-btn-install': 'Instalar',
		'hero-btn-blog': 'Leer blog',
		'features-label': '// características',
		'features-title': 'Para el dev que vive en la terminal',
		'features-subtitle': 'NeoComposer integra las herramientas que ya usas, sin fricción. Ahora con soporte CLI para automatización.',
		'feat-evim-title': 'Neovim como editor',
		'feat-evim-desc': 'Escribe tu correo con el editor que ya dominas. Atajos, macros, plugins — todo disponible. El archivo temporal se elimina al enviar.',
		'feat-ranger-title': 'Adjuntos via Yazi',
		'feat-ranger-desc': 'Navega tu sistema de archivos con Yazi para seleccionar adjuntos. Sin escribir rutas completas. Adjunta múltiples archivos.',
		'feat-agenda-title': 'Agenda de contactos',
		'feat-agenda-desc': 'Guarda destinatarios frecuentes en un JSON. Gestión con flag -a o usa índices con --agenda-index para scripting.',
		'feat-signature-title': 'Firma HTML',
		'feat-signature-desc': 'Define una firma personalizada en HTML con imágenes, links y estilos. Se inyecta automáticamente en cada correo.',
		'feat-smtp-title': 'SMTP + TLS',
		'feat-smtp-desc': 'Conexión segura via STARTTLS. Compatible con Gmail, Outlook y cualquier proveedor SMTP estándar.',
		'feat-cli-title': 'Modo programático',
		'feat-cli-desc': 'Integra en scripts con --recipient, --subject, --body, --attachments. Automatiza notificaciones y reportes.',
		'install-label': '// instalación',
		'install-title': 'Listo en 3 pasos',
		'install-subtitle': 'El instalador detecta tu distro, instala dependencias y configura el acceso directo.',
		'install-oneliner-label': 'instalación rápida',
		'install-oneliner-note': 'El instalador descarga los archivos directamente desde GitHub. Para instalación manual, clona el repositorio y ejecuta el script localmente.',
		'install-step1': 'Clona el repositorio',
		'install-step1-desc': 'Descarga NeoComposer desde GitHub.',
		'install-step2': 'Ejecuta el instalador',
		'install-step2-desc': 'El script detecta Arch, Debian/Ubuntu o Fedora y se encarga del resto: dependencias del sistema, dependencias Python, y el symlink.',
		'install-step2-note': 'Distros soportadas: Arch, Ubuntu/Debian/Mint/Kali, Fedora/CentOS/RHEL. El instalador instala yazi, neovim, jq y python3 si no están presentes.',
		'install-step3': 'Configura tus credenciales',
		'install-step3-desc': 'Edita el archivo .env que el instalador copió a ~/.config/neocomposer/.env.',
		'config-label': '// configuración',
		'config-title': 'SMTP y Gmail',
		'config-subtitle': 'Instrucciones para conectar NeoComposer con Gmail usando contraseña de aplicación.',
		'config-warning': 'Gmail requiere contraseña de aplicación, no tu contraseña normal. Activa la verificación en dos pasos primero, luego ve a Cuenta de Google → Seguridad → Contraseñas de aplicación.',
		'config-step1': 'Activa IMAP en Gmail',
		'config-step1-desc': 'En Gmail → Configuración → Ver toda la configuración → Reenvío y correo POP/IMAP → Habilitar IMAP.',
		'config-step2': 'Genera contraseña de aplicación',
		'config-step2-desc': 'Google Account → Seguridad → Contraseñas de aplicación → Selecciona "Otra" → genera y copia la clave de 16 caracteres.',
		'config-step3': 'Configura el .env',
		'config-signature-title': 'Firma HTML (opcional)',
		'config-signature-desc': 'Crea <code>~/.config/NeoComposer/signature.html</code> con tu firma. Se añade automáticamente a cada correo.',
		'usage-label': '// uso',
		'usage-title': 'Flujo de trabajo interactivo',
		'usage-subtitle': 'NeoComposer guía el proceso paso a paso.',
		'usage-cmd-header': 'Comando',
		'usage-desc-header': 'Descripción',
		'usage-cmd1': 'Inicia el compositor de correo',
		'usage-cmd2': 'Abre la gestión de agenda de contactos',
		'usage-cmd-title': "Paso a paso al ejecutar 'neocomposer'",
		'usage-step1': 'Elige destinatario',
		'usage-step1-desc': 'Ingresa un correo de uso único o selecciona uno de tu agenda.',
		'usage-step2': 'Escribe el asunto',
		'usage-step2-desc': 'Texto libre en la terminal.',
		'usage-step3': 'Redacta en Neovim',
		'usage-step3-desc': 'Se abre un buffer temporal. Escribe con todos los poderes de Neovim. Al guardar y salir (:wq) continúa el flujo.',
		'usage-step4': 'Adjuntos opcionales',
		'usage-step4-desc': 'Si confirmas con S, se abre Yazi para navegar y seleccionar archivos. Puedes adjuntar múltiples.',
		'usage-step5': 'Envío automático',
		'usage-step5-desc': 'NeoComposer conecta al SMTP, añade la firma HTML si existe, y envía. El archivo temporal se elimina.',
		'cli-label': '// modo programático',
		'cli-title': 'Uso en scripts y automatización',
		'cli-desc': 'Integra NeoComposer en tus flujos de trabajo con argumentos CLI. Perfecto para notificaciones, reportes automatizados y CI/CD.',
		'cli-examples-title': 'Ejemplos',
		'cli-ex-simple': 'Email simple',
		'cli-ex-attachments': 'Con múltiples adjuntos',
		'cli-ex-bodyfile': 'Cuerpo desde archivo',
		'cli-ex-agenda': 'Usando contacto de agenda',
		'cli-ex-monitor': 'Integración en script de monitoreo',
		'cli-script-title': 'Script programático (ejemplos)',
		'cli-script-desc': 'Integra NeoComposer en scripts bash para automatizar envíos desde cron, monitoreo o CI/CD.',
		'cli-summary-table': '📜 Ver ejemplos programáticos (bash)',
		'cli-ex-row1': 'Email simple con destinatario, asunto y cuerpo directo',
		'cli-ex-row2': 'Email con archivo adjunto',
		'cli-ex-row3': 'Múltiples adjuntos y cuerpo desde archivo',
		'cli-ex-row4': 'Usando contacto de agenda por índice',
		'cli-ex-row5': 'Listar contactos de agenda',
		'cli-ex-row6': 'Enviar output de comando (ej: <code>df -h</code>) por email',
		'cli-ex1-title': 'Ejemplo 1: Email simple',
		'cli-ex2-title': 'Ejemplo 2: Email con archivo adjunto',
		'cli-ex3-title': 'Ejemplo 3: Múltiples adjuntos y body desde archivo',
		'cli-ex4-title': 'Ejemplo 4: Usando contacto de agenda (índice 1)',
		'cli-ex5-title': 'Ejemplo 5: Listar contactos de agenda',
		'cli-ex6-title': 'Ejemplo 6: Enviar output de comando por email',
		'cli-options': 'Opciones disponibles',
		'cli-flag-recipient': 'Email del destinatario (requerido si no usas --agenda-index)',
		'cli-flag-subject': 'Asunto del email',
		'cli-flag-body': 'Cuerpo del mensaje (texto directo)',
		'cli-flag-body-file': 'Archivo con el cuerpo del mensaje',
		'cli-flag-attachments': 'Archivos a adjuntar (espacio separado, múltiples)',
		'cli-flag-agenda-index': 'Índice del contacto en agenda (1-indexed)',
		'cli-flag-list-contacts': 'Listar contactos de la agenda y salir',
		'cli-flag-interactive': 'Modo interactivo (por defecto si no se pasan otros args)',
		'cli-flag-agenda': 'Abrir la gestión de agenda de contactos',
		'cli-flag-help': 'Mostrar ayuda completa',
		'agenda-label': '// agenda',
		'agenda-title': 'Gestión de contactos',
		'agenda-desc': 'La agenda es un JSON en <code>~/.config/neocomposer/agenda.json</code>. El script <code>agenda.sh</code> la gestiona interactivamente.',
		'agenda-tip': 'Ejecuta <code>neocomposer --agenda</code> para gestionar contactos sin editar el JSON manualmente. Puedes agregar, modificar y eliminar desde el menú interactivo.',
		'roadmap-label': '// roadmap',
		'roadmap-title': 'Qué viene',
		'roadmap-subtitle': 'Lo implementado y lo planeado.',
		'roadmap-v110': 'v1.1.0 — Modo programático',
		'roadmap-done1': 'Argumentos CLI (--recipient, --subject, --body, --attachments)',
		'roadmap-done2': 'Soporte para múltiples archivos adjuntos',
		'roadmap-done3': 'Cuerpo desde archivo (--body-file)',
		'roadmap-done4': 'Selección de contactos por índice (--agenda-index)',
		'roadmap-done5': 'Listado de contactos (--list-contacts)',
		'roadmap-next': 'Próximas versiones',
		'roadmap-planned1': 'Soporte multi-cuenta (cambio de cuenta en runtime)',
		'roadmap-planned2': 'Historial de correos enviados',
		'roadmap-planned3': 'Plantillas de correo reutilizables',
		'roadmap-planned4': 'Formato Markdown a HTML',
		'roadmap-idea1': 'Integración con gestores de contraseñas (pass, 1Password CLI)',
		'changelog-label': '// changelog',
		'changelog-title': 'Historial de versiones',
		'changelog-subtitle': 'Generado automáticamente con <a href="https://github.com/orhun/git-cliff" target="_blank" rel="noopener">git-cliff</a>.',
		'changelog-loading': 'Cargando changelog…',
		'changelog-full': 'Historial completo: ',
		'changelog-empty-msg': 'Todavía no hay entradas, volvé a revisar después del próximo release.',
		'footer-tagline': 'Hecho desde la terminal, para la terminal.',
		'term-select': 'Seleccione una opción:',
		'term-opt1': '1. Enviar a un destinatario de uso único',
		'term-opt2': '2. Elegir un destinatario de la agenda',
		'term-option': 'Opción: ',
		'term-contacts': 'Contactos en la agenda:',
		'term-contact1': '1. Ada Lovelace (ada@example.com)',
		'term-contact-num': 'Número de contacto: ',
		'term-subject-label': 'Asunto: ',
		'term-input-subject': 'Deploy exitoso en producción',
		'term-editor': '&lt;abre Neovim — escribe con toda la potencia del editor&gt;',
		'term-attach': '¿Deseas adjuntar un archivo? (S/N): ',
		'term-sending': 'Enviando correo... |',
		'term-success': '✓ Correo enviado exitosamente',
	},
};

function applyTranslations(lang) {
	const t = translations[lang] || translations.en;
	document.documentElement.lang = lang;
	localStorage.setItem('neo-lang', lang);

	document.querySelectorAll('[data-i18n]').forEach(el => {
		const key = el.getAttribute('data-i18n');
		if (!t[key]) return;
		if (el.tagName === 'TITLE') {
			document.title = t[key];
		} else if (el.tagName === 'META') {
			el.setAttribute('content', t[key]);
		} else {
			el.innerHTML = t[key];
		}
	});

	const btn = document.getElementById('lang-toggle');
	if (btn) btn.textContent = lang === 'en' ? 'ES' : 'EN';
}

document.addEventListener('DOMContentLoaded', () => {
	const saved = localStorage.getItem('neo-lang') || 'en';
	applyTranslations(saved);

	const btn = document.getElementById('lang-toggle');
	if (btn) {
		btn.addEventListener('click', () => {
			const current = localStorage.getItem('neo-lang') || 'en';
			applyTranslations(current === 'en' ? 'es' : 'en');
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

	loadChangelog();
});

const CHANGELOG_REPO = 'https://github.com/4DRIAN0RTIZ/NeoComposer';

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
		const res = await fetch('changelog.json');
		if (!res.ok) throw new Error('changelog.json not found');
		const releases = await res.json();

		const withCommits = (releases || []).filter(r => (r.commits || []).length > 0);
		if (withCommits.length === 0) {
			renderChangelogEmpty(container);
			return;
		}

		container.innerHTML = withCommits.map(release => {
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
	const lang = localStorage.getItem('neo-lang') || 'en';
	const t = translations[lang] || translations.en;
	container.innerHTML = `<p class="changelog-empty">${t['changelog-empty-msg']}</p>`;
}

# NeoComposer

> Email desde la terminal, como debe ser.

Cliente de correo minimalista para la terminal. Escribe con Neovim, adjunta con Yazi, automatiza con CLI.

---

## Instalación rápida

```bash
git clone https://github.com/4DRIAN0RTIZ/NeoComposer.git
cd NeoComposer
sudo chmod +x install_neocomposer.sh
./install_neocomposer.sh
```

Edita `~/.config/neocomposer/.env` con tus credenciales SMTP.

---

## Uso

### Modo interactivo (por defecto)

```bash
neocomposer
```

Flujo guiado paso a paso: destinatario, asunto, Neovim, adjuntos opcionales.

### Modo programático (para scripts)

```bash
# Email simple
neocomposer -r "admin@dominio.com" -s "Alerta" -b "Disco al 90%"

# Con adjuntos
neocomposer \
  -r "equipo@dominio.com" \
  -s "Reporte" \
  -a /var/log/syslog /tmp/report.pdf

# Usando contacto de la lista de contactos
neocomposer -i 1 -s "Notificación" -b "Mensaje automático"

# Listar contactos
neocomposer -l

# Usando una plantilla reutilizable
neocomposer \
  -r "admin@dominio.com" \
  -t backup \
  -V host=api-01 \
  -V status=OK
```

Ver `--help` para todas las opciones.

---

## Plantillas reutilizables

Guarda tus plantillas en `~/.config/neocomposer/templates/` como `.txt`, `.html` o `.md`.

```txt
---
subject: Backup de {{host}}
---

Hola,

El backup de {{host}} terminó con estado: {{status}}.

{{body}}
```

Uso:

```bash
neocomposer --list-templates
neocomposer -r "equipo@dominio.com" -t backup -V host=api-01 -V status=OK
```

Notas:

- `--subject` sobrescribe el `subject` definido en la plantilla.
- `--body` o `--body-file` quedan disponibles como la variable `{{body}}`.
- En modo interactivo puedes elegir una plantilla y completar sus variables antes de editar el cuerpo en Neovim.

---

## Características

- ✏️ **Neovim** como editor nativo
- 📎 **Yazi** para adjuntar archivos
- 📋 **Lista de contactos** JSON
- ✍️ **Firma HTML** personalizable
- 🧩 **Plantillas reutilizables** con variables
- 🔐 **SMTP + STARTTLS**
- ⚡ **Modo programático** con CLI
- 🚀 **Instalador multi-distro**

---

## Documentación completa

[neocomposer.cuevaneander.tech](https://neocomposer.cuevaneander.tech)

---

## Configuración SMTP (Gmail)

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=tucuenta@gmail.com
SENDER_PASSWORD=tu_app_password  # 16 dígitos
SENDER_NAME=Tu Nombre
```

Genera la contraseña en: Google Account → Seguridad → Contraseñas de aplicación.

---

## Contribuir

Abierto a contribuciones. Fork, mejora y abre PR。

```bash
git checkout -b feat/mi-feature
git commit -m "feat: descripción corta"
git push origin feat/mi-feature
```

### Hooks de git

Este repo usa `.githooks/` para hooks compartidos. Actívalos una vez por clon:

```bash
git config core.hooksPath .githooks
```

El hook `pre-push` actualiza `openwiki/` automáticamente al pushear a `develop` o `main` (requiere [openwiki CLI](https://github.com/langchain-ai/openwiki) instalado globalmente y `OPENAI_API_KEY` en el entorno; si falta alguno, se salta sin bloquear el push).

---

## Autor

Creado por [4DRIAN0RTIZ](https://github.com/4DRIAN0RTIZ) desde [La Cueva del NeanderTech](https://cuevaneander.tech)。

Hecho desde la terminal, para la terminal.

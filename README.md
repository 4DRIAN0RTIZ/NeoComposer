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

# Usando contacto de agenda
neocomposer -i 1 -s "Notificación" -b "Mensaje automático"

# Listar contactos
neocomposer -l
```

Ver `--help` para todas las opciones.

---

## Características

- ✏️ **Neovim** como editor nativo
- 📎 **Yazi** para adjuntar archivos
- 📋 **Agenda de contactos** JSON
- ✍️ **Firma HTML** personalizable
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

---

## Autor

Creado por [4DRIAN0RTIZ](https://github.com/4DRIAN0RTIZ) desde [La Cueva del NeanderTech](https://cuevaneander.tech)。

Hecho desde la terminal, para la terminal.

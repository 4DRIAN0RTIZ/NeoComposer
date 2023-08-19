# NeoComposer

Envía un correo electrónico desde la terminal utilizando Neovim como editor de texto.

## Instalación

Otorga permisos de ejecución a `install_neocomposer` de la siguiente manera:

```bash
sudo chmod +x install_neocomposer
```

## Uso

Una vez instalado, ejecuta `neocomposer` desde la terminal para enviar un correo electrónico.

Neocomposer utiliza Neovim como editor de texto, por lo que puedes utilizar todos los comandos de Neovim para escribir el correo electrónico. De manera automática se abrirá un archivo temporal en Neovim, el cual se borrará una vez que se haya enviado el correo electrónico.

Para enviar el correo con una firma, crea un archivo llamado `signature.html` en el directorio `~/.config/NeoComposer/` y escribe la firma en HTML. Por ejemplo:
```html
<table cellspacing="0" cellpadding="0">
        <tr>
            <th style="border-right: 1px solid #000; padding-right: 10px;">Nombre:</th>
            <th style="padding-left: 10px;">Correcaminos</th>
        </tr>
        <tr>
            <th style="border-right: 1px solid #000; padding-right: 10px;">Cargo:</th>
            <th style="padding-left: 10px;">Desarrollador</th>
        </tr>
        <tr>
            <th style="border-right: 1px solid #000; padding-right: 10px;">Compañía:</th>
            <th style="padding-left: 10px;">Acme Corporation</th>
        </tr>
    </table>
```

En caso de que no se cuente con el archivo `signature.html`, se enviará el correo sin firma.

## Variables de entorno

El archivo `.env` tiene la siguiente estructura:
```bash
SMTP_SERVER=
SMTP_PORT=
SENDER_EMAIL=
SENDER_PASSWORD=
SENDER_NAME=
```

Asegúrate de configurar correctamente las variables de entorno antes de utilizar Neocomposer.

## Contribuciones

El proyecto está abierto a contribuciones, así que siéntete libre de hacer un fork y enviar un pull request.

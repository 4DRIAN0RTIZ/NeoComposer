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
<table style="width: 100%; font-family: Arial, sans-serif; font-size: 14px;">
  <tr>
    <td style="text-align: center;">
      <img src="https://neandertech.netlify.app/img/logo.png" alt="Foto" style="max-width: 100px;">
    </td>
  </tr>
  <tr>
    <td style="text-align: center; font-weight: bold; color: #333;">
      La Cueva del NeanderTech
    </td>
  </tr>
  <tr>
    <td style="text-align: center;">
      Enviado desde <a href="https://github.com/4DRIAN0RTIZ/NeoComposer"
        style="text-decoration: none; color: #007bff;">Neocomposer</a>
      Visto en <a href="https://neandertech.netlify.app/blog/envia-correos-desde-la-terminal-neocomposer-esta-aqui"</a>
    </td>
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

## Agenda

La agenda de contactos es un archivo JSON que tiene la siguiente estructura:
```json
{
    "contactos": [
        {
            "nombre": "Nombre del contacto",
            "correo": "Correo electrónico del contacto"
        }
    ]
}
```

Para acceder a la agenda de contactos, ejecuta `neocomposer -a` desde la terminal.

Ten en cuenta que la agenda de contactos es opcional, por lo que puedes enviar correos sin ella. Te permite agregar, modificar, eliminar y mostrar contactos.

## Contribuciones

El proyecto está abierto a contribuciones, así que siéntete libre de hacer un fork y enviar un pull request.

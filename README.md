# Descarga Videos e Imagenes de Canales y Grupos de Telegram

## Descripción

Este script de Python está diseñado para interactuar con canales y grupos de Telegram utilizando la biblioteca Telethon. Permite la descarga de mensajes, especialmente aquellos con medios (como videos e imágenes), de canales o grupos de Telegram especificados. Además, ofrece funcionalidades para listar diálogos y manejar errores durante el proceso de descarga.

## Características

-   Descarga de mensajes con medios de canales y grupos de Telegram.
-   Registro de mensajes descargados para evitar duplicados.
-   Registro de errores para descargas fallidas.
-   Listado de todos los canales, grupos y usuarios con los que el cliente interactúa.
-   Manejo de descargas simultáneas para optimizar el rendimiento.
-   Uso de semáforos para controlar el número máximo de descargas simultáneas.
-   Guarda los registros de descargas y errores en archivos de texto separados.

## Requisitos

-   Python 3.6 o superior.
-   Bibliotecas: Telethon, pytz, tqdm.
-   Un ID de API de Telegram y hash de API válidos. https://my.telegram.org/apps
-   Archivo config.json que contenga el ID de API de Telegram, el hash de API y opcionalmente el número máximo de descargas simultáneas.

## Configuración

1. Asegúrate de que Python 3.6 o superior esté instalado.
2. Asegúrate de tener pip, el gestor de paquetes de Python, instalado en tu sistema.
3. Asegúrate de tener pip, el gestor de paquetes de Python, instalado en tu sistema.
    ```bash
    pip install -r requirements.txt
    ```
    Esto instalará todas las dependencias listadas en el archivo requirements.txt.
4. Crea un archivo config.json en el mismo directorio que el script con el siguiente contenido:
    ```json
    {
        "TELEGRAM_API_ID": "tu_api_id",
        "TELEGRAM_API_HASH": "tu_api_hash",
        "MAX_SIMULTANEOUS_DOWNLOADS": 5
    }
    ```
    Reemplaza tu_api_id y tu_api_hash con tus credenciales de API de Telegram y ajusta MAX_SIMULTANEOUS_DOWNLOADS según sea necesario.

## Uso

1. Ejecuta el script:
    ```bash
    python media.py
    ```
2. Sigue las indicaciones interactivas para elegir un canal o grupo y comenzar la descarga de mensajes. También puedes listar los canales, grupos y usuarios.

## Notas

-   El script requiere que el usuario tenga permisos apropiados en el canal o grupo de Telegram para ciertas operaciones.
-   Se recomienda usar este script de manera responsable y en cumplimiento con los términos de servicio de Telegram.

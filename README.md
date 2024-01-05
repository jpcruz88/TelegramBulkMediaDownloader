# Descargador de Mensajes de Canales/Grupos de Telegram

## Descripción

Este script de Python está diseñado para interactuar con canales y grupos de Telegram utilizando la biblioteca Telethon. Proporciona funcionalidad para descargar mensajes, especialmente aquellos con medios, de canales o grupos de Telegram especificados. Además, ofrece características para listar usuarios en un canal o grupo y manejar errores durante el proceso de descarga.

## Características

-   Descarga de mensajes con medios de canales y grupos de Telegram.
-   Registro de mensajes descargados para evitar duplicados.
-   Registro de errores para descargas fallidas.
-   Listado de todos los canales y grupos a los que pertenece el usuario.
-   Listado de usuarios en un canal o grupo específico.
-   Manejo de descargas simultáneas para optimizar el rendimiento.

## Requisitos

-   Python 3.6 o superior.
-   Biblioteca Telethon.
-   Un ID de API de Telegram y hash de API válidos. https://my.telegram.org/apps
-   Archivo `config.json` que contenga el ID de API de Telegram y el hash de API.

## Configuración

1. Asegúrate de que Python 3.6 o superior esté instalado.
2. Instala Telethon:
    ```bash
    pip install telethon
    ```
3. Crea un archivo `config.json` en el mismo directorio que el script con el siguiente contenido:
    ```json
    {
        "TELEGRAM_API_ID": "tu_api_id",
        "TELEGRAM_API_HASH": "tu_api_hash"
    }
    ```
    Reemplaza `tu_api_id` y `tu_api_hash` con tus credenciales de API de Telegram.

## Uso

1. Ejecuta el script:
    ```bash
    python media.py
    ```
2. Sigue las indicaciones interactivas para:
    - Descargar mensajes de un canal/grupo elegido.
    - Listar usuarios en un canal/grupo específico.

## Funciones

-   `get_current_time()`: Devuelve la hora actual en una zona horaria predefinida.
-   `was_downloaded(message_id, log_file)`: Verifica si un mensaje ya fue descargado.
-   `log_error(message_id, error_file)`: Registra un error para un mensaje.
-   `download_message(message, download_directory, log_file, error_file)`: Descarga el mensaje especificado.
-   `process_errors(error_file, log_file, download_directory, channel_id)`: Procesa errores registrados durante las descargas.
-   `list_channels_and_groups()`: Lista todos los canales y grupos a los que pertenece el usuario.
-   `list_users(channel)`: Lista los usuarios en un canal o grupo especificado.
-   `main()`: La función principal que inicia el cliente y maneja las entradas del usuario.

## Notas

-   El script requiere que el usuario tenga permisos apropiados en el canal o grupo de Telegram para ciertas operaciones.
-   Se recomienda usar este script de manera responsable y en cumplimiento con los términos de servicio de Telegram.

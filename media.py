from telethon import TelegramClient
import asyncio
import uuid
import os
import datetime
import pytz
import json
from tqdm.asyncio import tqdm_asyncio

with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    api_id = config['TELEGRAM_API_ID']
    api_hash = config['TELEGRAM_API_HASH']
    MAX_SIMULTANEOUS_DOWNLOADS = config.get('MAX_SIMULTANEOUS_DOWNLOADS', 5) 


timezone = pytz.timezone('America/Mexico_City')

client = TelegramClient('session_name', api_id, api_hash)

semaphore = asyncio.Semaphore(MAX_SIMULTANEOUS_DOWNLOADS)

downloaded_messages = set()
error_messages = set()

def get_current_time():
    return datetime.datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')

async def download_message(message, download_directory, log_file, error_file):
    async with semaphore:
        temp_file_name = f"temp_{uuid.uuid4()}.part"
        temp_file_path = os.path.join(download_directory, temp_file_name)
    
        extension = ''
        if message.file and message.file.ext:
            extension = message.file.ext
        final_file_name = f"{message.date.strftime('%Y-%m-%d_%H-%M-%S')}_{message.id}{extension}"
        final_file_path = os.path.join(download_directory, final_file_name)

        try:
            if message.file and message.file.size:
                progress_bar = tqdm_asyncio(total=message.file.size, desc=final_file_name)

                def progress_callback(current_bytes, total_bytes):
                    progress_bar.n = current_bytes
                    progress_bar.refresh()

                await message.download_media(file=temp_file_path, progress_callback=progress_callback)
                progress_bar.close()

                if os.path.exists(temp_file_path):
                    os.rename(temp_file_path, final_file_path)
                    print(f"{get_current_time()} - Descargado: {final_file_path}")
                    downloaded_messages.add(str(message.id))
                    with open(log_file, 'a') as file:
                        file.write(str(message.id) + '\n')
                else:
                    print(f"{get_current_time()} - No se encontró el archivo temporal: {temp_file_path}")
            else:
                print(f"{get_current_time()} - Mensaje {message.id} no tiene un archivo para descargar.")
        except Exception as e:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            print(f"{get_current_time()} - Error al descargar el mensaje {message.id}: {e}")
            error_messages.add(str(message.id))
            with open(error_file, 'a') as file:
                file.write(str(message.id) + '\n')

async def process_errors(error_file, log_file, download_directory, channel_id):
    print(f"{get_current_time()} - Iniciando procesamiento de errores...")
    
    for message_id in error_messages:
        if message_id in downloaded_messages:
            continue

        message = await client.get_messages(channel_id, ids=int(message_id))
        if message:
            await download_message(message, download_directory, log_file, error_file)
        else:
            print(f"{get_current_time()} - Mensaje {message_id} no encontrado.")

async def list_dialogs():
    print("Canales, grupos y conversaciones con usuarios:")
    contador = 1
    dialog_dict = {}
    async for dialog in client.iter_dialogs():
        if dialog.is_channel or dialog.is_group or dialog.is_user:
            nombre_dialog = dialog.name.encode('utf-8', 'ignore').decode('utf-8')
            tipo_dialog = 'Canal' if dialog.is_channel else 'Grupo' if dialog.is_group else 'Usuario'
            print(f"id:{contador}, Nombre: {nombre_dialog}, ID: {dialog.id}, Tipo: {tipo_dialog}")
            dialog_dict[contador] = dialog.id
            contador += 1
    return dialog_dict

async def main():
    try:
        await client.start()
        dialog_dict = await list_dialogs()

        selected_id = int(input("Elige el número del canal, grupo o conversación con usuario para descargar los mensajes: "))
        if selected_id in dialog_dict:
            entity_id = dialog_dict[selected_id]
            entity = await client.get_entity(entity_id)

            download_directory = f"Downloads_{entity_id}"
            log_file = f"downloads_log_{entity_id}.txt"
            error_file = f"errors_log_{entity_id}.txt"
            os.makedirs(download_directory, exist_ok=True)

            print(f"{get_current_time()} - {entity.title if hasattr(entity, 'title') else entity.first_name} ({entity_id}) encontrado, comenzando descargas...")
            tasks = set()
            async for message in client.iter_messages(entity):
                if str(message.id) in downloaded_messages or not message.media:
                    continue
                task = asyncio.create_task(download_message(message, download_directory, log_file, error_file))
                tasks.add(task)
                if len(tasks) >= MAX_SIMULTANEOUS_DOWNLOADS:
                    _done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            await asyncio.gather(*tasks)
            await process_errors(error_file, log_file, download_directory, entity_id)
            print(f"{get_current_time()} - Proceso de descarga completado.")
    except KeyboardInterrupt:
        print("Interrupción detectada, cerrando el programa...")
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        print("Todas las tareas pendientes han sido canceladas.")
    finally:
        await client.disconnect()
        print("Cliente desconectado y programa terminado.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

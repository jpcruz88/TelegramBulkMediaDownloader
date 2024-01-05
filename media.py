from telethon import TelegramClient, errors
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
import asyncio
import os
import datetime
import pytz
import json

with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    api_id = config['TELEGRAM_API_ID']
    api_hash = config['TELEGRAM_API_HASH']

timezone = pytz.timezone('America/Mexico_City')

client = TelegramClient('session_name', api_id, api_hash)

MAX_SIMULTANEOUS_DOWNLOADS = 10

def get_current_time():
    """Obtiene la hora actual en la zona horaria especificada."""
    return datetime.datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')

def was_downloaded(message_id, log_file):
    """Verifica si un mensaje ya fue descargado previamente."""
    with open(log_file, 'a+') as file:
        file.seek(0)
        downloaded = file.read().splitlines()
        if str(message_id) in downloaded:
            print(f"{get_current_time()} - Mensaje {message_id} ya fue descargado.")
            return True
        else:
            file.write(str(message_id) + '\n')
            return False

def log_error(message_id, error_file):
    """Registra un error en el archivo de errores."""
    with open(error_file, 'a') as file:
        file.write(str(message_id) + '\n')
    print(f"{get_current_time()} - Error registrado para el mensaje {message_id}.")

async def download_message(message, download_directory, log_file, error_file):
    """Descarga un mensaje del canal o grupo."""
    try:
        print(f"{get_current_time()} - Iniciando descarga: {message.id}")
        file_name = f"{message.date.strftime('%Y-%m-%d_%H-%M-%S')}_{message.id}"
        path = await message.download_media(file=download_directory + '/' + file_name)
        print(f"{get_current_time()} - Descargado: {path}")
    except Exception as e:
        print(f"{get_current_time()} - Error al descargar el mensaje {message.id}: {e}")
        log_error(message.id, error_file)

async def process_errors(error_file, log_file, download_directory, channel_id):
    """Procesa los mensajes que fallaron en la descarga anteriormente."""
    print(f"{get_current_time()} - Iniciando procesamiento de errores...")
    with open(error_file, 'r') as file:
        error_message_ids = file.read().splitlines()

    for message_id in error_message_ids:
        if was_downloaded(message_id, log_file):
            print(f"{get_current_time()} - Mensaje {message_id} ya fue procesado anteriormente.")
            continue

        message = await client.get_messages(channel_id, ids=int(message_id))
        if message:
            await download_message(message, download_directory, log_file, error_file)
        else:
            print(f"{get_current_time()} - Mensaje {message_id} no encontrado.")

async def list_channels_and_groups():
    """Lista los canales y grupos del usuario y devuelve un diccionario con los IDs."""
    print("Canales y grupos:")
    contador = 1
    channel_dict = {}
    async for dialog in client.iter_dialogs():
        if dialog.is_channel or dialog.is_group:
            nombre_canal = dialog.name.encode('utf-8', 'ignore').decode('utf-8')
            print(f"id:{contador}, Nombre: {nombre_canal}, ID: {dialog.id}, Tipo: {'Canal' if dialog.is_channel else 'Grupo'}")
            channel_dict[contador] = dialog.id
            contador += 1
    return channel_dict

async def list_users(channel):
    """Lista los usuarios de un canal o grupo."""
    offset_user = 0
    limit_user = 100

    try:
        while True:
            participants = await client(GetParticipantsRequest(
                channel,
                ChannelParticipantsSearch(''),
                offset_user,
                limit_user,
                hash=0
            ))
            if not participants.users:
                break
            for user in participants.users:
                print(f"ID: {user.id} - Nombre: {user.first_name} {' ' + user.last_name if user.last_name else ''} - @{user.username if user.username else 'Sin username'} - Estado: {user.status}")
            offset_user += len(participants.users)
    except errors.ChatAdminRequiredError:
        print("Error: Privilegios de administrador requeridos para listar usuarios en este canal o grupo.")

async def main():
    await client.start()

    channel_dict = await list_channels_and_groups()

    print("\n¿Qué te gustaría hacer a continuación?")
    print("1. Descargar mensajes de un canal o grupo")
    print("2. Listar usuarios de un canal o grupo específico")
    option_ = input("Elige una opción (1 o 2): ")

    if option_ == '1':
        selected_id = int(input("Ingresa el número del canal o grupo: "))
        if selected_id in channel_dict:
            channel_id = channel_dict[selected_id]
            channel = await client.get_entity(channel_id)

            download_directory = f"Downloads_{channel_id}"
            log_file = f"downloads_log_{channel_id}.txt"
            error_file = f"errors_log_{channel_id}.txt"
            os.makedirs(download_directory, exist_ok=True)

            print(f"{get_current_time()} - Canal o grupo {channel.title} ({channel_id}) encontrado, comenzando descargas...")
            tasks = set()
            async for message in client.iter_messages(channel):
                if was_downloaded(message.id, log_file) or not message.media:
                    continue
                task = asyncio.create_task(download_message(message, download_directory, log_file, error_file))
                tasks.add(task)
                if len(tasks) >= MAX_SIMULTANEOUS_DOWNLOADS:
                    _done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            await asyncio.gather(*tasks)
            await process_errors(error_file, log_file, download_directory, channel_id)
            print(f"{get_current_time()} - Proceso de descarga completado.")
        else:
            print("Número de canal/grupo inválido.")

    elif option_ == '2':
        selected_id = int(input("Ingresa el número del canal o grupo: "))
        if selected_id in channel_dict:
            channel_id = channel_dict[selected_id]
            channel = await client.get_entity(channel_id)
            await list_users(channel)
        else:
            print("Número de canal/grupo inválido.")

with client:
    client.loop.run_until_complete(main())

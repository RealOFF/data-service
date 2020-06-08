from pymodm import connect
from telethon import TelegramClient
from telethon.errors import ChannelPrivateError, FloodWaitError
from datetime import datetime, timedelta

import time
import os

from src.pathes import channels_config_path
from src.utils.json_utils import getJSONdata
from src.utils.data_utils import getMessageURL
from src.models.message import Message
from src.models.channel import Channel
from src.models.static.static_channel import StaticChannel
from src.models.static.static_tag import StaticTag
from src.utils.parser_utils import getSalary, getTags

async def getChannelMessages(client, channel_name, min_id=None, limit=50):
    result = []
    try:
        result = await client.get_messages(channel_name, min_id=min_id, limit=limit)
    except ChannelPrivateError:
        print('Privat channel')
        print(channel_name)
    except FloodWaitError as e:
        print('Have to sleep', e.seconds, 'seconds')
        time.sleep(e.seconds)
    return result

async def getChannelMessageIdByDate(client, channel_name, offset_date):
    try:
        messages = await client.get_messages(channel_name, offset_date=offset_date, limit=1)
    except FloodWaitError as e:
        print('Have to sleep', e.seconds, 'seconds')
        time.sleep(e.seconds)
    return messages[0].id


def getTelegramClient():
    api_id = os.environ.get('TELEGRAM_CLIENT_API_ID')
    api_hash = os.environ.get('TELEGRAM_CLIENT_API_HASH')
    session_name = 'job'
    return TelegramClient(session_name, api_id, api_hash)

def updateChannelLastDate(channel_name, last_date=datetime.now()):
    Channel.objects.raw({'name': channel_name}).update( {"$set": {"last_date": last_date}})

def getIndexNameInList(list_, name):
        for i in range(len(list_)):
            if list_[i].name == name:
                return i
        return -1

def getName(obj):
    return obj.name

#todo remove form this
async def getNewMessages(days, hours):
    if days == None:
        days = 0
    else: 
        days = int(days)
    if hours == None:
        hours = 0
    else:
        hours = int(hours)
    print('Messages fetching started')
    client = getTelegramClient()
    await client.connect()
    connect(os.environ.get('MONGODB_URL_MESSAGES'), alias='Messages')
    connect(os.environ.get('MONGODB_URL_CHANNELS'), alias='Channels')
    connect(os.environ.get('MONGODB_URL_STATIC_LISTS'), alias='StaticChannels')
    connect(os.environ.get('MONGODB_URL_STATIC_LISTS'), alias='StaticTags')
    
    channels_config = getJSONdata(channels_config_path)
    channel_names = list(map(getName, StaticChannel.objects.all()))
    tags = list(map(getName, StaticTag.objects.all()))
    url_prefix = channels_config['url_prefix']
    db_channels = list(Channel.objects.all())

    for channel_name in channel_names:
        print(channel_name)
        last_date = datetime.now() - timedelta(days=days, hours=hours)
        index = getIndexNameInList(db_channels, channel_name)

        if index == -1:
            Channel(channel_name, last_date).save()
        else:
            last_date = db_channels[index].last_date


        messages = await getChannelMessages(
            client, 
            channel_name, 
            await getChannelMessageIdByDate(client, channel_name, last_date)
        )
        updateChannelLastDate.(channel_name)

        messages_to_db = []
        for message in messages:
            if message.text is None:
                continue
            message_to_db = Message(url=getMessageURL(url_prefix, channel_name, str(message.id)),
                                            text=message.message,
                                            date=message.date,
                                            channel=channel_name,
                                          
                                            salary=getSalary(message.message),
                                            tags=getTags(message.message, tags))
            if message_to_db:
                messages_to_db.append(message_to_db)
        if len(messages_to_db) != 0:
            Message.objects.bulk_create(messages_to_db)
    
    await client.disconnect()


async def deleteOldMessages(days, hours):
    print('Clean start')
    if days == None:
        days = 0
    else: 
        days = int(days)
    if hours == None:
        hours = 0
    else:
        hours = int(hours)
    connect(os.environ.get('MONGODB_URL_MESSAGES'), alias='Messages')
    Message.objects.raw({"date": {"$lt": datetime.now() - timedelta(days=days, hours=hours)}}).delete()

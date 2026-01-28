from logmagix import Logger
import asyncio
import yaml
import re
import os
import random
from telethon import TelegramClient
from telethon.tl.functions.messages import ForwardMessagesRequest
import warnings

# Suppress DeprecationWarnings for Windows Event Loop
warnings.filterwarnings("ignore", category=DeprecationWarning)

log = Logger()

def load_config():
    """Load configuration from config.yaml"""
    config_path = 'input/config.yaml'
    if not os.path.exists(config_path):
        log.error(f"Config file not found: {config_path}")
        return None
    
    with open(config_path, 'r') as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            log.error(f"Error parsing config file: {e}")
            return None

def parse_telegram_link(link):
    """
    Parse a Telegram link to extract username/chat_id and optional message/topic_id.
    """
    link = link.strip().rstrip('/')
    match = re.search(r't\.me/([^/]+)(?:/(\d+))?', link)
    
    if match:
        username = match.group(1)
        item_id = int(match.group(2)) if match.group(2) else None
        return username, item_id
        
    return None, None

async def forward_job(client, config):
    """Core forwarding logic"""
    forwarder_conf = config.get('forwarder', {})
    source_link = forwarder_conf.get('source_message')
    destinations = forwarder_conf.get('destinations', [])
    delay = forwarder_conf.get('delay_between_forwards', 0)
    ignore_on_error = forwarder_conf.get('ignore_on_error', [])

    log.info(f"Processing source: {source_link}")
    
    src_username, src_msg_id = parse_telegram_link(source_link)
    
    if not src_username or not src_msg_id:
        log.failure(f"Could not parse source link: {source_link}")
        return

    try:
        source_entity = await client.get_input_entity(src_username)
        # Verify message exists (lightweight check, mostly ensuring entity is valid)
        log.success(f"Source found: {src_username} (ID: {src_msg_id})")
        
        for dest_link in destinations:
            dest_user, dest_topic = parse_telegram_link(dest_link)
            
            if not dest_user:
                log.warning(f"Invalid destination link skipped: {dest_link}")
                continue
                
            try:
                dest_input = await client.get_input_entity(dest_user)
                
                # Using Invoke with ForwardMessages request to support topic forwarding
                # This ensures the 'Forwarded from' header is preserved.
                # 'top_msg_id' is the parameter for Topic ID.
                
                request_kwargs = {
                    "from_peer": source_entity,
                    "id": [src_msg_id],
                    "to_peer": dest_input,
                    "random_id": [random.randint(0, 2**63)]
                }

                if dest_topic:
                    # In newer layers, 'top_msg_id' is used for topics
                    request_kwargs["top_msg_id"] = dest_topic
                
                await client(ForwardMessagesRequest(**request_kwargs))
                
                log.success(f"Forwarded to: {dest_user}" + (f" (Topic: {dest_topic})" if dest_topic else ""))
                
                if delay > 0:
                    await asyncio.sleep(delay)
                
            except Exception as e:
                error_msg = str(e)
                if dest_link in ignore_on_error:
                    log.warning(f"Failed to forward to {dest_link} (Ignored): {error_msg}")
                else:
                    log.failure(f"Failed to forward to {dest_link}: {error_msg}")
    
    except Exception as e:
        log.failure(f"Critical error during forwarding session: {e}")

async def main():
    config = load_config()
    if not config:
        return

    tg_conf = config.get('telegram', {})
    api_id = tg_conf.get('api_id')
    api_hash = tg_conf.get('api_hash')
    session_name = tg_conf.get('session_name', 'forwarder_session')
    
    mode = config.get('forwarder', {}).get('mode', 'once')
    refresh_hours = config.get('forwarder', {}).get('daily_refresh_hours', 24)

    async with TelegramClient(session_name, api_id, api_hash) as client:
        log.info("Client started.")
        
        if mode == 'daily':
            log.info(f"Running in DAILY mode. Loop every {refresh_hours} hours.")
            while True:
                await forward_job(client, config)
                log.info(f"Sleeping for {refresh_hours} hours...")
                await asyncio.sleep(refresh_hours * 3600)
        else:
            log.info("Running in ONCE mode.")
            await forward_job(client, config)
            log.info("Job execution completed.")

if __name__ == '__main__':
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

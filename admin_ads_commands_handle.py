import os
from shutil import rmtree
from config import bot, CURRENT_DIR
from admin_commands_handle import is_user_owner_handler

ads_data_dir_path = os.path.join(CURRENT_DIR, 'data', 'ads_data')
current_ad_id = ''
current_ad_dir = ''


def register_commands():
    from main import breakdown_handler

    @bot.message_handler(commands=['add_new_ad'])
    @breakdown_handler
    @is_user_owner_handler
    def add_new_ad(message):
        bot.send_message(message.chat.id, 'Enter id')
        bot.register_next_step_handler(message, id_handler)

    @bot.message_handler(commands=['delete_ad_by_id'])
    @breakdown_handler
    @is_user_owner_handler
    def delete_ad_by_id(message):
        bot.send_message(message.chat.id, 'Enter id of the ad to delete')
        bot.register_next_step_handler(message, delete_ad_id_handler)


def create_ad_directory(ad_id):
    ad_dir = os.path.join(ads_data_dir_path, str(ad_id))
    os.makedirs(ad_dir, exist_ok=True)
    return ad_dir


def save_media_file(file_id, file_extension):
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_path = os.path.join(current_ad_dir, f'{len(os.listdir(current_ad_dir)) + 1}{file_extension}')
    with open(file_path, 'wb') as f:
        f.write(downloaded_file)


def save_text_to_file(filename, text):
    with open(os.path.join(current_ad_dir, filename), 'w', encoding='utf-8') as f:
        f.write(text)


def none_handler(message, next_step, next_message):
    if message.text.strip().lower() == 'none':
        bot.send_message(message.chat.id, next_message)
        if next_step:
            bot.register_next_step_handler(message, next_step)
        return True
    return False


def id_handler(message):
    global current_ad_id, current_ad_dir

    try:
        if none_handler(message, None, 'Ad was not added.'):
            return

        ad_id = int(message.text)
        if ad_id <= 0:
            raise ValueError

        ad_dir = os.path.join(ads_data_dir_path, str(ad_id))
        if os.path.exists(ad_dir):
            bot.send_message(message.chat.id, 'Ad with this id already exists. Please enter a different id.')
            bot.register_next_step_handler(message, id_handler)
            return

        current_ad_id = ad_id
        current_ad_dir = create_ad_directory(ad_id)
        save_text_to_file('id.txt', str(ad_id))
        bot.send_message(message.chat.id, 'Enter caption')
        bot.register_next_step_handler(message, caption_handler)
    except (ValueError, AttributeError):
        bot.send_message(message.chat.id, 'Invalid id. Please enter a positive integer')
        bot.register_next_step_handler(message, id_handler)


def caption_handler(message):
    try:
        if message.text.strip().lower() == 'none':
            bot.send_message(message.chat.id, 'Caption is required. Please enter a valid caption.')
            bot.register_next_step_handler(message, caption_handler)
            return

        save_text_to_file('caption.txt', message.text)
        bot.send_message(message.chat.id, 'Enter media or "None". After sending all files, type "save"')
        bot.register_next_step_handler(message, media_handler)
    except AttributeError:
        bot.send_message(message.chat.id, 'Invalid caption. Please enter a text')
        bot.register_next_step_handler(message, caption_handler)


def media_handler(message):
    try:
        if none_handler(message, url_handler, 'Enter url'):
            return
        if message.text.strip().lower() == 'save':
            bot.send_message(message.chat.id, 'Enter url')
            bot.register_next_step_handler(message, url_handler)
            return
    except AttributeError:
        pass

    if message.content_type == 'photo':
        photo = message.photo[-1]
        save_media_file(photo.file_id, '.jpg')
    elif message.content_type == 'video':
        save_media_file(message.video.file_id, '.mp4')
    else:
        bot.send_message(message.chat.id, 'Please send a photo or video')
        bot.register_next_step_handler(message, media_handler)
        return

    bot.send_message(message.chat.id, 'Ok go next')
    bot.register_next_step_handler(message, media_handler)


def url_handler(message):
    if none_handler(message, url_caption_handler, 'Enter url_caption'):
        return

    save_text_to_file('url.txt', message.text)
    bot.send_message(message.chat.id, 'Enter url_caption')
    bot.register_next_step_handler(message, url_caption_handler)


def url_caption_handler(message):
    if none_handler(message, None, 'Ad added successfully! Now use /admin_command_update_ads_config to update ads configuration'):
        pass
    else:
        save_text_to_file('url_caption.txt', message.text)
        bot.send_message(message.chat.id, 'Ad added successfully! Now use /admin_command_update_ads_config to update ads configuration')

    global current_ad_id, current_ad_dir
    current_ad_id = ''
    current_ad_dir = ''


def delete_ad_id_handler(message):
    try:
        ad_id = int(message.text)
        ad_dir = os.path.join(ads_data_dir_path, str(ad_id))
        if os.path.exists(ad_dir):
            rmtree(ad_dir)
            bot.send_message(message.chat.id, f'Ad with id {ad_id} deleted successfully. Now use /admin_command_update_ads_config to update ads configuration')
        else:
            bot.send_message(message.chat.id, f'Ad with id {ad_id} does not exist.')
    except ValueError:
        bot.send_message(message.chat.id, 'Invalid id. Please enter a positive integer')
        bot.register_next_step_handler(message, delete_ad_id_handler)

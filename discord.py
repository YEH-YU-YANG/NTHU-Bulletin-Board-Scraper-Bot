"""
This script sends Discord webhook messages containing announcements and current date-time information.

Dependencies:
    - discord_webhook: A Python library for sending Discord webhooks.
    - json: Standard library for JSON manipulation.
    - datetime: Standard library for handling date and time.

Functions:
    - read_announcements_from_json(): Reads announcements from a JSON file and returns them as a list of dictionaries.
    - date_time(): Generates a message containing current date, time, and day of the week, then sends it via Discord webhook.
    - send_webhook(): Reads announcements from JSON, constructs messages, and sends them via Discord webhook.

Usage:
    Ensure that 'announcements.json' file exists and contains announcement data in the required format.
    Set up a Discord webhook URL in the 'web_hook_url' variable.
    Execute the script to send Discord webhook messages with current date-time information and announcements.
"""


from discord_webhook import DiscordWebhook
import json
import datetime
import os

web_hook_url = os.environ['dc_web_hook_url']
webhook = DiscordWebhook(url=web_hook_url)

# 讀取公告資訊的函式
def read_announcements_from_json():
    """
    Reads announcements from a JSON file and returns them as a list of dictionaries.

    Example Usage:
        # Assuming 'announcements.json' contains announcement data.
        announcements = read_announcements_from_json()
        print(announcements)

    Returns:
        list: A list of dictionaries containing announcement information.
              Each dictionary should have keys: 'time', 'title', and 'link'.
              Example format: [{'time': '2024-03-24 10:00:00', 'title': 'Example Announcement', 'link': 'http://example.com'}]
    """
    with open('announcements.json', 'r', encoding='utf-8') as file:
        announcements = json.load(file)
    return announcements

def date_time():
    """
    Generates a message containing current date, time, and day of the week,
    then sends it via Discord webhook.

    Example Usage:
        # This function is automatically called when the script is executed.
        # It sends a Discord webhook message with the current date, time, and day of the week.
        # No direct function call is necessary.
    """
    # 取得目前日期和時間
    now = datetime.datetime.now()
    # 格式化日期
    today_date = now.strftime("%Y-%m-%d")
    # 格式化時間
    current_time = now.strftime("%H:%M:%S")
    # 格式化星期幾（繁體中文）
    week_day = {
        0: "Monday (一)",
        1: "Tuesday (二)",
        2: "Wednesday (三)",
        3: "Thursady (四)",
        4: "Friday (五)",
        5: "Saturday (六)",
        6: "Sunday (日)"
    }[now.weekday()]

    message = ""
    message += f">>> Date： {today_date}.      Day： {week_day}.\n"
    message += f"Update Time： {current_time}\n"

                  
    webhook.content = message

    # 發送 Webhook 請求
    response = webhook.execute()
    
    
def send_webhook():
    """
    Reads announcements from JSON, constructs messages, and sends them via Discord webhook.

    Example Usage:
        # Assuming 'announcements.json' contains announcement data and 'web_hook_url' is set.
        send_webhook()

    This function reads announcements from a JSON file using read_announcements_from_json(),
    constructs messages for each announcement, and sends them via Discord webhook.
    It sends multiple webhook requests if the number of announcements exceeds 10.
    """
    announcements = read_announcements_from_json()
    total_announcements = len(announcements)

    # 計算需要發送的 Webhook 請求次數
    num_requests = total_announcements // 10 + (1 if total_announcements % 10 != 0 else 0)

    for i in range(num_requests):

        # 計算要處理的公告索引範圍
        start_index = i * 10
        end_index = min(start_index + 10, total_announcements)
        
        for announcement in announcements[start_index:end_index]:

            
            # 創建要發送的訊息
            message = ""
            message += f"{announcement['time']} - [{announcement['title']}]({announcement['link']})\n"

            # 將訊息添加到 Webhook 中
            webhook.content = message
        
            response = webhook.execute()

        
        
if __name__ == "__main__":
    try:
        date_time()
        send_webhook()
    except Exception as e:
        print(f"Error: {e}")

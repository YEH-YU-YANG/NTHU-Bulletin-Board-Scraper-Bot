from bs4 import BeautifulSoup
import requests
import json

def scrape_announcements():
    """
    Scrapes announcements from a specific webpage and returns a list of dictionaries containing announcement details.

    Returns:
        list: A list of dictionaries where each dictionary represents an announcement with keys 'time', 'title', and 'link'.

    Example:
        >>> announcements = scrape_announcements()
        >>> print(announcements)
        [
            {'time': '2024-03-23', 'title': 'Sample Announcement 1', 'link': 'https://example.com/announcement1'},
            {'time': '2024-03-22', 'title': 'Sample Announcement 2', 'link': 'https://example.com/announcement2'},
            {'time': '2024-03-21', 'title': 'Sample Announcement 3', 'link': 'https://example.com/announcement3'}
        ]
    """
    
    url = "https://dcs.site.nthu.edu.tw/p/403-1174-64-1.php"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    announcements = []

    # 找到所有包含公告的區塊
    announcement_blocks = soup.find_all("div", class_="row listBS")

    for block in announcement_blocks:
        # 使用 find 方法找到第一個 <i> 標籤
        i_tag = block.find("i")
        if i_tag:
            time_stamp = i_tag.text.strip()  # 獲取日期信息
        else:
            time_stamp = ""  # 如果找不到日期信息，設置為空字符串
        
        # 在每個區塊中尋找所有 <a> 標籤
        a_tags = block.select("a")
        for a_tag in a_tags:
            title = a_tag.text.strip()
            link = a_tag["href"]
            announcements.append({
                "time": time_stamp,
                "title": title, 
                "link": link
            })

    return announcements


    
if __name__ == "__main__":
    announcements = scrape_announcements()

import schedule
import time
from links_retrieve import page_load_status, get_links
from comment_download import get_comments

def program():
    print('Running Schedule')
    new_links = get_links()
    if len(new_links)!=0:
        print('New Links Obtained')
        comment_download(new_links)

schedule.every().hour.do(program)

while True:
    schedule.run_pending()
    time.sleep(1)

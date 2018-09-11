import requests
from bs4 import BeautifulSoup
import time
import datetime

#url_mainpage = 'https://rostov-nd.besposrednika.ru/sdam/poisk/search/results?field_category[0]=10&field_category[1]=6&field_category[2]=7&field_category[3]=8&field_category[4]=9&field_podselenie=net&field_price[from]=10000&field_price[to]=15000&field_gallery[0]=1&field_closed[0]=net&search_for=&phrase=all'
url_bot='https://api.telegram.org/bot643550955:AAFKbTqrXfKvkjUIiaOwcwqj4rrya2F7Ots/sendMessage?chat_id=200521939&text='
url_mainpage = 'https://rostov-nd.besposrednika.ru/'
chat_id=200521939
def getData(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
    data = requests.get(url, headers = headers)
    text=data.text
    #print(text)
    f = open('text.txt', 'tw', encoding='utf-8')
    f.write(text)
    f.close()
    return text

def findNotes(data,url):
    urls_file=open('urls.txt', 'r+', encoding='utf-8')
    urls_known=urls_file.read()
    soup = BeautifulSoup(data, 'html.parser')
    note_list = soup.find_all('div', {'class': 'sEnLiCell unavailable'})
    flag=True
    for note in note_list:
        note_link = note.find('div', {'class': 'sEnLiTitle'}).find('a').get('href')
        if urls_known.find(note_link)<0:
            note_desc = note.find('div', {'class': 'sEnLiTitle'}).find('a').text.strip()
            note_price = note.find('div', {'class': 'sEnLiPrice'}).text.strip()
            note_date = note.find('div', {'class': 'sEnLiDate'}).text.strip()
            note_adr = note.find('div', {'class': 'sEnLiCity'}).text.strip()
            #out = print('Addr: {} \nDesc: {} \nPrice: {} \nDate: {}'.format(note_adr,note_desc,note_price,note_date))
            #payload = {'chat_id': chat_id, 'text': note_link}
            url_with_text='{}Addr:%20{}%20%0ADesc:%20{}%20%0APrice:%20{}%20%0ADate:%20{}%0ALink:%20{}'.format(url,note_adr,note_desc,note_price,note_date,note_link)
            #url_with_text=url+note_link
            try:
                data = requests.get(url_with_text)#, params = payload)
                print('{} Send: {}'.format(datetime.datetime.now(),note_link))
                #print(data.text)
                #print(note_link)
                urls_file.write(note_link + '\n')
            except Exception as e:
                print('{} Failed: {}'.format(datetime.datetime.now(),e)) 
            flag=False
    urls_file.close()

    #movie_link = item.find('div', {'class': 'nameRus'}).find('a').get('href')
    #movie_desc = item.find('div', {'class': 'nameRus'}).find('a').text

def main():
    html_data = getData(url_mainpage)
    while True:
        findNotes(html_data,url_bot)
        print('{} sleep'.format(datetime.datetime.now()))
        time.sleep(120)

if __name__ == '__main__':  
    main()
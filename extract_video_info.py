from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
from youtube_transcript_api import YouTubeTranscriptApi

# init session
session = HTMLSession()

def get_video_info(url):
    # download HTML code
    response = session.get(url)
    # execute Javascript
    response.html.render(sleep=1, timeout=60)
    # create beautiful soup object to parse HTML
    soup = bs(response.html.html, "html.parser")
    # open("index.html", "w").write(response.html.html)
    # initialize the result
    result = {}
    # result = soup.find_all("meta")
    # video title
    result["title"] = soup.find("meta", itemprop="name")['content']

    try:
        result["unlisted"] = soup.find("meta", itemprop="unlisted")['content']
    except:
        result["unlisted"] = "False"

    # video views
    result["views"] = soup.find("meta", itemprop="interactionCount")['content']
    # video description
    result["description"] = soup.find("meta", itemprop="description")['content']
    # date published
    result["date_published"] = soup.find("meta", itemprop="datePublished")['content']
    # get the duration of the video
    result["duration"] = soup.find("span", {"class": "ytp-time-duration"}).text
    # get the video tags
    result["tags"] = ', '.join([ meta.attrs.get("content") for meta in soup.find_all("meta", {"property": "og:video:tag"}) ])
    
    # number of likes
    text_yt_formatted_strings = soup.find_all("yt-formatted-string", {"id": "text", "class": "ytd-toggle-button-renderer"})
    try:
        result["likes"] = ''.join([ c for c in text_yt_formatted_strings[0].attrs.get("aria-label") if c.isdigit() ])
        result["likes"] = 0 if result["likes"] == '' else int(result["likes"])
    except:
        result["likes"] = 0
    # number of dislikes
    try:
        result["dislikes"] = ''.join([ c for c in text_yt_formatted_strings[1].attrs.get("aria-label") if c.isdigit() ])
        result["dislikes"] = 0 if result["dislikes"] == '' else int(result["dislikes"])
    except:
        result["dislikes"] = 0

    # channel details
    channel_tag = soup.find("yt-formatted-string", {"class": "ytd-channel-name"}).find("a")
    # channel name
    channel_name = channel_tag.text
    # channel URL
    channel_url = f"https://www.youtube.com{channel_tag['href']}"
    # number of subscribers as str
    channel_subscribers = soup.find("yt-formatted-string", {"id": "owner-sub-count"}).text.strip()
    result['channel'] = {'name': channel_name, 'url': channel_url, 'subscribers': channel_subscribers}
    return result


def get_video_all(url):
    # download HTML code
    response = session.get(url)
    # execute Javascript
    response.html.render(timeout=60)
    # create beautiful soup object to parse HTML
    soup = bs(response.html.html, "html.parser")
    # open("index.html", "w").write(response.html.html)

    result = soup.find_all("meta")
    return result



def get_transcript(id):
    texts = YouTubeTranscriptApi.get_transcripts([id], languages=['pt'])
    dialogs = list()
    for t in texts[0].get(id):
        elem_str = t.get('text')
        elem_str = elem_str.replace('\n',' ')
        elem_str = elem_str.replace('... ...',' ') 
        dialogs.append(elem_str)

    entire_dialog = ''
    for d in dialogs:
        if len(d.strip()) > 0:
            entire_dialog += d.replace('\'','"') + ' '

    entire_dialog = entire_dialog.replace('... ...',' ')
    entire_dialog = entire_dialog.replace(' pro ',' para o ')
    entire_dialog = entire_dialog.replace(' pra ',' para ')

    return entire_dialog


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="YouTube Video Data Extractor")
    parser.add_argument("id", help="ID of the YouTube video")

    args = parser.parse_args()
    # parse the video URL from command line
    id = args.id
    
    url = "https://www.youtube.com/watch?v="+str(id)

    try:
        data = get_video_info(url)
        
        # print in nice format
        print(f"\nTitle: {data['title']}")
        print(f"Unlisted: {data['unlisted']}")
        print(f"Views: {data['views']}")
        print(f"Published at: {data['date_published']}")
        print(f"Video Duration: {data['duration']}")
        print(f"Video tags: {data['tags']}")
        print(f"Likes: {data['likes']}")
        print(f"Dislikes: {data['dislikes']}")
        print(f"\nDescription: {data['description']}\n")
        print(f"\nChannel Name: {data['channel']['name']}")
        print(f"Channel URL: {data['channel']['url']}")
        print(f"Channel Subscribers: {data['channel']['subscribers']}")
    except:
        print("Youtube Video NOT found")

    try:
        dialogs = get_transcript(id)
        print("\nDialogs")
        print(dialogs)
        print("")
    except:
        pass

    #data_all = get_video_all(url)
    #print(data_all)
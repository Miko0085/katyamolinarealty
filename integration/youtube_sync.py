"""Read-only YouTube metadata importer. No publishing, no secrets written."""
import argparse, json, os, urllib.parse, urllib.request
from pathlib import Path

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--channel-id',required=True)
    parser.add_argument('--output',default='youtube-import.json')
    args=parser.parse_args()
    key=os.environ.get('YOUTUBE_API_KEY')
    if not key: parser.error('Set YOUTUBE_API_KEY in the environment')
    def get(resource, **params):
        query=urllib.parse.urlencode(dict(params,key=key))
        try:
            with urllib.request.urlopen('https://www.googleapis.com/youtube/v3/'+resource+'?'+query, timeout=30) as res:
                return json.load(res)
        except Exception as exc:
            raise SystemExit('YouTube API request failed: '+type(exc).__name__) from None
    channels=get('channels',part='contentDetails',id=args.channel_id)['items']
    if not channels: raise SystemExit('Channel not found')
    playlist=channels[0]['contentDetails']['relatedPlaylists']['uploads']
    ids=[]; token=None
    while True:
        params=dict(part='contentDetails',playlistId=playlist,maxResults=50)
        if token: params['pageToken']=token
        data=get('playlistItems',**params)
        ids.extend(x['contentDetails']['videoId'] for x in data['items'])
        token=data.get('nextPageToken')
        if not token: break
    ids=list(dict.fromkeys(ids)); rows=[]
    for i in range(0,len(ids),50):
        for v in get('videos',part='snippet,contentDetails,status',id=','.join(ids[i:i+50]))['items']:
            if v['status'].get('privacyStatus')!='public' or not v['status'].get('embeddable'): continue
            s=v['snippet']; rows.append(dict(youtube=v['id'],title=s['title'],description=s['description'],publishedAt=s['publishedAt'],duration=v['contentDetails']['duration'],thumbnails=s['thumbnails'],channelTitle=s['channelTitle'],status='draft',chapters=[],transcript=[]))
    Path(args.output).write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Exported {len(rows)} public embeddable videos for review')
if __name__=='__main__': main()


#import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import re
import pandas as pd

# modify this function to get URLs
def getURLs():
    youtubeVideoURLs = ["https://www.youtube.com/watch?v=bW3IQ-ke43w",
                       "https://www.youtube.com/watch?v=LrVhBokiZas",
                       "https://www.youtube.com/watch?v=_mCC-68LyZM"]
    return youtubeVideoURLs

def writeToFile(df):
    df.to_csv('results.csv')

def getVideoIDfromURL(URL):
    # regex pattern to match youtube URL and get video ID
    # some formats that are supported:
    # www.youtube.com/v/r8IwCQ4zL50
    # www.youtube.com?v=r8IwCQ4zL50
    # http://www.youtube.com/watch?v=r8IwCQ4zL50&feature=youtu.be
    # http://www.youtube.com/watch?v=r8IwCQ4zL50
    # youtu.be/r8IwCQ4zL50
    # http://www.youtube.com/watch?feature=player_detailpage&v=r8IwCQ4zL50#t=31s
    # //www.youtube.com/watch?v=r8IwCQ4zL50&feature=youtu.be
    # //www.youtube.com/watch?v=r8IwCQ4zL50
    # //www.youtube.com/watch?feature=player_detailpage&v=r8IwCQ4zL50#t=31s
    # //www.youtube.com/embed/r8IwCQ4zL50
    youtubeURLpattern = '((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)'
    # parse with regex and return parsed value
    match = re.search(youtubeURLpattern,URL)
    if match:
        return match.group(0)
    else:
        return None



def getVideoInfo(vid):

    # settings for Youtube API call
    api_service_name = "youtube"
    api_version = "v3"
    # TODO!!! you should change this to your own API KEY
    DEVELOPER_KEY = ***************************************

    # make youtube API call to get video info
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    # part = id get you id and basic info
    # part = snippet get you
    #        publishedAt, channelId, title, description, thumbnails, channelTitle, tags[],
    #        categoryId, liveBroadcastContent, defaultLanguage, localized
    # part = contentDetails get you
    #        duration, dimension, definition, caption, licensedContent, regionRestriction
    #        contentRating, projection, hasCustomThumbnail
    # detail info on which part get you what info can be found here
    # https://developers.google.com/youtube/v3/docs/videos#resource
    request = youtube.videos().list(
        part="id,snippet,contentDetails",
        id=vid
    )
    response = request.execute()

    return response


def downloadCaption(vid):
    pass


if __name__ == "__main__":

    # get desired video IDs
    videoURLs = getURLs()

    # initialize dataframe
    cols = ['vid','url','title','description','caption']

    df = pd.DataFrame(columns=cols)
    videoID = None
    # loop over all videos and parse information
    for URL in videoURLs:
        # data container for the current entry
        d = {'vid':None,'url':None,'title':None,'description':None,'caption':None}
        d['url'] = URL
        videoID = getVideoIDfromURL(URL)
        if videoID:
            d['vid'] = videoID
            # get response
            response = getVideoInfo(videoID)
            d['title'] = response['items'][0]['snippet']['title']
            d['description'] = response['items'][0]['snippet']['description']

            if response['items'][0]['contentDetails']['caption'] == 'false':
                pass # no caption
            else:
                downloadCaption(videoID)
                d['caption'] = True
        #print(d)
        df = df.append(d, ignore_index=True)
        videoID = None

    writeToFile(df)

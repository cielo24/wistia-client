# Wistia Client

A small and simple wrapper of the Wistia API. Currently only supporting the Wistia Data API.


## Getting Started with Wistia API

### Step 1: Get the API Token

All accounts already have at least one API Token, you can access them at: `https://XYZ.wistia.com/account/api`.
Some endpoints may required specific permissions, so keep that in mind.

### Step 2: Create a project

This project will be where all the media will be stored inside the account, you should create it using the web interface.

After the project is created, you can look at its URL (`https://XYZ.wistia.com/projects/HASHED_ID`) to get the project's `hashed_id`.
This will be used to list all media from this project in the next step.

### Step 3: List project media

You can list your project media using this:
```
from wistia_client.wistia_data_client import WistiaDataClientV1
client = WistiaDataClientV1(API_TOKEN)
project_medias = client.get_project_medias(PROJECT_HASHED_ID)
```

This method accepts the two optional parameters `page` (defaults to `1` which is the first page) and `per_page` (defaults to `100`) where you can use to fetch less or more media and even change pages. These are sorted by most recent media as being the first ones.

### Step 4: Selecting media assets

Each media has one or more video asset files that you may want to download, you can check them like this:

```
first_media = project_medias[0]
assets = first_media["assets"]
first_asset = assets[0]
print(json.dumps(first_asset, indent=4))
```

Each asset has this structure:

```
{
    "url": "http://embed.wistia.com/deliveries/ABC.bin",
    "width": 640,
    "height": 400,
    "fileSize": 12345678,
    "contentType": "video/mp4",
    "type": "OriginalFile"
}
```

### Step 5: Downloading media

After selecting the media and asset you want to download, you can download that media as such:

```
media_name = first_media["name"]
with open(f"{media_name}.mp4", "wb") as file: # This is assuming the asset is an mp4 file.
    client.download_asset(first_asset, file)
```

### Step 6: Upload SRT captions

To upload SRT files to a media, you will need the media hashed id, the language code in ISO-639–2 and the srt data:

```
media_hashed_id = first_media["hashed_id"]
language_code = "eng"
sample_srt = b"1\n00:00:00,000 --> 00:00:03,000\nOh caption, my caption."
client.upload_media_srt(media_hashed_id, language_code, sample_srt)
```

## Rate limits

The rate limits for the API is 600 requests per minute.

Fetching media information counts towards the rate limit but downloading assets does not count to this number as it doesn't use the api.

import json
import requests


class WistiaDataClientV1:
    ENDPOINT = "https://api.wistia.com/v1"

    def __init__(self, api_token):
        """
        `api_token` can be acquired at https://XX.wistia.com/account/api
        """
        self.api_token = api_token
        self.default_headers = {"Authorization": f"Bearer {self.api_token}"}

    def _request_get(self, method, params=None):
        response = requests.get(
            f"{self.ENDPOINT}/{method}", headers=self.default_headers, params=params
        )
        response.raise_for_status()
        if response.content:
            return response.json()

    def _request_post(self, method, data=None, files=None):
        response = requests.post(
            f"{self.ENDPOINT}/{method}",
            headers=self.default_headers,
            data=data,
            files=files,
        )
        response.raise_for_status()
        if response.content:
            return response.json()

    def _request_delete(self, method, params=None):
        response = requests.delete(
            f"{self.ENDPOINT}/{method}", headers=self.default_headers, params=params
        )
        response.raise_for_status()
        if response.content:
            return response.json()

    def get_project_medias(self, project_hashed_id, page=None, per_page=None):
        """
        Gets the list of most recently added media to the project with this
        `project_hashed_id`.
        """
        return self._request_get(
            f"medias.json",
            params={
                "project_id": project_hashed_id,
                "page": page,
                "per_page": per_page,
                "sort_by": "created",
                "sort_direction": "0",  # Descending
            },
        )

    def delete_media(self, media_hashed_id):
        """
        Deletes media with this `media_hashed_id`.
        """
        return self._request_delete(f"medias/{media_hashed_id}.json")

    def download_asset(self, asset, file_obj, progress_callback=None):
        """
        Takes in `asset` data and downloads it into the `file_object`.

        If `progress_callback` is provided, it will be used to send the
        percentage of the download as a float back, to be used with logging. It
        will report every 1MiB as per chunk size.
        """

        url = asset["url"]
        file_size = asset["fileSize"]
        downloaded_bytes = 0

        with requests.get(url, stream=True) as stream:
            stream.raise_for_status()
            # Using 1MiB just to prevent high ram usage.
            for chunk in stream.iter_content(1 << 20):
                if progress_callback:
                    downloaded_bytes += len(chunk)
                    progress_callback(downloaded_bytes / file_size)

                file_obj.write(chunk)

    def upload_media_srt(self, media_hashed_id, language_code, srt_text):
        """
        Uploads an SRT data to a media with this `media_hashed_id`.
        """
        return self._request_post(
            f"medias/{media_hashed_id}/captions.json",
            data={"language": language_code},
            files={"caption_file": srt_text},
        )

    def get_media_srt_list(self, media_hashed_id):
        """
        Lists all available SRT files for this `media_hashed_id`
        """
        return self._request_get(f"medias/{media_hashed_id}/captions.json")

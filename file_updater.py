import os
import requests
from datetime import datetime

class FileUpdater:
    def __init__(self, username, repository, branch, local_path):
        self.username = username
        self.repository = repository
        self.branch = branch
        self.local_path = local_path

    def _get_all_files_in_repo(self):
        url = f"https://api.github.com/repos/{self.username}/{self.repository}/contents?ref={self.branch}"
        response = requests.get(url)
        response.raise_for_status()
        return [file_info["path"] for file_info in response.json() if file_info["type"] == "file"]

    def _get_github_file_modification_time(self, file_path):
        url = f"https://api.github.com/repos/{self.username}/{self.repository}/commits?path={file_path}&per_page=1"
        response = requests.get(url)
        response.raise_for_status()
        last_modified = datetime.strptime(response.json()[0]["commit"]["author"]["date"], "%Y-%m-%dT%H:%M:%SZ")
        return last_modified

    def compare_modification_times(self):
        github_files = self._get_all_files_in_repo()

        for file_path in github_files:
            local_file_path = os.path.join(self.local_path, file_path)
            if os.path.exists(local_file_path):
                local_mod_time = datetime.fromtimestamp(os.path.getmtime(local_file_path))
                github_mod_time = self._get_github_file_modification_time(file_path)
                print(f"File: {file_path}, Local: {local_mod_time}, GitHub: {github_mod_time}, Same: {local_mod_time == github_mod_time}")
            else:
                print(f"File: {file_path}, Local: Not found, GitHub: {self._get_github_file_modification_time(file_path)}")

# Example usage:
file_updater = FileUpdater("RoseTheFlower", "MetroSteam", "master", "themes/RoseTheFlower-MetroSteam")
file_updater.compare_modification_times()

import os
import csv
import requests
import time
from tqdm import tqdm

# 替換這個變數為實際的資料夾路徑
paper_list_root = "paper_list"


def download_file(url, file_path) -> None:
    """
    Download file from url to file_path
    """
    if os.path.exists(file_path):
        raise FileExistsError(f"File already exists: {file_path}")

    file_path = os.path.abspath(file_path)
    file_folder = os.path.dirname(file_path)
    os.makedirs(file_folder, exist_ok=True)

    with requests.get(url, stream=True) as response:
        if response.status_code != 200:
            raise requests.RequestException(
                f"Failed to download {file_path} from {url}"
            )

        total_size = int(response.headers.get("content-length", 0))
        block_size = 1024
        with open(file_path, "wb") as file, tqdm(
            desc=f"Downloading {file_path}",
            total=total_size,
            unit="B",
            unit_scale=True,
            unit_divisor=block_size,
            leave=False,
        ) as bar:
            for data in response.iter_content(block_size):
                file.write(data)
                bar.update(len(data))


def manual_download_file(url, file_path, manual_download_dir, show_download_dir=False):
    """
    Download file from url to file_path, but ask user to download it into download_dir, then move it to file_path
    """
    if os.path.exists(file_path):
        raise FileExistsError(f"File already exists: {file_path}")

    file_path = os.path.abspath(file_path)
    file_folder = os.path.dirname(file_path)
    os.makedirs(file_folder, exist_ok=True)

    manual_download_dir = os.path.expanduser(manual_download_dir)
    manual_download_dir = os.path.abspath(manual_download_dir)

    # ask user to download the file
    # TODO: use `open` to automatically open the download link
    display_filename = os.path.basename(file_path)
    if show_download_dir:
        input(f"Download {display_filename} into {manual_download_dir} then press Enter: {url}")
    else:
        input(f"Download {display_filename} then press Enter: {url}")
    # print("\033[F\033[K", end="")

    # get newest file in download_dir
    files = os.listdir(manual_download_dir)
    if not files:
        raise FileNotFoundError("No file downloaded")
    files.sort(key=lambda x: os.path.getctime(os.path.join(manual_download_dir, x)))
    newest_file = files[-1]

    # check if the file is downloaded within 1 minute
    if os.path.getctime(os.path.join(manual_download_dir, newest_file)) < time.time() - 60:
        raise TimeoutError("File download timeout")
    
    # move the file to file_path
    os.rename(os.path.join(manual_download_dir, newest_file), file_path)


def read_csv(csv_file):
    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


if __name__ == "__main__":
    csv_file = "papers.csv"
    paper_csv = read_csv(csv_file)
    print(paper_csv)

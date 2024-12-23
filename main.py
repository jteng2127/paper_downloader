from download import download_file, manual_download_file
from google_api import get_credentials, fetch_spreadsheet
import pandas as pd
import logging
import dotenv
import os

dotenv.load_dotenv()
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
RANGE = os.getenv("RANGE")

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    is_skip_ieee = (input("Skip IEEE papers? (Y/n): ") or "Y").lower() == "y"
    if not is_skip_ieee:
        manual_download_dir = input("Enter the manual download directory: ")

    logger.info("Fetching spreadsheet...")
    creds = get_credentials()
    df = fetch_spreadsheet(creds, SPREADSHEET_ID, RANGE)

    paper_count = 0
    ieee_count = 0
    no_link_count = 0
    downloaded_count = 0
    failed_count = 0
    for index, row in df.iterrows():
        if row["download"] == "1":
            paper_count += 1
            filename = f'{paper_count:03d}_{row["title"].replace("/", "_")}'
            filepath = f"papers/{filename}.pdf"
            link = row["link"]

            if link == "":
                logger.error(f"Link is empty for paper {paper_count}: {filename}")
                no_link_count += 1
                continue

            if "ieee" in link:
                ieee_count += 1
                if is_skip_ieee:
                    logger.info(f"Skipping IEEE paper: {filename}")
                    continue
                else:
                    try:
                        manual_download_file(link, filepath, manual_download_dir)
                        logger.info(f"Downloaded paper {paper_count}: {filename}")
                        downloaded_count += 1
                    except FileExistsError:
                        logger.info(f"File already exists: {filename}.pdf, skipping...")
                        downloaded_count += 1
                    except Exception as e:
                        logger.error(f"Failed to download {filename}: {e}")
                        failed_count += 1
            else:
                try:
                    download_file(link, filepath)
                    logger.info(f"Downloaded paper {paper_count}: {filename}")
                    downloaded_count += 1
                except FileExistsError:
                    logger.info(f"File already exists: {filename}.pdf, skipping...")
                    downloaded_count += 1
                except Exception as e:
                    logger.error(f"Failed to download {filename}: {e}")
                    failed_count += 1
    logger.info(
        f"Downloaded {downloaded_count} papers, {failed_count} failed, {ieee_count} IEEE papers, {no_link_count} no link"
    )


def main2():
    creds = get_credentials()
    df = fetch_spreadsheet(creds, SPREADSHEET_ID, RANGE)
    local_df = pd.read_csv("papers.csv")
    cnt = 0
    for index, row in df.iterrows():
        title = row["title"]
        if title in local_df["Title"].values:
            cnt += 1
            local_df_idx = local_df[local_df["Title"] == row["title"]].index[0]
            print(local_df.loc[local_df_idx]["URL"])
        else:
            print()
    print(cnt)


if __name__ == "__main__":
    main()

import csv, os, shutil, requests
from urllib.parse import urlparse

from default_variables import CSV_HEADER, CSV_FIELDNAMES

from helpers.debug_helper import print_debug_log

OUTPUT_FOLDER = "output"

def write_report(article_info_list):
    try:
        __create_empty_output_folder__()
        __download_all_pictures__(article_info_list)
        __write_report_file__(article_info_list)

        print_debug_log("Report written successfully!")
    except Exception as ex:
        print_debug_log(f"Error when writing report: {ex}")

def __create_empty_output_folder__():
    print_debug_log("Checking output folder")
    
    output_folder_exists = os.path.isdir(OUTPUT_FOLDER)

    if output_folder_exists:
        print_debug_log("Output folder already exists. Deleting...")
        shutil.rmtree(OUTPUT_FOLDER)

    os.makedirs(OUTPUT_FOLDER)

    print_debug_log("New output folder created")

def __download_all_pictures__(article_info_list):

    print_debug_log(f"Downloading {len(article_info_list)} images")

    for article_info in article_info_list:

        picture_url_parse = urlparse(article_info["picture_url"])
        picture_filename = os.path.basename(picture_url_parse.path)

        article_info["picture_filename"] = picture_filename

        try:
            response = requests.get(article_info["picture_url"])

            with open(f"{OUTPUT_FOLDER}/{picture_filename}", "wb") as f:
                f.write(response.content)
        except:
            print_debug_log(f"Error when downloading image {picture_filename}")
        finally:
            # The report doesn't need the full url, but only the picture filename
            del article_info["picture_url"]

    print_debug_log(f"Downloaded all images")

def __write_report_file__(article_info_list):
    print_debug_log("Report file opened")

    with open("nyt_report.csv", "wt", encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)

        writer.writerow(CSV_HEADER)

        writer.writerows(article_info_list)    

    print_debug_log("Report file closed")
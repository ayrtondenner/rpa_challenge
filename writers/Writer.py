import os, shutil, requests
from urllib.parse import urlparse

from helpers.debug_helper import print_debug_log

# Importing libs for parallel download
from multiprocessing import Pool, cpu_count

class Writer(object):
    __OUTPUT_FOLDER__ = "output"

    def __init__(self, article_info_list):
        self.article_info_list = article_info_list

    def write_report(self):
        """Read article info list, creates a folder, download all related images and writes a report
        """
        try:
            self.__create_empty_output_folder__()
            self.__get_filename_from_urls__()
            self.__download_all_pictures__()
            self.__delete_urls_from_article_list__()

            print_debug_log("Report file opened")
            self.__write_report_file__()
            print_debug_log("Report file closed")

            print_debug_log("Report written successfully!")
        except Exception as ex:
            print_debug_log(f"Error when writing report: {ex}")

    def __create_empty_output_folder__(self):
        """Deletes the output folder if it exists, and creates an empty output folder
        """
        try:
            print_debug_log("Checking output folder")
            
            output_folder_exists = os.path.isdir(self.__OUTPUT_FOLDER__)

            if output_folder_exists:
                print_debug_log("Output folder already exists. Deleting...")
                shutil.rmtree(self.__OUTPUT_FOLDER__)

            os.makedirs(self.__OUTPUT_FOLDER__)

            print_debug_log("New output folder created")
        except Exception as ex:
            print_debug_log(f"Error when deleting output folder: {ex}")

    def __get_filename_from_urls__(self):
        """Get filenames from images url
        """
        self.article_info_list = [self.__get_filename_from_url__(article_info) for article_info in self.article_info_list]

    def __delete_urls_from_article_list__(self):
        """Delete 'picture_url' property from articles info, since this information shouldn't be in the report
        """

        for article_info in self.article_info_list:
            if "picture_url" in article_info:
                
                # The report doesn't need the full url, but only the picture filename
                del article_info["picture_url"]

    def __download_all_pictures__(self):
        """Creates a multiprocessing pool to download all articles images
        """
        try:

            articles_count = len(self.article_info_list)

            print_debug_log(f"Downloading {articles_count} images and using {cpu_count()} CPUs")

            # Creating pool of CPU workers to parallelize images download

            pool = Pool(cpu_count())
            download_results = pool.map(self.__download_picture__, self.article_info_list)
            pool.close()
            pool.join()

            download_success_count = download_results.count(True)
            download_success_percentage = round(download_success_count/articles_count * 100, 4)

            print_debug_log(f"Downloaded with success {download_success_count}/{articles_count} ({download_success_percentage}%) images")

        except Exception as ex:
            print_debug_log(f"Error when downloading all pictures: {ex}")

    def __write_report_file__(self):
        """Method that must be implemented in child class

        Raises:
            NotImplementedError: this method must be implemented in child class
        """
        raise NotImplementedError("Calling generic __write_report_file__ method")


    def __get_filename_from_url__(self, article_info):
        """Get filename from article image url

        Args:
            article_info (str): article info dict

        Returns:
            str: the image filename
        """
        try:
            if article_info["picture_url"] != None:

                picture_url_parse = urlparse(article_info["picture_url"])
                picture_filename = os.path.basename(picture_url_parse.path)

                article_info["picture_filename"] = picture_filename
        except Exception as ex:
            print_debug_log(f"Error when getting filename from url: {ex}")
        finally:
            return article_info
    
    def __download_picture__(self, article_info):
        """Downloads a single image from article info

        Args:
            article_info (dict): a single article info

        Returns:
            bool: returns if the image was downloaded successfully
        """

        if article_info["picture_url"] == None:
            return True

        try:
            picture_url = article_info["picture_url"]
            picture_filename = article_info["picture_filename"]

            response = requests.get(picture_url)

            with open(f"{self.__OUTPUT_FOLDER__}/{picture_filename}", "wb") as f:
                f.write(response.content)

            return True
        except Exception as ex:
            print_debug_log(f"Error when downloading image {picture_filename}: {ex}")

            return False
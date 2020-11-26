from BackEnd.functions.dataretrieval import Scraper
import re
import os
from pathlib import Path


def create_text_file_from_html(url, file_path):
    re_url = re.compile(r"https?://(www\.)?")
    short_url = re_url.sub('', url).strip().strip('/')
    file_name = re.sub('[/.]', '_', short_url)[:15]

    file = os.path.join(file_path, file_name + ".txt")
    if not os.path.exists(file):
        scraper = Scraper()
        data = scraper.get_data_from_source(url)

        with open(file, "w", encoding="utf-8") as f:
            f.write(data.url + "\n")
            f.write(data.title + "\n")
            f.write(data.text_body + "\n")
        print(f"Successfully created \"{file}\"")
    else:
        print(f"WARNING: File \"{file}\" already exists")


if __name__ == "__main__":
    subject_sources = ["Vaccine_sources.txt"]

    for subject_source in subject_sources:
        sources_file = os.path.join("Testing_Data", subject_source)
        sources = open(sources_file, "r")

        subject = subject_source.split('_')[0]
        folder_for = os.path.join("Testing_Data", subject, "For")
        folder_against = os.path.join("Testing_Data", subject, "Against")

        if not os.path.exists(folder_for):
            os.makedirs(folder_for)

        if not os.path.exists(folder_against):
            os.makedirs(folder_against)

        against_sources = []
        for_sources = []
        for source in sources:
            source_split = source.split(',')
            if source_split[0] == 'a':
                against_sources.append(source_split[1])
            elif source_split[0] == 'f':
                for_sources.append(source_split[1])
            else:
                print(f"UNKNOWN source type: \'{source_split[0]}'")
        sources.close()

        for source in for_sources:
            create_text_file_from_html(source.strip(), folder_for)

        for source in against_sources:
            create_text_file_from_html(source.strip(), folder_against)

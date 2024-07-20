import openpyxl
import requests
import os

# Load the Excel file
excel_path = './AMQDB.xlsx'
wb = openpyxl.load_workbook(excel_path)
sheet = wb['All']

# Ensure the directory to save files exists
save_directory = 'downloaded_webm_files'
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# Function to download a file
def download_file(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {url}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")

# Iterate through the rows and download the .webm files
for row in sheet.iter_rows(min_row=2):  # assuming the first row is the header
    anime_name = row[1].value  # Column B
    song_type = row[2].value  # Column C
    song_info = row[3]  # Column D with hyperlink

    if song_info.hyperlink and song_info.hyperlink.target.endswith('.webm'):
        url = song_info.hyperlink.target
        file_name = f"{anime_name} {song_type} - {song_info.value}.webm"
        # Remove any characters from the file name that are invalid in a file system
        file_name = "".join([c if c.isalnum() or c in " .-_()" else "_" for c in file_name])
        save_path = os.path.join(save_directory, file_name)

        if os.path.exists(save_path):
            print(f"Already downloaded: {file_name}")
        else:
            download_file(url, save_path)

print("Download completed.")

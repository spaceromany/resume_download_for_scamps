import requests
from tqdm import tqdm
import os

# Set the download URL and the save path
url = "https://hueaml.blob.core.windows.net/scampsdatasetrelease/scamps_videos.tar.gz"
save_path = "/HDD/SCAMPS/scamps_videos.tar.gz"

# Set the maximum number of retries
max_retries = 3

# Open the local file in append mode
with open(save_path, "ab") as f:
    # Get the size of the local file
    local_file_size = os.path.getsize(save_path)

    # Send an HTTP GET request to the URL
    response = requests.get(url, stream=True)

    # Get the total size of the file
    file_size = int(response.headers.get("Content-Length"))

    # Check if the size of the local file is smaller than the size of the file
    if local_file_size < file_size:
        # Initialize the number of retries
        retries = 0

        # Retry the request if the connection fails
        while True:
            # Set the starting and ending bytes for the request
            start_byte = local_file_size
            end_byte = file_size - 1

            # Set the HTTP Range header to download the specified range of bytes
            headers = {"Range": f"bytes={start_byte}-{end_byte}"}

            try:
                # Send the HTTP GET request
                response = requests.get(url, headers=headers, stream=True)
                break
            except:
                # Increment the number of retries
                retries += 1

                # If the number of retries is greater than the maximum, raise an exception
                if retries > max_retries:
                    raise Exception("Failed to download file after maximum number of retries")

        # Use tqdm to show the progress bar
        for data in tqdm(response.iter_content(chunk_size=4096), total=file_size, initial=local_file_size, unit="B", unit_scale=True, desc=save_path):
            # Write the data to the local file
            f.write(data)
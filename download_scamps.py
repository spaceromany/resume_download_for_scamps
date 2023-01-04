import urllib.request
import os

# Set the download URL and the save path
url = "https://hueaml.blob.core.windows.net/scampsdatasetrelease/scamps_videos.tar.gz"
save_path = "/HDD/SCAMPS/scamps_videos.tar.gz"

# Set the number of bytes to download per iteration (e.g. 4MB)
bytes_per_iteration = 4 * 1024 * 1024

# Open the URL and get the size of the file
response = urllib.request.urlopen(url)
file_size = int(response.info().get("Content-Length"))

# Check if the local file exists
if os.path.exists(save_path):
    # Open the local file in append mode
    with open(save_path, "ab") as f:
        # Get the size of the local file
        local_file_size = os.path.getsize(save_path)

        # Check if the size of the local file is smaller than the size of the file
        if local_file_size < file_size:
            # Calculate the number of bytes to download
            bytes_to_download = file_size - local_file_size

            # Calculate the number of iterations required to download the remaining bytes
            iterations = int(bytes_to_download / bytes_per_iteration) + 1

            # Set the starting and ending bytes for each iteration
            for i in range(iterations):
                start_byte = local_file_size + i * bytes_per_iteration
                end_byte = min(local_file_size + (i + 1) * bytes_per_iteration - 1, file_size - 1)

                # Set the HTTP Range header to download the specified range of bytes
                headers = {"Range": f"bytes={start_byte}-{end_byte}"}
                request = urllib.request.Request(url, headers=headers)

                # Read the data in the specified range
                data = urllib.request.urlopen(request).read()

                # Write the data to the local file
                f.write(data)
else:
    # If the local file doesn't exist, download the entire file
    urllib.request.urlretrieve(url, save_path)
import os
import requests

# Your 3 API tokens
API_TOKENS = [
    '1lQraGqc7ZGecDsDKGOzM7uygb8kiRyx',
    '1lQraGqc7ZGecDsDKGOzM7uygb8kiRyx',
    '1lQraGqc7ZGecDsDKGOzM7uygb8kiRyx'
]

# Your existing folder IDs for each account
FOLDER_IDS = [
    '3a3d183b-231d-4469-a7e2-47fb19a9fe18',  # Replace with your folder ID for account 1
    '392aa4ba-3a7d-41de-afa8-8882d97e8204',  # Replace with your folder ID for account 2
    '438d5927-dba3-484a-a4cb-0741d0d3e075'   # Replace with your folder ID for account 3
]

# Path to your local folder containing files
LOCAL_FOLDER = 'downloads/'  # Replace with your local folder path

def gather_files(local_path):
    files_list = []
    for root, dirs, files in os.walk(local_path):
        for file in files:
            files_list.append(os.path.join(root, file))
    return sorted(files_list, key=lambda x: os.path.basename(x).lower())

def upload_file(api_token, folder_id, file_path):
    headers = {'Authorization': f'Bearer {api_token}'}
    url = 'https://upload.gofile.io/uploadfile'
    with open(file_path, 'rb') as f:
        files = {'file': (os.path.basename(file_path), f)}
        data = {'folderId': folder_id}
        try:
            response = requests.post(url, files=files, data=data, headers=headers)
            response.raise_for_status()
            result = response.json()
            if result['status'] == 'ok':
                print(f"Uploaded {os.path.basename(file_path)}")
            else:
                print(f"Failed to upload {os.path.basename(file_path)}: {result}")
        except Exception as e:
            print(f"Error uploading {os.path.basename(file_path)}: {e}")

def main():
    all_files = gather_files(LOCAL_FOLDER)

    # Sort files alphabetically (by filename)
    all_files.sort(key=lambda x: os.path.basename(x).lower())

    total_files = len(all_files)
    group_size = total_files // 3
    # Distribute remaining files to the last group
    groups = [
        all_files[0:group_size],
        all_files[group_size:2*group_size],
        all_files[2*group_size:]
    ]

    # Upload each group into your specified folder IDs
    for i in range(3):
        print(f"\nUploading files to folder ID {FOLDER_IDS[i]} (Account ending {API_TOKENS[i][-4:]})")
        for file_path in groups[i]:
            upload_file(API_TOKENS[i], FOLDER_IDS[i], file_path)

if __name__ == '__main__':
    main()
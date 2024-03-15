from pytube import YouTube
import os

video_directory = "public/youtube_video"

def prepare_directory(directory):
    # print("Checking if directory exists")
    if not os.path.exists(directory):
        # print("Creating directory")
        os.makedirs(directory)
    else:
        # print("Directory already exists, deleting existing files")
        files = os.listdir(directory)
        for file in files:
            file_path = os.path.join(directory, file)
            os.remove(file_path)
            # print(f"Deleted file: {file_path}")

    # print("Navigating to directory")
    os.chdir(directory)

def download(link):
    try:
        youtube_object = YouTube(link)
    except:
        print("Invalid link")
        return False
    
    try:
        # print("Preparing directory")
        prepare_directory(video_directory)

        # print("Getting high quality video")
        youtube_object = youtube_object.streams.get_highest_resolution()
        # print("Downloading video")
        video_path = youtube_object.download()
        # print("Video download complete")
    except Exception as e:
        print(f"Something went wrong while downloading the youtube video: {e}")
        return False

    return True, video_path

if __name__  == "__main__":
    link = input("Enter a youtube link: ")
    download(link)

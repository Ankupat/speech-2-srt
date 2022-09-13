# speech-2-srt
The scripts converts video to mp3 audio and converts it to SRT subtitles using Google TTS engine.

# Pre-requisites
Install all the dependancy from the requirements.txt. The code is compatible with python3 onwards.
```code
python3 -m pip install -r requirements.txt
```

# Usage
```code
video2srt.py [-h] [--storage_uri STORAGE_URI] [--language_code LANGUAGE_CODE] [--sample_rate_hertz SAMPLE_RATE_HERTZ] [--max_chars MAX_CHARS] [--encoding ENCODING] [--audio_channel_count AUDIO_CHANNEL_COUNT] [--base_path BASE_PATH] [--file_name FILE_NAME]

options:

  -h, --help			show this help message and exit
  --storage_uri			STORAGE_URI (If file already in the google cloud storage)
  --language_code		LANGUAGE_CODE (default: gu-IN)
  --sample_rate_hertz		SAMPLE_RATE_HERTZ (default: 16000)
  --max_chars			MAX_CHARS (default: 40)
  --encoding			ENCODING (default: ENCODING_UNSPECIFIED)
  --audio_channel_count		AUDIO_CHANNEL_COUNT (default: 1)
  --base_path			BASE_PATH
  --file_name			FILE_NAME
  ```
 # Example
 #### usecase 1: If you want to create the SRT subs from video
 ```code
 python3 video2srt.py --base_path="/Users/abc/Documents/github/speech-2-srt/test_content/" --file_name="test.mp4"
 ```
 
 #### usecase 2: If you already have audio file (mp3) in the google cloud storage
 ```code
 python3 video2srt.py --storage_uri="gs://test/test.mp3"
 ```

# Notes
  - Change the Google Cloud Folder path as required in the script.
  - The file base path can be hardcoded as default in the script to avoid defining at the command line.
  - The SRT and TXT files will be store at the same base path.

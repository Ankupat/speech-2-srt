# speech-2-srt
The scripts converts video to mp3 audio and converts it to SRT subtitles using Google TTS engine.

# Pre-requisites
Install all the dependancy from the requirements.txt

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

# Notes
  - Change the Google Cloud Folder path as required in the script

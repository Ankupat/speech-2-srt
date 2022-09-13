# -*- coding: utf-8 -*-
from moviepy.editor import *
from gcloud import storage
from google.cloud import speech
import srt


def mp4_to_mp3(args):
    # MP4 to MP3 Conversion
    print(
        "-------------------------- Converting the Video File to Audio (MP3) --------------------------"
    )
    audio_filename = args.file_name.split(".")[0] + ".mp3"
    video = VideoFileClip(f"{args.base_path}{args.file_name}")
    video.audio.write_audiofile(f"{args.base_path}{audio_filename}")
    file_path = f"{args.base_path}{audio_filename}"
    return file_path


def upload_to_cloud(file_path):
    """
    saves a file in the google storage. As Google requires audio files greater than 60 seconds to be saved on cloud before processing
    It always saves in 'akdm' (folder)
    Input:
        Path of file to be saved
    Output:
        URI of the saved file
    """
    print(
        "-------------------------- Upload Audio (MP3) file to Google Cloud Storage --------------------------"
    )
    print("Uploading to cloud...")
    client = storage.Client()
    bucket = client.get_bucket("akdm")
    file_name = str(file_path).split("/")[-1]
    blob = bucket.blob(file_name)

    ## For slow upload speed
    storage.blob._DEFAULT_CHUNKSIZE = 2097152  # 1024 * 1024 B * 2 = 2 MB
    storage.blob._MAX_MULTIPART_SIZE = 2097152  # 2 MB

    with open(file_path, "rb") as f:
        blob.upload_from_file(f)
    print("uploaded at: ", "gs://akdm/{}".format(file_name))
    return "gs://akdm/{}".format(file_name)


def long_running_recognize(args):
    """
    Transcribe long audio file from Cloud Storage using asynchronous speech
    recognition
    """
    print(
        "-------------------------- Transcribing the Audio (MP3) --------------------------"
    )
    print("Transcribing {} ...".format(args.storage_uri))
    client = speech.SpeechClient()

    # Encoding of audio data sent.
    operation = client.long_running_recognize(
        config={
            "enable_word_time_offsets": True,
            "enable_automatic_punctuation": True,
            "sample_rate_hertz": args.sample_rate_hertz,
            "language_code": args.language_code,
            "audio_channel_count": args.audio_channel_count,
            "encoding": args.encoding,
        },
        audio={"uri": args.storage_uri},
    )
    response = operation.result()

    subs = []

    for result in response.results:
        # First alternative is the most probable result
        subs = break_sentences(args, subs, result.alternatives[0])

    print("Transcribing finished")
    return subs


def break_sentences(args, subs, alternative):
    firstword = True
    charcount = 0
    idx = len(subs) + 1
    content = ""
    word_count = len(alternative.words) - 1
    for index, w in enumerate(alternative.words):
        if firstword:
            # first word in sentence, record start time
            start = w.start_time

        charcount += len(w.word)
        content += " " + w.word.strip()

        if (
            "." in w.word
            or "!" in w.word
            or "?" in w.word
            or charcount > args.max_chars
            or index == word_count
            or ("," in w.word and not firstword)
        ):
            # break sentence at: . ! ? or line length exceeded
            # also break if , and not first word

            subs.append(
                srt.Subtitle(
                    index=idx,
                    start=start,
                    end=w.end_time,
                    content=srt.make_legal_content(content),
                )
            )
            firstword = True
            idx += 1
            content = ""
            charcount = 0
        else:
            firstword = False
    return subs


def write_srt(args, subs):
    print("-------------------------- Create SRT File --------------------------")
    srt_file = args.storage_uri.split("/")[-1].split(".")[0] + ".srt"
    print("Writing {} subtitles to: {}".format(args.language_code, srt_file))
    f = open(srt_file, "w")
    f.writelines(srt.compose(subs))
    f.close()
    return


def write_txt(args, subs):
    print("-------------------------- Create TXT File --------------------------")
    txt_file = args.storage_uri.split("/")[-1].split(".")[0] + ".txt"
    print("Writing text to: {}".format(txt_file))
    f = open(txt_file, "w")
    for s in subs:
        f.write(s.content.strip() + "\n")
    f.close()
    return


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--storage_uri",
        type=str,
    )
    parser.add_argument(
        "--language_code",
        type=str,
        default="gu-IN",
    )
    parser.add_argument(
        "--sample_rate_hertz",
        type=int,
        default=16000,
    )
    parser.add_argument(
        "--max_chars",
        type=int,
        default=40,
    )
    parser.add_argument("--encoding", type=str, default="ENCODING_UNSPECIFIED")
    parser.add_argument("--audio_channel_count", type=int, default=1)
    parser.add_argument(
        "--base_path",
        type=str,
    )
    parser.add_argument(
        "--file_name",
        type=str,
    )
    args = parser.parse_args()
    if not args.storage_uri:
        file_path = mp4_to_mp3(args)
        storage_uri = upload_to_cloud(file_path)
        args.storage_uri = storage_uri

    subs = long_running_recognize(args)
    write_srt(args, subs)
    write_txt(args, subs)


if __name__ == "__main__":
    main()

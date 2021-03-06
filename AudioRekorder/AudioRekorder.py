import time

import argparse
import requests

parser = argparse.ArgumentParser('Just a test')
parser.add_argument('-url', '-u', default="http://stream.electroradio.fm/192k")
parser.add_argument('--fileName', '-f', required=True)
parser.add_argument('--duration', '-d', type=int, default=30)
arg = parser.parse_args()
print(arg.url, arg.duration, arg.fileName)

default_file_name = time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".mp3"


def record_audio(path=arg.fileName, stream_url=arg.url, time_limit=arg.duration):
    print("Recording audio...")
    filename = path
    m_file = open(filename, 'wb')
    chunk_size = 1024

    start_time_in_seconds = time.time()

    time_limit = time_limit - 11 if time_limit > 11 else 1
    time_elapsed = 0
    url = stream_url
    with requests.Session() as session:
        response = session.get(url, stream=True)
        for chunk in response.iter_content(chunk_size=chunk_size):
            if time_elapsed > time_limit:
                break
            # to print time elapsed
            if int(time.time() - start_time_in_seconds) - time_elapsed > 0:
                time_elapsed = int(time.time() - start_time_in_seconds)
                print(time_elapsed, end='\r', flush=True)
            if chunk:
                m_file.write(chunk)

        m_file.close()


if arg:
    record_audio()
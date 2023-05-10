import os
import sys
import subprocess

def read_timestamps_and_titles(timestamp_file):
    with open(timestamp_file, 'r') as f:
        lines = f.readlines()
    timestamps_and_titles = [line.strip().split(' ', 1) for line in lines]
    return timestamps_and_titles

def play_video_at_timestamp(video_file, timestamp):
    command = f'mpv --start={timestamp} --pause {video_file} > mpv.stdout'
    #print(command)
    process = subprocess.Popen(command, shell=True)
    process.wait()
    return process.returncode

def create_video_snippet(video_file, start_time, end_time, output_dir, title):
    start_time_parts = start_time.split(":")
    start_time_seconds = sum(float(x) * 60 ** (len(start_time_parts) - 1 - i) for i, x in enumerate(start_time_parts))

    end_time_parts = end_time.split(":")
    end_time_seconds = sum(float(x) * 60 ** (len(end_time_parts) - 1 - i) for i, x in enumerate(end_time_parts))

    duration = end_time_seconds - start_time_seconds

    title = title.replace(" ", "_")
    output_file = os.path.join(output_dir, f'{start_time}_{title}.mp4')
    command = f'ffmpeg -ss {start_time_seconds} -i {video_file} -t {duration} -c copy "{output_file}"'
    subprocess.call(command, shell=True)


def main(timestamp_file, video_file):
    timestamps_and_titles = read_timestamps_and_titles(timestamp_file)
    output_dir = f'output/{timestamp_file}'
    os.makedirs(output_dir, exist_ok=True)

    for i, (timestamp, title) in enumerate(timestamps_and_titles):
        print(f'\n \n Playing video at timestamp: {timestamp}')
        print(f'Titel {title}')
        play_video_at_timestamp(video_file, timestamp)

        end_time = input('Enter the end time (HH:MM:SS) where the video was stopped: ')
        if end_time is "":
            continue
        create_video_snippet(video_file, timestamp, end_time, output_dir, title)
        print(f'Created snippet "{title}" from {timestamp} to {end_time}')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <timestamp_file> <video_file>")
        sys.exit(1)

    timestamp_file = sys.argv[1]
    video_file = sys.argv[2]

    main(timestamp_file, video_file)



import os
import time
import cv2
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class VideoHandler(FileSystemEventHandler):
    def __init__(self, processed_files):
        self.processed_files = processed_files

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
            if event.src_path not in self.processed_files:
                self.process_video(event.src_path)

    def convert_video(self, input_path, output_path):
        command = [
            'ffmpeg',
            '-i', input_path,
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '128k',
            output_path
        ]
        subprocess.run(command, check=True)

    def process_video(self, video_path):
        try:
            video_name = os.path.splitext(os.path.basename(video_path))[0]
            video_dir = os.path.dirname(video_path)
            output_directory = os.path.join(video_dir, "frames")
            os.makedirs(output_directory, exist_ok=True)

            converted_path = os.path.join(output_directory, f"{video_name}_converted.mp4")
            self.convert_video(video_path, converted_path)

            video = cv2.VideoCapture(converted_path)
            if not video.isOpened():
                print(f"Error: Could not open converted video file {converted_path}.")
                return

            fps = int(video.get(cv2.CAP_PROP_FPS))
            frame_count = 0

            while True:
                ret, frame = video.read()
                if not ret:
                    break

                if frame_count % fps == 0:
                    frame_path = os.path.join(output_directory, f"{video_name}_frame_{frame_count // fps:04d}.jpg")
                    cv2.imwrite(frame_path, frame)

                frame_count += 1

            video.release()
            print(f"Processed {video_path}. Frames saved in {output_directory}.")

            os.remove(converted_path)
            self.processed_files.add(video_path)

        except subprocess.CalledProcessError as e:
            print(f"Error during video conversion: {e}")
        except cv2.error as e:
            print(f"OpenCV error occurred while processing {video_path}: {e}")
        except Exception as e:
            print(f"An error occurred while processing the video {video_path}: {e}")

def process_existing_files(directory, processed_files):
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path) and file_name.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
            if file_path not in processed_files:
                handler.process_video(file_path)

if __name__ == "__main__":
    print("Video Frame Extractor")
    watch_dir = input("Enter the directory to watch: ")
    os.makedirs(watch_dir, exist_ok=True)

    processed_files = set()
    handler = VideoHandler(processed_files)
    process_existing_files(watch_dir, processed_files)

    observer = Observer()
    observer.schedule(handler, watch_dir, recursive=False)
    observer.start()

    print(f"Watching directory: {watch_dir}")
    print("Press Ctrl+C to stop...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
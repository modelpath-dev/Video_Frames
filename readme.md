# Video Frame Extractor

## Description

This Python script monitors a specified directory for new video files and automatically extracts frames from them. It uses FFmpeg to convert videos to a compatible format and OpenCV to process the videos and extract frames.

## Features

- Watches a specified directory for new video files
- Supports .mp4, .mov, .avi, and .mkv video formats
- Converts videos to a format compatible with OpenCV using FFmpeg
- Extracts one frame per second from each video
- Saves extracted frames as JPEG images
- Cleans up temporary converted videos to save disk space

## Requirements

- Python 3.6+
- OpenCV (`cv2`)
- FFmpeg
- Watchdog

## Installation

1. Clone this repository or download the script.
2. Install the required Python packages:

3. Ensure FFmpeg is installed on your system and accessible from the command line.

## Usage

1. Run the script:

2. When prompted, enter the full path of the directory you want to monitor.
3. The script will start watching the specified directory. Any new video files added to this directory will be automatically processed.
4. Press Ctrl+C to stop the script.

## Output

For each video processed, the script will:
1. Create a new directory named after the video file.
2. Save extracted frames as JPEG images in this directory.
3. Name the frames as `frame_XXXX.jpg`, where XXXX is the frame number.

## Error Handling

The script includes error handling for:
- Video conversion errors
- OpenCV processing errors
- General exceptions

Any errors encountered during processing will be printed to the console.

## Notes

- Ensure you have sufficient disk space, as video processing can generate large amounts of data.
- The script currently extracts one frame per second. You can modify this by changing the condition in the frame extraction loop.





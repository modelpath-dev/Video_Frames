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


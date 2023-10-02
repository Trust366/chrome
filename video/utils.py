import os
import subprocess
import uuid
import numpy as np
import cv2

from django.conf import settings

from video.models import RecordingSession, RecordingChunk


def generate_unique_id():
    new_id = str(uuid.uuid4())
    try:
        # Check if the ID already exists
        RecordingSession.objects.get(recording_id=new_id)
        # If yes, try again
        return generate_unique_id()
    except RecordingSession.DoesNotExist:
        # If no, return the ID
        return new_id


def get_chunk_dir(recording_id):
    return os.path.join(settings.MEDIA_ROOT, 'recording_chunks', recording_id)


def combine_chunks(recording_id):
    chunks = RecordingChunk.objects.filter(session__recording_id=recording_id).order_by('order')
    if not chunks:
        return None

    # Get the latest chunk to determine the MIME type
    latest_chunk = chunks.last()
    if not latest_chunk:
        return None

    mime_type = latest_chunk.session.mime_type

    # Define the output video path
    output_path = os.path.join(get_chunk_dir(recording_id), 'combined_video.mp4')

    # Call the combine_chunks_to_video function
    combine_chunks_to_video(get_chunk_dir(recording_id), output_path)

    return output_path


def combine_chunks_to_video(chunk_dir, output_video_path):
    # Get a list of chunk files in the directory
    chunk_files = sorted([os.path.join(chunk_dir, file) for file in os.listdir(chunk_dir)])

    # Initialize an empty list to store chunk data
    chunk_data = []

    for chunk_file in chunk_files:
        with open(chunk_file, 'rb') as file:
            chunk_data.append(file.read())

    # Combine the binary chunks into a single byte stream
    video_data = b''.join(chunk_data)

    # Define video properties (e.g., frame width, height, frame rate)
    frame_width = 640  # Replace with your frame width
    frame_height = 480  # Replace with your frame height
    frame_rate = 30  # Replace with your desired frame rate

    # Create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, frame_rate, (frame_width, frame_height))

    # Initialize variables for tracking frame position
    frame_pos = 0

    # Read frames from the video data and write them to the output video
    while frame_pos < len(video_data):
        frame_size = frame_width * frame_height * 3  # Assuming 3 channels (e.g., RGB)
        frame_data = video_data[frame_pos:frame_pos + frame_size]
        if len(frame_data) != frame_size:
            break  # Reached the end of video data

        # Reshape frame data and write it to the video
        frame = np.frombuffer(frame_data, dtype=np.uint8).reshape(frame_height, frame_width, 3)
        out.write(frame)
        frame_pos += frame_size

    # Release the VideoWriter and close the video file
    out.release()

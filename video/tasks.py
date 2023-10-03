import time
import openai
from .models import RecordingSession
from .utils import combine_chunks
from celery import shared_task

@shared_task
def transcribe_video(recording_id):
    try:
        recording_session = RecordingSession.objects.get(recording_id=recording_id)
    except RecordingSession.DoesNotExist:
        return

    # Simulate transcription process
    video_file = combine_chunks(recording_id)
    
    # Assuming 'whisper-1' is a valid model ID for OpenAI transcription
    transcript = openai.Audio.transcribe('whisper-1', open(video_file, 'rb'))
    time.sleep(10)  # Simulate a 10-second transcription

    # Update the recording session with the transcription result
    recording_session.metadata = transcript.get('text', '')
    recording_session.status = 'completed'
    recording_session.save()

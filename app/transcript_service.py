
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound

import traceback


def fetch_transcript(video_id: str, ytt_api: YouTubeTranscriptApi):
    print(f"Fetching transcript for video ID: {video_id}")
    try:
       
        transcript =  ytt_api.fetch(video_id, languages=['en']).snippets
        return {"transcript": transcript, "message": "Success"}
    
    except NoTranscriptFound:
        try:
            transcript_list = list(ytt_api.list_transcripts(video_id))
            print(f"Available transcripts: {[str(t) for t in transcript_list]}")

            auto_en = next(
                (trans for trans in transcript_list if trans.is_generated and trans.language_code == 'en'),
                None
            )
            if auto_en:
                print("Auto-generated English transcript found.")
                return {"transcript": auto_en.fetch().snippets, "message": "Auto-generated English transcript"}

            for transcript in transcript_list:
                try:
                    if transcript.is_translatable:
                        print(f"Checking translatable transcript: {transcript.language}")
                        # print(  transcript.translation_languages)
                        translation_languages = transcript.translation_languages
                        language_codes = [lang.language_code for lang in translation_languages]


                        if 'en' in language_codes:
                            translated = transcript.translate('en').fetch().snippets
                            print(f"Successfully translated transcript from {transcript.language} to English.")
                            return {
                                "transcript": translated,
                                "message": f"Translated from {transcript.language}"
                            }
                except Exception as e:
                    print(f"Translation attempt failed: {e}")
                    continue


            first_available = transcript_list[0]
            print(f"Falling back to first available transcript: {first_available.language}")
            return {
                "transcript": first_available.fetch().snippets,
                "message": f"Fallback to first available: {first_available.language}"
            }

        except Exception as e:
            print("Transcript fallback failed:")
            traceback.print_exc()
            return {"transcript": [], "message": "No transcript available"}
    
    except Exception as e:
        print("Unexpected error occurred:")
        traceback.print_exc()
        return {"transcript": [], "message": "Something went wrong"}

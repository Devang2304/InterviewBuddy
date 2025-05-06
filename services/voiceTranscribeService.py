from faster_whisper import WhisperModel


class voiceTranscribeService:
    def __init__(self, model_size="tiny.en"):
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")

    def transcribe(self, audio) -> str:
        segments, info = self.model.transcribe(audio, beam_size=5)
        print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
        transcribedText = ""
        for segment in segments:
            transcribedText += segment.text + " "
            print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        return transcribedText.strip()
    


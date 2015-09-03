import pyaudio
import speech_recognition as sr


languages = {"italian" : "it-IT",
             "english" : "en-US",
             "japanese" : "ja"}


class Audiotron:

    def __init__(self, language=languages["english"]):
        self.recon = sr.Recognizer()
        self.language = language

    def calibrate(self):
        with sr.Microphone() as source:
            self.recon.adjust_for_ambient_noise(source)

    def acquire(self):
        with sr.Microphone() as source:
            audio = self.recon.listen(source)
        try:
            return str(self.recon.recognize_google(audio, language=self.language))
        except LookupError:
            return None
        except sr.UnknownValueError:
            return None


def test():
    r = sr.Recognizer()
    with sr.Microphone() as source:                # use the default microphone as the audio source
        print("calibrating")
        r.adjust_for_ambient_noise(source)         # listen for 1 second to calibrate the energy threshold for ambient noise levels
        print("Say something")
        audio = r.listen(source)                   # now when we listen, the energy threshold is already set to a good value, and we can reliably catch speech right away
        print("Elaborazione")
    try:
        print("You said " + str(r.recognize_google(audio)))    # recognize speech using Google Speech Recognition
    except LookupError:                            # speech is unintelligible
        print("Could not understand audio")
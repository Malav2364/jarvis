import speech_recognition as sr
import wikipedia
import pyttsx3
import sys

def search_wikipedia():
    """Searches for a given topic in Wikipedia and prints/speaks the summary."""
    
    # Initialize speech recognition
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak into the microphone:")
        audio_data = recognizer.listen(source, timeout=5)  # Set the timeout to 5 seconds

    try:
        query = recognizer.recognize_google(audio_data)
        print("You said:", query)
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return

    try:
        # Get the summary from Wikipedia
        summary = wikipedia.summary(query)

        # Split the summary into lines and print only the first 10 lines
        summary_lines = summary.split('\n')
        limited_summary = '\n'.join(summary_lines[:1])
        print(limited_summary)

        # Initialize the text-to-speech engine
        engine = pyttsx3.init()

        # Get a list of available voices
        voices = engine.getProperty('voices')

        # Ask the user for the desired voice index
        voice_index = int(input("Enter the voice index (0 for default, 1 for first alternative, etc.): "))

        # Select the voice based on the user's input
        engine.setProperty('voice', voices[voice_index].id)

        # Increase the speaking rate (adjust the value as needed)
        engine.setProperty('rate', 200)

        # Speak the limited summary
        engine.say(limited_summary)
        engine.runAndWait()

        # Ask if the user is satisfied with the information
        satisfied = input("Are you satisfied with the information? (yes/no): ")
        if satisfied.lower() == "yes":
            print("Thank you for using the program.")
            sys.exit()  # Exit the program

    except wikipedia.exceptions.PageError:
        print("Sorry, I couldn't find anything about that topic on Wikipedia.")
    except wikipedia.exceptions.DisambiguationError as e:
        print("Did you mean one of these?")
        for option in e.options:
            print("- " + option)

if __name__ == "__main__":
    search_wikipedia()

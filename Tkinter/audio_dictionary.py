import requests
import pygame
import tkinter as tk
from tkinter import messagebox
import tempfile
import os


# Function to fetch word data from the Free Dictionary API
def get_word_data(word):
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to play pronunciation audio
def play_pronunciation(audio_url):
    try:
        # Send a GET request to the audio URL
        response = requests.get(audio_url)
        response.raise_for_status()  # Check for request errors

        # Create a temporary file to save the audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            temp_audio.write(response.content)
            temp_audio_path = temp_audio.name

        # Initialize pygame mixer
        pygame.mixer.init()
        pygame.mixer.music.load(temp_audio_path)
        pygame.mixer.music.play()

        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # Remove the temporary file after playback
        os.remove(temp_audio_path)

    except requests.RequestException as e:
        messagebox.showerror("Error", f"Unable to download audio: {e}")
    except pygame.error as e:
        messagebox.showerror("Error", f"Unable to play audio: {e}")


# Function to handle the search and display results
def search_word():
    word = entry.get().strip()
    if not word:
        messagebox.showwarning("Input Error", "Please enter a word to search.")
        return

    data = get_word_data(word)
    if data:
        try:
            definition = data[0]['meanings'][0]['definitions'][0]['definition']
            result_text.set(f"Definition of '{word}':\n{definition}")
            phonetics = data[0].get('phonetics', [])
            if phonetics:
                audio_url = phonetics[0].get('audio', '')
                if audio_url:
                    play_pronunciation(audio_url)
                else:
                    messagebox.showinfo("Audio Not Available", "Pronunciation audio not available for this word.")
            else:
                messagebox.showinfo("Phonetics Not Available", "Phonetic data not available for this word.")
        except (IndexError, KeyError) as e:
            messagebox.showerror("Data Error", f"Unexpected data format: {e}")
    else:
        messagebox.showerror("Word Not Found", f"No definition found for '{word}'.")

# Setting up the GUI
if __name__ == "__main__":
    app = tk.Tk()
    app.title("Personal Audio Dictionary")

# Word entry field
entry_label = tk.Label(app, text="Enter a word:")
entry_label.pack(pady=5)
entry = tk.Entry(app, width=50)
entry.pack(pady=5)
entry.bind("<Return>", lambda event: search_word())  # Bind Enter key to search

# Search button
search_button = tk.Button(app, text="Search", command=search_word)
search_button.pack(pady=5)

# Result display
result_text = tk.StringVar()
result_label = tk.Label(app, textvariable=result_text, wraplength=400, justify="left")
result_label.pack(pady=10)

def on_closing():
        pygame.mixer.quit()
        app.destroy()

app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()

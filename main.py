import base64
from openai import OpenAI
import tiktoken
from ebooklib import epub
from bs4 import BeautifulSoup
import os

api_key = "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"
# Define the chunk size in tokens
CHUNK_SIZE = 12000
 
client = OpenAI(api_key=api_key)
encoding = tiktoken.encoding_for_model("gpt-4o-audio-preview")

def extract_chapters_to_files(epub_path, output_dir="chapters"):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Load the EPUB file
    book = epub.read_epub(epub_path)

    # The book's spine defines the reading order
    spine = book.spine

    # Iterate through each item in the spine
    for index, (idref, _) in enumerate(spine, start=1):
        item = book.get_item_with_id(idref)
        if item and item.get_type() == epub.ITEM_DOCUMENT:
            # Get the HTML content of the chapter
            html_content = item.get_content()
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract the textual content
            text = soup.get_text(separator=' ', strip=True)
            
            # Determine a filename for the chapter
            chapter_filename = f"chapter_{index:02d}.txt"
            chapter_path = os.path.join(output_dir, chapter_filename)
            
            # Write the extracted text to a file
            with open(chapter_path, "w", encoding="utf-8") as outfile:
                outfile.write(text)

def audioBook(decoded_chunks):
 
 for i, chunk_text in enumerate(decoded_chunks):
  print(f"tiktoken {i} - {chunk_text}")

  response = client.chat.completions.create(
   model="gpt-4o-audio-preview",
   messages=[
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "Please produce an audiobook narration using a female voice with a professional Italian accent. Adopt a dynamic, natural, and contextually appropriate delivery. During narrative segments, maintain a calm, engaging tone. Differentiate character voices subtly in pitch and tempo. Convey emotions—tension, joy, sorrow—through changes in vocal intensity and pacing. Pause appropriately at punctuation, emphasize questions with a rising tone, and accentuate exclamations with slight volume increases. Keep diction crisp, ensure technical terms are pronounced accurately, and maintain consistent character voices throughout. No background noise should be present. Prior to final output, perform a test passage and adjust as needed for optimal clarity and believability."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": chunk_text}
       ]
     }
    ],
   modalities=["text", "audio"],
   audio={
    "voice": "alloy",
    "format": "wav"
   },
   temperature=1.1 )
  
  print(f"response TTS {i} - {response.choices[0]}")

  # Salva il file audio in formato mp3
  with open(f"output_{i}.mp3", "wb") as f:
      f.write(base64.b64decode(response.choices[0].message.audio.data))

def text_to_cunck(text):
  # Encode the entire text into tokens
 tokens = encoding.encode(text)

 # Split tokens into chunks of 12,000 tokens
 chunks = [tokens[i:i+CHUNK_SIZE] for i in range(0, len(tokens), CHUNK_SIZE)]

 # Decode each chunk back into text strings
 decoded_chunks = [encoding.decode(chunk) for chunk in chunks]

 return decoded_chunks;

if __name__ == "__main__":
    # Percorso al file epub di input
  epub_BASE_FOLDER = os.path.join(os.getcwd(), "epub")
  epub_path = os.path.join(epub_BASE_FOLDER, "Incastrati_John Grisham.epub")
  
  extract_chapters_to_files(epub_path)

  '''with open(file_path, 'r', encoding='utf-8') as f:
   tts_text = f.read() 

  decoded_chunks = text_to_cunck(tts_text) 
  
    # Conversione da testo ad audio
  audioBook(file_path)'''

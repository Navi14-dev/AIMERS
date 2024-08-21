import torch
from transformers import ViltProcessor, ViltForQuestionAnswering
from PIL import Image
import tkinter as tk
from tkinter import filedialog

# Initialize the processor and model
processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")

# Function to open an image file using a file dialog
def open_image():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

# Function to ask a question about the image and get the answer
def ask_question(image_path, question):
    image = Image.open(image_path)
    # Process the image and question
    inputs = processor(image, question, return_tensors="pt")

    # Get the answer from the model
    with torch.no_grad():
        outputs = model(**inputs)
        answer = processor.decode(outputs.logits.argmax(-1))

    return answer

def main():
    # Load image
    image_path = open_image()
    if not image_path:
        print("No image selected.")
        return

    # Ask a question
    question = input("Ask a question about the image: ")

    # Get the answer
    answer = ask_question(image_path, question)

    # Print the result
    print(f"Answer: {answer}")

if __name__ == "__main__":
    main()
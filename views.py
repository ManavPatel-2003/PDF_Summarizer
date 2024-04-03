from django.shortcuts import render
from PyPDF2 import PdfReader
import openai
from dotenv import load_dotenv
import os

load_dotenv()

# Create your views here.
def home(request):
    return render(request, 'home.html')

def process(request):
    if(request.method=='POST'): 
        openai.api_key = os.environ.get('OPENAI_API_KEY')


        file = request.FILES['file1']
        # creating a pdf reader object
        reader = PdfReader(file)

        # printing number of pages in pdf file
        length = len(reader.pages)

        # getting a specific page from the pdf file
        data = ''
        for i in range(length):
            page = reader.pages[i]
            data += page.extract_text()

        # extracting text from page
        # text = page.extract_text()
        response = openai.ChatCompletion.create(
            model = 'gpt-3.5-turbo',
            messages = [{'role':'system', 'content':"Act as humble, student friendly professional teacher or professor"},
                        {'role':'user', 'content': data},
                        {'role':'user', 'content':"Please summarize this text for me."}]
        )

        explanation = response['choices'][0]['message']['content']
        print(explanation)
        return render(request, 'home.html', {'page':length, 'data':explanation})
    else:
        return render(request, 'home.html')
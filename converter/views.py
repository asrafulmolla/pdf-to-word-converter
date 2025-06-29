from django.shortcuts import render

# Create your views here.
import os
from django.shortcuts import render
from django.conf import settings
from django.http import FileResponse
from pdf2docx import Converter

def index(request):
    context = {}
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)
        pdf_file = request.FILES['pdf_file']
        input_path = os.path.join(settings.MEDIA_ROOT, pdf_file.name)
        output_name = pdf_file.name.replace('.pdf', '.docx')
        output_path = os.path.join(settings.MEDIA_ROOT, output_name)

        with open(input_path, 'wb+') as dest:
            for chunk in pdf_file.chunks():
                dest.write(chunk)

        cv = Converter(input_path)
        cv.convert(output_path)
        cv.close()

        context['converted_file_url'] = settings.MEDIA_URL + output_name

    return render(request, 'converter/index.html', context)
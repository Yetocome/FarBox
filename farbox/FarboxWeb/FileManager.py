
def handle_upload_file(f):
    with open('upload_file.doc', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

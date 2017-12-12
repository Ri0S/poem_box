import urllib.request


def T2M(sample_path):
    f = open(sample_path, 'rb')
    txt = f.read().decode('utf-8')

    client_id = "94znWx8FitYh6ePv8pFy"
    client_secret = "BGrgkIj8iZ"

    encText = urllib.parse.quote(txt)

    data = "speaker=jinho&speed=-1&text=" + encText;
    url = "https://openapi.naver.com/v1/voice/tts.bin"

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)

    response = urllib.request.urlopen(request, data=data.encode('utf-8'))
    rescode = response.getcode()

    if rescode == 200:
        print("TTS mp3 저장")
        response_body = response.read()
        with open('sample.mp3', 'wb') as f:
            f.write(response_body)
        return True
    else:
        print("Error Code:" + rescode)
        return False

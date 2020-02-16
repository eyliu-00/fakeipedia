from starlette.applications import Starlette
from starlette.responses import UJSONResponse
import gpt_2_simple as gpt2
import tensorflow as tf
import uvicorn
import os
import gc
import base64

from fakeipedia import *

app = Starlette(debug=False)

generator = Text_Generator()
completer = Text_Generator(model_name = "124M")

# Needed to avoid cross-domain issues
response_header = {
    'Access-Control-Allow-Origin': '*'
}

generate_count = 0

@app.route('/', methods=['GET', 'POST', 'HEAD'])
async def homepage(request):
    global generate_count
    global generator

    if request.method == 'GET':
        params = request.query_params
    elif request.method == 'POST':
        params = await request.json()
    elif request.method == 'HEAD':
        return UJSONResponse({'text': ''},
                             headers=response_header)


    img_data = params.get('image')
    img_data = img_data[img_data.find(',') + 1:]

    with open("img.jpg", "wb") as fh:
        fh.write(base64.b64decode(img_data))


    item, prob, location = get_final_detection("img.jpg")
    prefix = ""
    if prob < 0.4 and location:
        prefix = make_prefix(location)
    else:
        prefix = make_prefix(item.capitalize())

    text = generator.generate_entry(prefix)
    # text = ''.join(text.split("@@@")[:-1])

    # Replace [i] with citations.
    for i in range(1, 10):
        text = text.replace('[{}]'.format(i),
            '<sup id="cite_ref-{0}" class="reference"><a href="#cite_note-3">&#91;{0}&#93;</a></sup>'.format(i))

    # Add links to random words
    words = text.split()
    words = set(words)
    for i, word in enumerate(words):
        if i % 2 == 0:
            if (len(word) > 5 and word[0].isupper()) or len(word) > 8:
                text = text.replace(word + " ", '{}{}{}'.format(
                    '<a href="#">', word + " ", '</a>'))

    text2 = completer.generate_entry(text, length=500)
    text = text.join(text2.split(".")[:-1])

    generate_count += 1

    gc.collect()
    return UJSONResponse({'text': text, 'prefix': item.capitalize()},
                         headers=response_header)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

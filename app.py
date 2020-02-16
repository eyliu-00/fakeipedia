from starlette.applications import Starlette
from starlette.responses import UJSONResponse
import gpt_2_simple as gpt2
import tensorflow as tf
import uvicorn
import os
import gc
import base64

# from fakeipedia import *
from detect import *

app = Starlette(debug=False)

# generator = Text_Generator()

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
        print("hello!!")
        return UJSONResponse({'text': ''},
                             headers=response_header)


    img_data = params.get('image')
    img_data = img_data[img_data.find(',') + 1:]

    with open("img.jpg", "wb") as fh:
        fh.write(base64.b64decode(img_data))


    prefix, prob = get_final_detection("img.jpg")
    prefix = prefix.capitalize()

    # text = generator.generate_entry(prefix)
    text = 'Hello friends'

    generate_count += 1

    gc.collect()
    return UJSONResponse({'text': text, 'prefix': prefix},
                         headers=response_header)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

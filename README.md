<div "center">
  <div>
    <h1 align="center">Llama OCR</h1>
  </div>
	<p align="center">An python library to run OCR for free with Llama 3.2 Vision.</p>
</div>

---

```
git clone  https://github.com/Rost381/llama-ocr.git
cd llama-ocr
``` 


## How it works

This library uses the free Llama 3.2 endpoint from [Together AI](https://togetherai.link/) to parse images and return json or markdown. Paid endpoints for Llama 3.2 11B and Llama 3.2 90B are also available for faster performance and higher rate limits.

You can control this with the `model` option which is set to `Llama-Vision-Free` by default but can also accept `Llama-3.2-11B-Vision` or `Llama-3.2-90B-Vision`.



## Installation for use from the command line
```
python3 -m venv venv
. ./venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Add TOGETHER_API_KEY to .env

`echo "TOGETHER_API_KEY=your_api_key_here" > .env`

### JSON (Default)

`./llama.py image.jpg`

### Formating JSON

`./llama.py image.jpg --pretty`

### Markdown

`./llama.py image.jpg --markdown`

### Using a paid model

`./llama.py image.jpg --model Llama-3.2-90B-Vision`

## Use in projects 
```
from base import ocr
```
### with default parameters
```
result = ocr(
    file_path=args.file_path,
    api_key=api_key
)
```
## or
```
result = ocr(
    file_path=file_path,
    api_key=api_key,
    model=model,
    return_markdown=markdown
)
```

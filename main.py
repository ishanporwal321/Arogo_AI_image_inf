from fastapi import FastAPI, File, UploadFile, HTTPException
import base64
from groq import Groq
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
   CORSMiddleware,
   allow_origins=["http://localhost:3000"],  # Adjust the port if your React app runs on a different port
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)

# Function to encode the image
def encode_image(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File is not an image.")
    
    image_bytes = await file.read()
    base64_image = encode_image(image_bytes)
    
    client = Groq(api_key="XYZ")
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What's in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        model="llama-3.2-11b-vision-preview",
    )
    
    description = chat_completion.choices[0].message.content
    
    return {"description": description}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
import asyncio
from concurrent.futures import ThreadPoolExecutor
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

executor = ThreadPoolExecutor(max_workers=1)

# Store uploaded file contents temporarily
uploaded_files = {}

@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Error: index.html not found</h1>"

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Handle file uploads"""
    try:
        # Read file content
        content = await file.read()
        
        # Try to decode as text
        try:
            text_content = content.decode('utf-8')
            file_type = "text"
        except UnicodeDecodeError:
            text_content = f"[Binary file: {file.filename}]"
            file_type = "binary"
        
        # Store in memory with session ID
        file_id = f"{file.filename}_{len(uploaded_files)}"
        uploaded_files[file_id] = {
            "filename": file.filename,
            "content": text_content,
            "type": file_type,
            "size": len(content)
        }
        
        return JSONResponse({
            "success": True,
            "file_id": file_id,
            "filename": file.filename,
            "size": len(content),
            "preview": text_content[:500] if len(text_content) > 500 else text_content
        })
        
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=400)

@app.post("/ask")
async def ask(request: Request):
    try:
        data = await request.json()
        prompt = data.get("prompt", [])
        file_context = data.get("file_context", None)
        
        print(f"Received prompt: {prompt}")
        
        # Add file context to the conversation if available
        if file_context:
            file_info = uploaded_files.get(file_context)
            if file_info:
                context_message = f"\n\n[File: {file_info['filename']}]\n{file_info['content']}"
                # Add file content to the first user message
                if prompt and prompt[0]['role'] == 'user':
                    prompt[0]['content'] += context_message
        
        try:
            import ollama
        except ImportError:
            return JSONResponse({"response": "Error: Run pip install ollama"})

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            executor,
            lambda: ollama.chat(model="Rice", messages=prompt)
        )

        print(f"Ollama response: {response}")

        # Handle different response formats
        if hasattr(response, 'message') and hasattr(response.message, 'content'):
            text = response.message.content
        elif isinstance(response, dict) and "message" in response:
            text = response["message"]["content"]
        else:
            text = str(response)

        print(f"Sending back: {text}")
        return JSONResponse({"response": text})

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse({"response": f"Error: {str(e)}"})

if __name__ == "__main__":
    import uvicorn
    print("🍚 Starting RiceGPT on http://localhost:8080")
    print("📎 File upload support enabled!")
    uvicorn.run(app, host="127.0.0.1", port=8080)


#  Offline AI Assistant  
A simple, local-first AI assistant that runs entirely on your machine. No cloud, no API keys, no hidden magic — just FastAPI, Ollama, and a lightweight frontend working together to give you an offline chat experience.

---

## 🚀 What This Project Does  
This app lets you:

- Chat with a local LLM (I used the **Rice** model on Ollama)  
- Upload files and ask questions about them  
- Preview uploaded content  
- Run everything offline on your own laptop  

It’s basically a tiny personal AI that doesn’t depend on the internet.

---

## 🛠️ Tech Behind It  
- **FastAPI** for the backend  
- **Ollama** for running the local model  
- **HTML + JS** for the frontend  
- **Uvicorn** as the server  
- **ThreadPoolExecutor** to keep model responses smooth  

---

## 📂 Project Layout  
```
offline-ai-assistant/
│── backend.py        # FastAPI server + file handling + model calls
│── index.html        # Simple frontend UI
│── requirements.txt  # Python dependencies
│── README.md
```

---

## ▶️ How to Run It

### 1. Install Python dependencies  
```
pip install fastapi uvicorn python-multipart
```

### 2. Install Ollama + your model  
Download Ollama from: https://ollama.com  
Then pull the model you want (example):  
```
ollama pull Rice
```

### 3. Start the server  
```
python backend.py
```

You should see something like:

```
🍚 Starting RiceGPT on http://localhost:8080
📎 File upload support enabled!
```

### 4. Open the app  
Just open `index.html` in your browser, or visit:  
```
http://localhost:8080
```

---

## 📡 API Overview

### **GET /**  
Serves the frontend.

### **POST /upload**  
Uploads a file and stores its content temporarily.

### **POST /ask**  
Sends your prompt (and optional file context) to the local model.

---

## 🌱 Ideas for Future Upgrades  
- A nicer UI (chat bubbles, dark mode, animations)  
- Support for multiple models  
- Save chat history  
- Add voice input/output  
- Let users download conversation logs  

---

## 🤝 Contributing  
If you want to improve something, feel free to open a PR or issue.  
This project is meant to be simple and hackable.


---


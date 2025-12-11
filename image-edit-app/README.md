# Image Edit App

A simple web app with a FastAPI backend and React frontend that edits uploaded images using OpenAI's `gpt-image-1-mini` model.

## Prerequisites
- Python 3.9+
- Node.js 18+
- An OpenAI API key

## Setup

1. **Clone and enter the project directory** (already inside `image-edit-app` for these steps).
2. **Create your environment file**
   ```bash
   cp .env.example .env
   ```
   Add your `OPENAI_API_KEY` to `.env`.

3. **Install backend dependencies**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Install frontend dependencies**
   ```bash
   cd ../frontend
   npm install
   ```

## Running the app

### Start the backend
From `image-edit-app/backend` (with your virtual environment activated):
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Start the frontend
In a new terminal from `image-edit-app/frontend`:
```bash
npm run dev -- --host
```
Vite dev server proxies `/api` and `/edited_image` to the backend.

### Build the frontend for production
```bash
npm run build
```

## How it works
- Upload an image and describe the edits you want.
- The backend saves the upload to `uploaded_image/`, sends it to OpenAI for editing, and stores the result in `edited_image/`.
- The frontend displays the edited image returned by the API.

## File structure
```
image-edit-app/
├── backend/
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
├── uploaded_image/
├── edited_image/
├── .env.example
├── .gitignore
└── README.md
```

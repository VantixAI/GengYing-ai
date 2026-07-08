# GengYing AI

> Find the right meme for every sentence.

GengYing AI is an AI-powered meme search and caption generator. Users can enter a sentence, and the system will find the most relevant memes based on its meaning and emotion.

For example:

> My boss asked me to work this weekend, but I am too afraid to say no.

The app returns matching memes and suggests several captions that users can copy or download.

## Features

- Search memes with natural language
- Return the six most relevant images
- Generate meme caption suggestions
- Copy or download memes
- Upload memes to a private collection
- Record clicks to improve future results

## How It Works

1. CLIP converts the user's text into a vector.
2. CLIP converts each meme image into a vector.
3. FAISS compares the vectors and finds the closest matches.
4. The app returns the most relevant memes.

The first version uses a pretrained CLIP model and does not require custom model training. In the future, user feedback can be used to improve ranking and fine-tune the model.

## Tech Stack

- **Frontend:** Next.js, TypeScript, Tailwind CSS
- **Backend:** Python, FastAPI
- **AI:** PyTorch, CLIP
- **Vector Search:** FAISS
- **Database:** SQLite
- **Deployment:** Vercel and Hugging Face Spaces

## Project Structure

```text
gengying-ai/
├── web/       # Next.js frontend
├── server/    # FastAPI backend and CLIP search
├── memes/     # Meme images
└── data/      # Vector index and database
```

## Status

This project is currently under development. The first version will support text-based meme search, caption suggestions, uploads, copying, and downloads.

## License

MIT

## Local Development

The repository is organized as a runnable MVP:

```text
gengying-ai/
|-- web/
|   |-- app/             # Next.js pages and styles
|   |-- components/      # Search, result, and upload UI
|   |-- lib/             # FastAPI client
|   `-- types/           # Shared frontend types
|-- server/
|   |-- main.py          # FastAPI endpoints
|   |-- model.py         # multilingual OpenCLIP encoder
|   |-- search.py        # FAISS similarity search
|   |-- build_index.py   # image indexing command
|   |-- database.py      # SQLite click tracking
|   `-- captions.py      # MVP caption generator
|-- memes/               # source and uploaded meme images
`-- data/                # generated index, metadata, and database
```

### Backend

Use Python 3.10 or 3.11, then run from the project root:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r server/requirements.txt
python -m server.build_index
uvicorn server.main:app --reload --port 8000
```

Put images into `memes/` before building the index. API documentation is available at `http://localhost:8000/docs`.

### Frontend

Use Node.js 20 or newer:

```powershell
cd web
Copy-Item .env.local.example .env.local
npm install
npm run dev
```

Open `http://localhost:3000`. Re-run `python -m server.build_index` after uploading new images so they become searchable.

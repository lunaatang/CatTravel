# Cat Travel

A fun web application that lets you send your cat on virtual adventures! Upload a photo of your cat, choose a destination, and see your feline friend in amazing places.

## Features

- Upload cat photos
- Generate realistic composite images using AI
- Modern, responsive UI

## Tech Stack

- Frontend: React 18 + Vite
- Backend: Python FastAPI
- AI: OpenAI API (DALL-E 3 and GPT-4o)


## Project Structure

```
Cat Travel/
├── frontend/           # React + Vite frontend
│   ├── public/         # Static assets
│   ├── src/
│   │   ├── assets/     # Frontend assets
│   │   ├── App.tsx     # Main React component
│   │   ├── App.css     # Styling
│   │   ├── main.tsx    # Entry point
│   │   └── index.css   # Global styles
│   ├── package.json    # Frontend dependencies
│   └── README.md       # Frontend documentation
├── backend/            # FastAPI backend
│   ├── app/
│   │   └── main.py     # FastAPI application with OpenAI integration
│   └── requirements.txt # Backend dependencies
├── package.json        # Root package.json for running both services
└── README.md           # Project documentation
```

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   # Install root dependencies
   npm install

   # Install frontend dependencies
   cd frontend
   npm install

   # Install backend dependencies
   cd ../backend
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the project root directory (important: make sure it's in the root directory `/Users/your-username/path/to/Cat Travel/`, NOT in backend/app/)
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```
   - Verify the API key is correctly loaded by checking the server logs when starting the application

4. Start the development servers:
   ```bash
   # From the root directory
   npm run dev
   ```
   This will start:
   - Frontend on http://localhost:5173
   - Backend on http://localhost:8000

## Usage

1. Open http://localhost:5173 in your browser
2. Upload a photo of your cat
3. Enter a location (e.g., "Paris", "the moon", "underwater")
4. Click "Generate" and wait for the magic to happen!
5. View and download your cat's new adventure photo

## Notes

- The application requires an OpenAI API key with access to the image generation API
- Image processing and generation may take a few seconds
- The AI analyzes your cat's features to create more accurate representations
- For best results, use clear photos of cats with good contrast against the background 
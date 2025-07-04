# LLM Email Writer

A web application that leverages Large Language Models (LLMs) to help users compose, edit, and export emails. The project features a React frontend and a Python FastAPI backend, with optional GPU acceleration via CUDA and Docker support.

## Features

- Compose and edit emails using LLMs
- Export emails to PDF
- Modern React frontend
- FastAPI backend with GPU support (CUDA)
- Easy deployment with Docker and Docker Compose

## Project Structure

```
llm_email_writer/
├── backend/         # FastAPI backend (Python)
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/        # React frontend (JavaScript)
│   ├── src/
│   ├── public/
│   └── Dockerfile
├── convert_to_pdf.py # Utility to convert emails to PDF
└── docker-compose.yml # Multi-container orchestration
```

## Prerequisites

- Docker & Docker Compose (recommended)
- Or:
  - Python 3.8+
  - Node.js & npm

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/llm_email_writer.git
cd llm_email_writer
```

### 2. Run with Docker (Recommended)

```bash
docker-compose up --build
```

- The frontend will be available at `http://localhost:3000`
- The backend API will be available at `http://localhost:8000`

### 3. Run Locally (Without Docker)

#### Backend

```bash
cd backend
pip install --upgrade pip
pip install -r requirements.txt
pip install vllm torch
uvicorn app:app --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend
npm install
npm start
```

## Usage

1. Open the frontend in your browser.
2. Compose your email using the LLM-powered interface.
3. Export your email to PDF as needed.

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements.

## License

[MIT License](LICENSE) (or specify your license here) 
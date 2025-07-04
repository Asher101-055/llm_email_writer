from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from vllm import LLM, SamplingParams


# Initialize FastAPI app
app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get model path from environment or use default
MODEL_PATH = ("Qwen/Qwen2.5-0.5B")
print("MODEL_PATH:", MODEL_PATH)

# Initialize vLLM with the specified model
llm = LLM(
    model=MODEL_PATH,
    gpu_memory_utilization=0.8,
    max_model_len=512,
    tensor_parallel_size=1
)

# Define request body structure for email generation
class EmailRequest(BaseModel):
    intent: str
    tone: str = "neutral"
    length: str = "medium"
    sender_name: str = "You"
    receiver_name: str = "Recipient"

# Helper function to build the prompt for the LLM
def build_prompt(intent, tone, length, sender_name, receiver_name):
    return (
        f"Write an email from {sender_name} to {receiver_name} about {intent}. "
        f"Use a {tone} tone. Keep it {length}."
    )

# API endpoint to generate an email using the LLM
@app.post("/generate-email")
async def generate_email(req: EmailRequest):
    prompt = build_prompt(req.intent, req.tone, req.length, req.sender_name, req.receiver_name)
    params = SamplingParams(
        temperature=0.7,
        top_p=0.9,
        max_tokens=200,
        top_k=20
    )
    outputs = llm.generate(prompt, sampling_params=params)
    email = outputs[0].outputs[0].text.strip()
    return {"email": email}
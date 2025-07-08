import os
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
MODEL_PATH = os.getenv("MODEL_PATH", "Qwen/Qwen2.5-0.5B")
print("MODEL_PATH:", MODEL_PATH)

# Initialize vLLM with the specified model
llm = LLM(
    model=MODEL_PATH,
    gpu_memory_utilization=0.8,
    max_model_len=1024,  # Increased for better context
    tensor_parallel_size=1
)

# Define request body structure for email generation
class EmailRequest(BaseModel):
    intent: str
    tone: str = "professional"
    length: str = "medium"
    sender_name: str = "You"
    receiver_name: str = "Recipient"

# Enhanced prompt engineering function
def build_prompt(intent, tone, length, sender_name, receiver_name):
    # Define tone-specific instructions
    tone_instructions = {
        "formal": "Use formal language, proper grammar, and professional vocabulary. Avoid contractions and slang.",
        "casual": "Use conversational language, contractions, and friendly expressions. Keep it relaxed and approachable.",
        "professional": "Use business-appropriate language with clear structure. Be respectful and courteous.",
        "friendly": "Use warm, welcoming language with positive expressions. Show genuine interest and care.",
        "urgent": "Use direct, action-oriented language. Emphasize time sensitivity and importance.",
        "apologetic": "Use humble, regretful language. Acknowledge the issue and show commitment to resolution.",
        "enthusiastic": "Use energetic, positive language with exclamation marks where appropriate. Show excitement and passion."
    }
    
    # Define length constraints
    length_constraints = {
        "short": "Keep the email concise (2-3 sentences). Get straight to the point.",
        "medium": "Write a balanced email (4-6 sentences). Include necessary details without being verbose.",
        "long": "Write a comprehensive email (7-10 sentences). Provide detailed explanations and context."
    }
    
    # Build the enhanced prompt with explicit instructions
    prompt = f"""Write a {tone} email from {sender_name} to {receiver_name}.

Topic: {intent}

INSTRUCTIONS:
- {sender_name} is writing TO {receiver_name}
- Be direct and clear about the purpose
- Use appropriate language for the tone and context
- Focus on the main message: {intent}
- Make it natural and appropriate for the relationship between {sender_name} and {receiver_name}
- {tone_instructions.get(tone, '')}
- {length_constraints.get(length, '')}

Email format:
Dear {receiver_name},

[Main message - state the purpose clearly]

[Additional context if needed]

[Professional closing]

Keep it {length} in length.

Write the email now:"""

    return prompt

# Enhanced sampling parameters for better output
def get_sampling_params(tone, length):
    # Adjust temperature based on tone
    base_temp = 0.5
    if tone in ["casual", "enthusiastic"]:
        base_temp = 0.8
    elif tone in ["formal", "professional"]:
        base_temp = 0.6
    
    # Adjust max_tokens based on length
    length_tokens = {
        "short": 150,
        "medium": 300,
        "long": 500
    }
    
    return SamplingParams(
        temperature=base_temp,
        top_p=0.9, #adapts to top k , filtering
        top_k=50,  # balance diversity
        max_tokens=length_tokens.get(length, 300),
        repetition_penalty=1.1,  # Prevent repetitive text
        presence_penalty=0.1,  # Encourage diverse vocabulary
        frequency_penalty=0.1
    )

# API endpoint to generate an email using the LLM
@app.post("/generate-email")
async def generate_email(req: EmailRequest):
    prompt = build_prompt(req.intent, req.tone, req.length, req.sender_name, req.receiver_name)
    params = get_sampling_params(req.tone, req.length)
    
    print(f"DEBUG: Sending prompt to model: {prompt}")
    try:
        outputs = llm.generate(prompt, sampling_params=params)
        if not outputs or not outputs[0].outputs or not outputs[0].outputs[0].text:
            print("DEBUG: Model returned no output.")
            return {"email": "Error: Model did not return any output."}
        raw_output = outputs[0].outputs[0].text
        email = raw_output.strip()
    except Exception as e:
        print(f"Model error: {e}")
        return {"email": f"Error: {str(e)}"}
    
    print(f"DEBUG: Raw model output: '{raw_output}'")
    print(f"DEBUG: Processed email: '{email}'")
    
    return {"email": email}
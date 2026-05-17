from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import time
import re

app = FastAPI(
    title="10MinZepto AI Grocery Assistant",
    description="A premium chatbot microservice serving real-time grocery queries.",
    version="1.0.0"
)

# Configure CORS to allow communication from the Django frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local development, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    user_email: str = "guest"

class ChatResponse(BaseModel):
    reply: str
    suggestions: list[str]

# Premium Grocery Query Catalog
INTENTS = [
    {
        "keywords": [r"hello", r"hi", r"hey", r"greetings", r"hola"],
        "responses": [
            "Hello! I am your 10MinZepto AI assistant. How can I help you with your fresh groceries today? 🍎🛒",
            "Hey there! Ready for some lightning-fast delivery? Ask me about our fresh fruits, vegetables, or today's deals! ⚡🥑",
            "Hi! Welcome to 10MinZepto. What fresh ingredients or snacks can I help you find today? 🍇🥦"
        ],
        "suggestions": ["Show Today's Deals", "How fast is delivery?", "Track my order"]
    },
    {
        "keywords": [r"delivery", r"speed", r"time", r"how fast", r"minutes"],
        "responses": [
            "We deliver 100% farm-fresh groceries to your doorstep in **under 10 minutes** from our closest hyper-local dark store! ⚡📦",
            "Our average delivery time is just **8.4 minutes**! Our riders are dispatched instantly once your order is confirmed. 🚴‍♂️💨"
        ],
        "suggestions": ["Is delivery free?", "Track my order", "Payment options"]
    },
    {
        "keywords": [r"fresh", r"quality", r"organic", r"farm", r"fruits", r"vegetables"],
        "responses": [
            "At 10MinZepto, quality is our absolute priority. We source our fruits and vegetables directly from local farms daily at 4:00 AM! 🌾🍏",
            "Every product undergoes strict 7-stage quality checks. If you are not satisfied, we offer instant refunds with no questions asked! 🛡️🍊"
        ],
        "suggestions": ["How to get refund?", "Today's Deals", "Show categories"]
    },
    {
        "keywords": [r"deal", r"offer", r"discount", r"coupon", r"promo", r"sale"],
        "responses": [
            "Check out our **Today's Deals** section on the homepage for up to **50% OFF** fresh essentials, snacks, and masalas! 🏷️🔥",
            "Use coupon code **ZEPTOFIRST** at checkout to get **flat 20% off** plus free delivery on your first order! 🎁🛒"
        ],
        "suggestions": ["Browse Products", "Is delivery free?", "Payment options"]
    },
    {
        "keywords": [r"track", r"where is my order", r"status", r"order"],
        "responses": [
            "You can track your live order status by visiting the **My Profile** or **My Cart** page once logged in! 🗺️👀",
            "All active dispatches show real-time rider tracking. Need immediate help? Call us at **+91-8115500585**. 📞🚴‍♂️"
        ],
        "suggestions": ["Contact support", "Browse Products", "Today's Deals"]
    },
    {
        "keywords": [r"refund", r"return", r"cancel", r"money back", r"complaint"],
        "responses": [
            "Not satisfied with an item? Simply go to your profile, select the order, and click 'Request Refund'. We issue instant wallet credits! 💳🛡️",
            "For refund assistance, please email our support team at **vishalkaverma811@gmail.com** or call **+91-8115500585**. We are active 24/7! 📞✉️"
        ],
        "suggestions": ["Contact support", "How fast is delivery?", "Today's Deals"]
    },
    {
        "keywords": [r"free", r"shipping", r"charge", r"cost"],
        "responses": [
            "Delivery is absolutely **FREE** on all orders above **₹199**! For smaller orders, a nominal fee of ₹15 applies. 🚚💰",
            "Keep an eye out for free delivery promotions on our homepage carousel banner! 🌟🚴‍♂️"
        ],
        "suggestions": ["Today's Deals", "How fast is delivery?", "Browse Products"]
    },
    {
        "keywords": [r"support", r"contact", r"phone", r"email", r"help", r"call"],
        "responses": [
            "Our 10MinZepto Support Team is here 24/7! You can reach us at:\n- **Phone**: +91-8115500585 📞\n- **Email**: vishalkaverma811@gmail.com ✉️",
            "Need help with your order? Reach out to us instantly via phone at **+91-8115500585** or email **vishalkaverma811@gmail.com**. We resolve most queries in under 5 minutes! 🤝⚡"
        ],
        "suggestions": ["Track my order", "How to get refund?", "Today's Deals"]
    }
]

DEFAULT_RESPONSES = [
    "I'm not sure I fully understand. Could you please specify if you're asking about our fresh fruits, delivery speeds, refund policies, or today's deals? 🍎🥦",
    "I'm here to help you get fresh groceries in 10 minutes! Try asking me about 'delivery speed', 'deals', or 'how to get a refund'. ⚡🛍️",
    "That sounds interesting! Please ask me about our fresh vegetables, offers, or contact support at +91-8115500585 for instant assistance. 📞🥦"
]

DEFAULT_SUGGESTIONS = ["How fast is delivery?", "Today's Deals", "Track my order", "Contact support"]

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "10MinZepto AI Grocery Assistant",
        "endpoints": ["/chat"]
    }

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    user_msg = request.message.strip().lower()
    
    # Introduce a short mock latency (500ms) to simulate human processing and make UI feel extremely natural
    time.sleep(0.5)
    
    # Matching intents
    for intent in INTENTS:
        for keyword in intent["keywords"]:
            if re.search(keyword, user_msg):
                reply = random.choice(intent["responses"])
                suggestions = intent["suggestions"]
                return ChatResponse(reply=reply, suggestions=suggestions)
                
    # Default response if no intent matches
    reply = random.choice(DEFAULT_RESPONSES)
    return ChatResponse(reply=reply, suggestions=DEFAULT_SUGGESTIONS)

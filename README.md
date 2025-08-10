AI Clinic Assistant - FastAPI BackendThis project is a production-ready, multi-tenant backend for an AI-powered WhatsApp assistant tailored for clinics (beauty salons, dental clinics, therapy centers, etc.). It's built with Python, FastAPI, and a suite of modern technologies to provide a scalable, customizable, and robust solution.✨ FeaturesCore Backend:FastAPI: High-performance asynchronous web framework.PostgreSQL: Robust relational database for data persistence.Pydantic: Data validation and settings management.Celery & Redis: Asynchronous task queue for background processing.FastAPI Users & JWT: Secure authentication and user management.Environment-based Config: Using .env for easy configuration.🤖 AI Integration:OpenAI GPT-4: State-of-the-art language model for conversational AI.Dynamic Prompt Engineering: Prompts are customized for each clinic (name, services, tone, etc.).Chat History: All conversations are logged for review and fine-tuning.Streaming Responses: Server-Sent Events (SSE) for real-time message streaming.💬 WhatsApp Integration:Twilio/360Dialog: Ready for integration with major WhatsApp Business API providers.Message Queueing: Celery ensures reliable processing of incoming messages.🧠 Vector Database (RAG):Pinecone Integration: For efficient similarity search on clinic-specific documents.Document Management: Clinics can upload documents (FAQs, service lists) to be used as context for the AI.Retrieval Augmented Generation (RAG): Enhances AI responses with information retrieved from the vector store.⚙️ Admin & Customization:Multi-Tenancy: Data isolation for each clinic.Admin Panel (via FastAPI): Endpoints for clinic registration, service management, and AI tuning.Chat History Viewer: Endpoint to review conversations for each clinic.🚀 DevOps & Deployment:Docker & Docker Compose: Containerized setup for easy development and deployment.Gunicorn: Production-ready WSGI server.Loguru: Structured and powerful logging.OpenAPI Documentation: Automatic interactive API docs.Health Check: Endpoint for monitoring service status.📂 Project Structureapp/
├── main.py
├── config.py
├── database.py
├── models/
│   ├── __init__.py
│   ├── base.py
│   ├── chat.py
│   ├── clinic.py
│   └── user.py
├── schemas/
│   ├── __init__.py
│   ├── chat.py
│   ├── clinic.py
│   ├── token.py
│   └── user.py
├── routers/
│   ├── __init__.py
│   ├── auth.py
│   ├── chat.py
│   └── clinic.py
├── services/
│   ├── __init__.py
│   ├── auth.py
│   ├── ai_engine.py
│   ├── vectorstore.py
│   └── whatsapp.py
├── utils/
│   ├── __init__.py
│   └── prompt_builder.py
├── background/
│   ├── __init__.py
│   └── tasks.py
└── admin/
    ├── __init__.py
    └── dashboard.py
.env.example
docker-compose.yml
Dockerfile
requirements.txt
🚀 Getting StartedPrerequisitesDocker and Docker ComposeAn OpenAI API KeyA Pinecone API Key and EnvironmentA Twilio Account SID, Auth Token, and WhatsApp number (or another provider)SetupClone the repository:git clone <repository-url>
cd <repository-name>
Create and configure the environment file:Copy the example environment file:cp .env.example .env
Edit the .env file and fill in your credentials for the database, OpenAI, Pinecone, and Twilio.Build and run the application with Docker Compose:docker-compose up --build
This will start the FastAPI application, PostgreSQL database, Redis, and a Celery worker.Access the API Documentation:Once the containers are running, navigate to http://localhost:8000/docs in your browser.You will see the interactive OpenAPI documentation for all available endpoints.How it WorksClinic Registration: A clinic owner registers an account.Configuration: The owner configures their clinic's details, services, and AI personality.Document Upload: The owner can upload documents (e.g., FAQs) which are then chunked, embedded, and stored in Pinecone.WhatsApp Message: A customer sends a message to the clinic's WhatsApp number.Message Ingestion: Twilio forwards the message to the /whatsapp/webhook endpoint.AI Processing: The message is put into a Celery queue. The AI engine retrieves relevant context from Pinecone (RAG), builds a dynamic prompt, and gets a response from OpenAI's GPT-4.Response Delivery: The generated response is sent back to the customer via the Twilio API.Logging: The entire conversation is saved to the database.
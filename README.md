# AWS RAG Technical Assistant 🚀

A stateful, chatbot designed to help users keen on AWS ML Specialty particularly, navigate AWS Machine Learning and Cloud Infrastructure concepts.

## 🛠️ The Architecture
- **LLM Engine:** Amazon Nova Lite (via Amazon Bedrock)
- **Knowledge Base:** Retrieval-Augmented Generation (RAG) using an S3-backed vector store.
- **Backend:** AWS Lambda (Python/Boto3) with custom session management.
- **Frontend:** Responsive HTML5/JavaScript with Markdown rendering.

## 💡 Key Features
- **Semantic Flexibility:** The bot is programmed to handle terminology errors (e.g., clarifying "Language Learning Model" vs. "Large Language Model") through custom prompt engineering.
- **Session Persistence:** Maintains conversation history across multiple turns using Bedrock Session IDs.
- **Contextual Grounding:** Answers are strictly grounded in technical documentation stored in S3 to prevent hallucinations.

## 🚀 Deployment
The backend is deployed as a serverless AWS Lambda function, integrated with Amazon Bedrock's `retrieve_and_generate` API to provide real-time, documented technical support.

import boto3
import json

client = boto3.client('bedrock-agent-runtime', region_name='eu-central-1')

KNOWLEDGE_BASE_ID = 'TFHZCWWETH'
MODEL_ARN = 'eu.amazon.nova-lite-v1:0' 

def lambda_handler(event, context):
    user_query = None
    session_id = None
    
    try:
        if 'body' in event and event['body']:
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        else:
            body = event

        user_query = (body.get('question') or body.get('prompt') or 
                      body.get('message') or body.get('query') or body.get('text'))
        session_id = body.get('sessionId')
                      
    except Exception as e:
        print(f"Data Extraction Error: {str(e)}")

    if not user_query:
        return {
            'statusCode': 400,
            'headers': {"Access-Control-Allow-Origin": "*"},
            'body': json.dumps("No prompt found.")
        }

    try:
        rg_params = {
            'input': {'text': user_query},
            'retrieveAndGenerateConfiguration': {
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': KNOWLEDGE_BASE_ID,
                    'modelArn': MODEL_ARN,
                    'generationConfiguration': {
                        'promptTemplate': {
                            'textPromptTemplate': """
You are a professional AWS Technical Assistant. Use the provided SEARCH RESULTS to answer the user's question with technical precision.

### OPERATIONAL GUIDELINES:
- SCOPE: Your primary knowledge is AWS Machine Learning and Cloud Infrastructure. If a topic is in the search results, prioritize that information.
- SEMANTIC FLEXIBILITY: If a user uses a slightly incorrect term (e.g., "Language Learning Model" or "S3 Storage"), interpret their intent based on the technical context of AWS and AI.
- CLARIFICATION: If you correct a user, do it helpfully. (e.g., "I believe you're asking about Large Language Models (LLMs)...").
- SYNTHESIS: When a user asks a complex "How-to" question, combine relevant facts from different sections of the search results to provide a complete workflow.
- FALLBACK: If the answer is absolutely not in the results, state that you are a specialist in the provided domain and offer to discuss a related concept that IS in your records.

SEARCH RESULTS:
$search_results$

USER QUESTION:
$query$
"""
                        }
                    }
                }
            }
        }

        if session_id and session_id != "null":
            rg_params['sessionId'] = str(session_id)

        response = client.retrieve_and_generate(**rg_params)
        answer = response['output']['text']
        new_session_id = response.get('sessionId')

        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST",
                "Content-Type": "application/json"
            },
            'body': json.dumps({
                "answer": answer,
                "sessionId": new_session_id 
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {"Access-Control-Allow-Origin": "*"},
            'body': json.dumps(f"AI Error: {str(e)}")
        }
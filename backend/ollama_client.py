import ollama

def get_ollama_response(prompt):
    response = ollama.chat(
        model='llama3',
        messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ],
        options={
            'temperature': 0.2
        }
    )
    return response['message']['content']

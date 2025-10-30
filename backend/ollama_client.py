import ollama

def get_ollama_response(prompt):
    try:
        response = ollama.chat(
            model='gemma3:1b',
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                }
            ],
            options={
                'temperature': 0.2
            }
        )
        return response['message']['content']
    except Exception as e:
        return f"Error communicating with Ollama: {str(e)}"

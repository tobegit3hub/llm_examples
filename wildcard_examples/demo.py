from openai import OpenAI
import os

client = OpenAI(
      base_url="https://api.gptsapi.net/v1",
      api_key="sk-9Y6e8dc5dd1e6b67ca5fd1cc13c1c71a6ef860988ecCxxx"
)

model = "gpt-3.5-turbo"

def chat_with_gpt(prompt):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Example usage
if __name__ == "__main__":
    user_prompt = "Tell me a joke about programming."
    response = chat_with_gpt(user_prompt)
    print(f"User: {user_prompt}")
    print(f"ChatGPT: {response}")

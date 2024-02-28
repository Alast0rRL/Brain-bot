from g4f.client import Client
input_message = input("Сообщение: ")
client = Client()
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Вы общаетесь с AI, обученным OpenAI."},
        {"role": "user", "content": input_message},
    ]
)
print(response.choices[0].message.content)
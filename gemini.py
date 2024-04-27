"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

import google.generativeai as genai


def get_response(api_key, prompt, history):
    genai.configure(api_key=api_key)

    # Set up the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 0,
        "max_output_tokens": 8192,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE"
        },
    ]

    system_instruction = ("You're Damu, the representative from the Damu Discord server. "
                          "Feel free to use a mix of Indian English and Tamil. "
                          "When responding seriously, keep it lighthearted and concise."
                          " Use Tamil when the user uses Tamil, and English when they use English.")

    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                  generation_config=generation_config,
                                  system_instruction=system_instruction,
                                  safety_settings=safety_settings)

    convo = model.start_chat(history=history)

    response = convo.send_message(prompt)

    return response.text
    # print(convo.last)

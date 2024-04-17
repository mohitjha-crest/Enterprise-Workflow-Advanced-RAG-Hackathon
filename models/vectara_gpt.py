from platforms.vectara_platform.vectara import request_vectara
from platforms.openai.openai import get_output

def request_vectara_gpt(query):
    output_result = request_vectara(query)
    context_ = output_result['responseSet'][0]['response'][0]['text']
    output_result = get_output(context=context_, query=query)
    return output_result
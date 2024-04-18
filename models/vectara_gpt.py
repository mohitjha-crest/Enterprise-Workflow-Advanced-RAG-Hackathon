from platforms.vectara_platform.vectara import request_vectara_sop, request_vectara_sop_and_chat_history
from platforms.openai.openai import get_output

def request_vectara_gpt_sop(query):
    output_result = request_vectara_sop(query)
    print ("output_result-->", output_result)
    context_ = output_result['responseSet'][0]['response'][0]['text']
    output_result = get_output(context=context_, query=query)
    return output_result

def request_vectara_gpt_sop_and_chat_history(query):
    output_result = request_vectara_sop_and_chat_history(query)
    context_ = output_result['responseSet'][0]['response'][0]['text']
    output_result = get_output(context=context_, query=query)
    return output_result
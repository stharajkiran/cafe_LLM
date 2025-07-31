def get_chatbot_response(client,model_name,messages,temperature=0):
    """_summary_

    Args:
        client (_type_): _description_
        model_name (_type_): _description_
        messages (_type_): _description_
        temperature (int, optional): _description_. Defaults to 0.

    Returns:
        _type_: _description_
    """
    input_messages = []
    for message in messages:
        input_messages.append({"role": message["role"], "content": message["content"]})

    response = client.chat.completions.create(
        model=model_name,
        messages=input_messages,
        temperature=temperature,
        top_p=0.8,
        max_tokens=2000,
    ).choices[0].message.content
    
    return response


def get_embedding(embedding_client,model_name,text_input):
    """

    Args:
        embedding_client (OpenAI): OpenAI client API
        model_name (str): model to be used
        text_input (str): text to be embedded

    Returns:
        embedings: vectore embedding
    """
    output = embedding_client.embeddings.create(input = text_input,model=model_name)
    
    embedings = []
    for embedding_object in output.data:
        embedings.append(embedding_object.embedding)

    return embedings

def double_check_json_output(client,model_name,json_string):
    prompt = f""" You will check this json string and correct any mistakes that will make it invalid. Then you will return the corrected json string. Nothing else. 
    If the Json is correct just return it.

    If there is any text before order after the json string, remove it.
    Do NOT return a single letter outside of the json string.
    The first thing you should write is open curly brace of the json and last letter you write should be the closing curly brace.

    You should check the json string for the following text between triple backticks:
    ```
    {json_string}
    ```
    """

    messages = [{"role": "user", "content": prompt}]

    response = get_chatbot_response(client,model_name,messages)
    response = response.replace("`","")

    return response
import requests
import time

def _translate_list_of_text(auth_key: str, lang: str, texts: list[str]) -> list[str]:
    if len(texts) > 50:
        raise Exception
    
    url = f"https://api-free.deepl.com/v2/translate?auth_key={auth_key}&target_lang={lang}"
    for text in texts:
        url += f"&text={text}"
        
    req = requests.get(url)
    content = req.json()
    return [
        translation["text"] 
        for translation in content["translations"]
    ]

def _parse_dict(auth_key: str, lang: str, value: dict):
    result = {}
    keys = list(value.keys())
    values = parse(auth_key, lang, list(value.values()))
    
    for num, key in enumerate(keys):
        result[key] = values[num]
    
    return result

def _parse_list(auth_key: str, lang: str, value: list):
    result = []
    t1, t2 = [], []
    for i in range(0, len(value)):
        if not isinstance(value[i], str):
            t2.append(i)
            
        t1.append(value[i])
        
    values = [t1[i:i+50] for i in range(0, len(t1), 50)]
    for v in values:
        result.extend(_translate_list_of_text(auth_key, lang, v))
        
    for i in t2:
        result.insert(i, parse(value[i]))
        
    return result

def parse(auth_key: str, lang: str, obj): 
    if isinstance(obj, dict):
        result = _parse_dict(auth_key, lang, obj)    
    elif isinstance(obj, list):
        result = _parse_list(auth_key, lang, obj)
    elif isinstance(obj, str):
        result = _translate_list_of_text(auth_key, lang, [obj])[0]

    time.sleep(1.0)
    return result
        
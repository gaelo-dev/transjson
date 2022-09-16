from urllib.parse import urlparse, urljoin
from urllib import parse
import requests
import time

def _translate_list_of_text(auth_key: str, lang: str, texts: list[str]) -> list[str]:
    if len(texts) > 50:
        raise Exception
    
    url = parse.urlparse("https://api-free.deepl.com/v2/translate?auth_key=aaa")
    url._replace()
    url = parse.urljoin("https://api-free.deepl.com/v2/translate", parse.urlencode({"auth_key": auth_key, "target_lang": lang}))
    for text in texts:
        url = parse.urljoin(url, parse.urlencode({"text": text}))
    
    req = requests.get(parse.urlparse(url).geturl())
    content = req.json()
    return [
        translation["text"] 
        for translation in content["translations"]
    ]
        
class Parser:
    def __init__(self, auth_key: str, lang: str, value) -> None:
        self.auth_key = auth_key
        self.lang = lang
        self.value = value
    
    def ___translate_list(self, texts: list[str]) -> list[str]:
        if len(texts) > 50:
            raise Exception
        
        url = parse.urlparse(parse.urljoin(
            "https://api-free.deepl.com/v2/translate?", 
            parse.urlencode({
                "auth_key": self.auth_key, 
                "target_lang": self.lang
            })
        ))
        
        for text in texts:
            url = url._replace(query=f"{url.query}&" + parse.urlencode({"text": text}))
            
        req = requests.get(url)
        content = req.json()
        return [
            translation["text"] 
            for translation in content["translations"]
        ]
    
    def __dict(self, value: dict) -> dict:
        result = {}
        keys = list(value.keys())
        values: list = Parser(self.auth_key, self.lang, list(value.values)).parse()
        
        for num, key in enumerate(keys):
            result[key] = values[num]
        
        return result
    
    def __list(self, value: list) -> list:
        result = []
        t1, t2 = [], []
        for i, val in enumerate(value):
            if isinstance(val, str):
                t1.append(val)
            else:
                t2.append(i)
            
            
        values = [t1[i:i+50] for i in range(0, len(t1), 50)]
        for v in values:
            result.extend(self.___translate_list(v))
            
        for i in t2:
            result.insert(i, Parser(self.auth_key, self.lang, value[i]).parse())
        
        return result
    
    def parse(self):
        if isinstance(self.value, dict):
            result = self.__dict(self.value)
        elif isinstance(self.value, list): 
            result = self.__list(self.value)
        elif isinstance(self.value, str):
            result = self.___translate_list([self.value])[0]
        else:
            result = self.value
        
        time.sleep(1.0)
        return result
    
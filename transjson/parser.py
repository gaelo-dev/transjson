from urllib import parse
from threading import Lock
from typing import Self, Any, ItemsView, Iterator
import requests
import time
import re


class Cache:
    def __init__(self) -> None:
        self.lock = Lock()
        self._cache = {}
        self.count = 1

    def __iter__(self) -> Iterator:
        return self._cache.__iter__()

    def __enter__(self) -> Self:
        self.lock.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.lock.locked:
            self.lock.release()
            
    def set(self, match: Any) -> None:
        self._cache[match] = "{=" + str(self.count) + "=}"
        self.count += 1
        
    def items(self) -> ItemsView[Any, str]:
        return self._cache.items()


class Parser:
    def __init__(self, cache: Cache, auth_key: str, lang: str, value) -> None:
        self.cache = cache
        self.auth_key = auth_key
        self.lang = lang
        self.value = value
    
    def ___translate_list(self, texts: list[str]) -> list[str]:
        if len(texts) > 50:
            raise Exception

        url = parse.urlparse("https://api-free.deepl.com/v2/translate")
        url = url._replace(query=parse.urlencode({"auth_key": self.auth_key, "target_lang": self.lang}))

        for text in texts:
            text = self.__parse_and_cache(text)
            url = url._replace(query=f"{url.query}&" + parse.urlencode({"text": text}))
            
        req = requests.get(url.geturl())
        content = req.json()
        return [
            self.__unparse_from_cache(translation["text"])
            for translation in content["translations"]
        ]
    
    def __dict(self, value: dict) -> dict:
        result = {}
        keys = list(value.keys())
        values: list = Parser(self.auth_key, self.lang, list(value.values())).parse()

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
    
    def __parse_and_cache(self, text: str):
        with self.cache as c:
            matchs = re.findall(r'(\{[^}]*\})', text)
            for match in matchs:
                if match not in c:
                    c.set(match)
            
            for k, v in c.items():
                text = text.replace(k, v)
        
        return text

    def __unparse_from_cache(self, text: str):
        with self.cache as c:
            for k, v in c.items():
                print(k, v, "**", text)
                text = text.replace(v, k)
                print("**", text)
        
        return text

    
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
    
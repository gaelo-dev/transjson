import aiohttp
import env


class ClientSession(aiohttp.ClientSession):
    def __init__(self, **kwargs) -> None:
        super().__init__("https://api-free.deepl.com", **kwargs)

    async def search_translation(self, lang, value):
        if isinstance(value, dict):
            translation = {}
            for k, v in value.items():
                translation[k] = await self.search_translation(lang, v)
            
            return translation
        
        if isinstance(value, list):
            translation = []
            for v in value:
                await translation.append(self.search_translation(lang, v))
                
            return translation
        
        if isinstance(value, str):
            async with self.get(f"/v2/translate?auth_key={env.auth_key}&text={value}&target_lang={lang}") as resp:
                json = await resp.json()
                return json["text"]
            
        return value

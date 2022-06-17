import asyncio
import aiohttp
import env


class ClientSession(aiohttp.ClientSession):
    def __init__(self, **kwargs) -> None:
        super().__init__("https://api-free.deepl.com", **kwargs)

    async def search_translation(self, lang, value):
        if isinstance(value, dict):
            translation = {}
            keys = [k for k in value.keys()]
            values = self.search_translation(lang, [v for v in value.values()])
            
            for n, k in enumerate(keys):
                translation[k] = values[n]
            
            return translation
        
        if isinstance(value, list):
            translation = []
            url = f"/v2/translate?auth_key={env.auth_key}&target_lang={lang}"
            for v in value:
                if not isinstance(v, str):
                    translation.append(self.search_translation(lang, v))
                    continue
                        
                url += f"&text={value}"

            async with self.post(url) as resp:
                print(f"translating -> {lang}")
                json = await resp.json()
                for k, v in json["translations"]:
                    if k == "text":
                        translation.append(v)
            
            return translation
        
        if isinstance(value, str):
            await self.search_translation(lang, [value])
        
        await asyncio.sleep(1.5)
        return value
    
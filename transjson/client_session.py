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
            values = await self.search_translation(lang, [v for v in value.values()])

            for n, k in enumerate(keys):
                translation[k] = values[n]

            return translation

        if isinstance(value, list):
            translation = []
            text = False
            url = f"/v2/translate?auth_key={env.auth_key}&target_lang={lang}"
            for v in value:
                if not isinstance(v, str):
                    translation.append(await self.search_translation(lang, v))
                    continue

                url += f"&text={v}"
                text = True

            if text:
                async with self.post(url) as resp:
                    print(f"translating -> {lang}")
                    json = await resp.json()
                    for i in json["translations"]:
                        translation.append(i["text"])

            return translation

        if isinstance(value, str):
            translation = await self.search_translation(lang, [value])
            return translation[0]

        await asyncio.sleep(1.5)
        return value

from client_session import ClientSession
import asyncio
import argparse
import json


def args_parse():    
    parser = argparse.ArgumentParser(description="file to be translated")
    parser.add_argument("file")
    parser.add_argument("languages", default=["en"], type=lambda s: s.split(","), nargs=argparse.OPTIONAL)
    parser.add_argument("directory", default="", nargs=argparse.OPTIONAL)
    
    return parser.parse_args()


async def main():
    args = args_parse()

    with open(args.file, "r") as f:
        translation_base: dict = json.loads(f.read())
    
    async with ClientSession() as session:
        for lang in args.languages:
            translation = {}
            for key, value in translation_base.items():
                translation[key] = await session.search_translation(lang, value)
            
            with open(f"{args.directory}/{lang}.json", "w") as f:
                f.write(json.dumps(translation))

                
asyncio.run(main())
from .parser import Parser, Cache
import threading
import dotenv
import click
import json


class Translate(threading.Thread):
    def __init__(self, cache, auth_key, lang, value, dir) -> None:
        super().__init__(daemon=False)
        self.cache = cache
        self.auth_key = auth_key
        self.lang = lang
        self.value = value
        self.dir = dir
        self.start()
    
    def run(self) -> None:
        with open(f"{self.dir}/{self.lang}.json", "w") as f:
            f.write(json.dumps(Parser(self.cache, self.auth_key, self.lang, self.value).parse(), ensure_ascii=False, indent=4))


@click.command
@click.argument("filename", type=click.Path(exists=True, dir_okay=False))
@click.option("-k", "--key", envvar="AUTH_KEY")
@click.option("-l", "--lang", multiple=True, default=["es"])
@click.option("-d", "--directory", default=".", type=click.Path(file_okay=False))
def transjson(filename, key, lang, directory):
    if key is None:
        raise Exception("Missing auth key")
        
    with open(filename, "r") as f:
        base = json.load(f)
    
    cache = Cache()
    threads = []
    for l in lang:
        threads.append(Translate(cache, key, l, base, directory))


if "__main__" == __name__:
    dotenv.load_dotenv()
    transjson()

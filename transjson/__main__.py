import threading
import click
import parser
import json


class Translate(threading.Thread):
    def __init__(self, auth_key, lang, obj, dir) -> None:
        super().__init__(daemon=False)
        self.auth_key = auth_key
        self.lang = lang
        self.obj = obj
        self.dir = dir
        
        self.start()
    
    def run(self) -> None:
        with open(f"{self.dir}/{self.lang}.json", "w") as f:
            f.write(json.dumps(parser.parse(self.auth_key, self.lang, self.obj), indent=4))


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
    
    print(lang)
    threads = []
    for l in lang:
        threads.append(Translate(key, l, base, directory))


if "__main__" == __name__:
    transjson()

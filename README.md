# Transjson
a script that automates the translation of a json using the deepl api

## Settings
---
add an .env file and set the authentication token, like here:
```
AUTH_KEY="your_token"
```

### Other environment variables
+ **DEFAULT_LANGUAGES** -> languages to which the file will be translated without the need to specify it, it is of type list

## Usage
---
arguments:
```
file [languages] [directory]
```

+ **file** -> file to translate
+ **languages** -> languages to translate (eg: "en, es")
+ **directory** -> directory where the new translations will be saved
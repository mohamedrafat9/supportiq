import re
import unicodedata

def clean_text(text:str)->str:
    if not isinstance(text,str):
        raise TypeError("text must be a string")

    text=unicodedata.normalize("NFC",text)

    text=text.replace("\r\n","\n").replace("\r","\n")

    text="".join(
        char
        for char in text 
        if char in "\n\t" or unicodedata.category(char)!="Cc"
    )

    text = re.sub(r"[^\S\n]+", " ", text)

    text = re.sub(r" *\n *", "\n", text)

    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


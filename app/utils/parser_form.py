def parsing_number(text: str,default):
    text=text.replace(" ","")
    text=text.replace(",",".")
    if text=="":
        return default
    else:
        try:
            return float(text)
        except ValueError:
            print(f"{text} - НЕ ЧИСЛО")



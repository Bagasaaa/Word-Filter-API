import re

def cleansing(text):
    # Make text being lowercase
    text = text.lower()

    # Remove punctuation, math operation char, etc
    pattern_1 = r'[\`\~\!\@\#\$\%\^\&\*\(\)\_\+\-\=\[\]\\\;\'\,\.\/\{\}\|\:\"\<\>\?\"]'
    text = re.sub(pattern_1, "", text)

    # Remove Whitespace or Multiplespace
    pattern_2 = r'(\s+)'
    text = re.sub(pattern_2, " ", text)

    # Remove numbers
    pattern_3 = r'\d+'
    text = re.sub(pattern_3, "", text)

    text = text.rstrip()
    text = text.lstrip()
    
    return text
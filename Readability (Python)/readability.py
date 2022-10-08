import cs50
letters = 0
words = 1
sentences = 0
text = cs50.get_string("Text: ")
for i in range(0, len(text)):
    if text[i] >= 'a' and text[i] <= 'z' or text[i] >= 'A' and text[i] <= 'Z':
        letters = letters + 1
    elif text[i] == ' ':
        words = words + 1
    elif text[i] == '.' or text[i] == '!' or text[i] == '?':
        sentences = sentences + 1
L = (letters * 100) / words
S = (sentences * 100) / words
index = 0.0588 * L - 0.296 * S - 15.8
if index < 1:
    print("Before Grade 1")
elif index > 16:
    print("Grade 16+")
else:
    print(f"Grade {round(index)}")
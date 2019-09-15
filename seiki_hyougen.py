import re
text = "abc123def456ghi,HP１２３４；：　ある意味koreｇa"
new_text = re.sub(r"[a-z]", "", text)
print(new_text) 

new_text = re.sub(r"[^a-z]", "", text)
print(new_text)
with open('src/dashboard.py', 'rb') as f:
    content = f.read()
content = content.decode('utf-8', errors='ignore')
with open('src/dashboard.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed!')
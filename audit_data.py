import json

with open('data/surnames.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('Total entries:', len(data))

# Duplicates in same community
seen = {}
duplicates = []
for x in data:
    key = (x['surname'].lower().strip(), x['community'].lower().strip())
    if key in seen:
        duplicates.append((seen[key], x['id'], x['surname'], x['community']))
    else:
        seen[key] = x['id']

print(f'Duplicates ({len(duplicates)}):')
for d in duplicates:
    print(' ', d)

print('\nCheck oddities:')
oddities = []
for x in data:
    s = x['surname']
    c = x['community']
    cat = x['category']
    sub = x['subcaste_or_clan']
    
    # Check for Khas names mislabeled as Newar
    if 'newar' in cat.lower() and s in ['Acharya', 'Agnihotri', 'Bhatta', 'Dev', 'Giri', 'Jha', 'Mishra', 'Sharma', 'Shukla']:
        oddities.append((x['id'], s, c, cat, sub, 'Dubious Newar title/Brahmin entry'))
    if c.lower() == 'rai' and s in ['Chaurasiya']:
        oddities.append((x['id'], s, c, cat, sub, 'Misclassified Terai caste as Rai'))
    if 'tharu' in c.lower() and s in ['Khas']:
        oddities.append((x['id'], s, c, cat, sub, 'Khas in Tharu'))
    if 'tamang' in c.lower() and s in ['Sahi']:
        oddities.append((x['id'], s, c, cat, sub, 'Sahi in Tamang'))

for o in oddities:
    print(' ', o)

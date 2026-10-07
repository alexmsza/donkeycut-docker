#!/usr/bin/env python3
path = '/home/alexmsza/DonkeyUseCorp/Donkey/site/.env'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
has_auth_url = False
for line in lines:
    if line.startswith('DATABASE_URL='):
        new_lines.append('DATABASE_URL="postgresql://postgres:postgrespassword@postgres:5432/donkey?sslmode=disable"\n')
    elif line.startswith('DIRECT_URL='):
        new_lines.append('DIRECT_URL="postgresql://postgres:postgrespassword@postgres:5432/donkey?sslmode=disable"\n')
    elif line.startswith('BETTER_AUTH_URL='):
        new_lines.append('BETTER_AUTH_URL="http://localhost:3000"\n')
        has_auth_url = True
    else:
        new_lines.append(line)

if not has_auth_url:
    new_lines.append('BETTER_AUTH_URL="http://localhost:3000"\n')

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print('Updated .env successfully')

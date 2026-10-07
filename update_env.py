#!/usr/bin/env python3
path = '/home/alexmsza/DonkeyUseCorp/Donkey/site/.env'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith('DATABASE_URL='):
        new_lines.append('DATABASE_URL="postgresql://postgres:postgrespassword@postgres:5432/donkey?sslmode=disable"\n')
    elif line.startswith('DIRECT_URL='):
        new_lines.append('DIRECT_URL="postgresql://postgres:postgrespassword@postgres:5432/donkey?sslmode=disable"\n')
    elif line.startswith('DONKEY_DEV_AUTH_BYPASS='):
        new_lines.append('DONKEY_DEV_AUTH_BYPASS=1\n')
    elif line.startswith('BETTER_AUTH_SECRET='):
        new_lines.append('BETTER_AUTH_SECRET="dev-secret-key-12345678901234567890"\n')
    else:
        new_lines.append(line)

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print('.env updated successfully')

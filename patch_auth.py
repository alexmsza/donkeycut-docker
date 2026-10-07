#!/usr/bin/env python3
path = '/home/alexmsza/DonkeyUseCorp/Donkey/site/src/lib/auth.ts'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

target = 'const baseURL = process.env.VERCEL ? DONKEYCUT_CANONICAL : undefined;'
replacement = 'const baseURL = process.env.BETTER_AUTH_URL ?? (process.env.VERCEL ? DONKEYCUT_CANONICAL : undefined);'
content = content.replace(target, replacement)

target2 = ': {};'
replacement2 = ': {\n      trustedOrigins: ["http://localhost:3000", "http://127.0.0.1:3000"],\n    };'
content = content.replace(target2, replacement2, 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Patched auth.ts successfully')

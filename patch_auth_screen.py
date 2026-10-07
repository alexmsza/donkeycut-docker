#!/usr/bin/env python3
path = '/home/alexmsza/DonkeyUseCorp/Donkey/site/src/app/_components/landing/AuthScreen.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

target = '''      {method === "email" ? <EmailAuthForm mode={mode} /> : <button
        type="button"
        aria-label={screenCopy.googleAlt}
        disabled={isPending}
        onClick={handleGoogleAuth}
        className={cn(
          "inline-flex border-none bg-transparent p-0",
          isPending ? "cursor-default opacity-60" : "cursor-pointer",
        )}
      >
        <Image
          src={screenCopy.googleSrc}
          alt={screenCopy.googleAlt}
          width={screenCopy.googleWidth}
          height={40}
          priority
          unoptimized
          className="block h-14"
          style={{ width: googleButtonWidth }}
        />
      </button>}'''

replacement = '''      {method === "email" ? (
        <>
          <EmailAuthForm mode={mode} />
          <div className="mt-3">
            <Link
              href={mode === "sign-in" ? "/sign-in" : "/sign-up"}
              className="text-xs text-[#666] underline hover:text-ink"
            >
              Ou entrar com conta Google
            </Link>
          </div>
        </>
      ) : (
        <>
          <button
            type="button"
            aria-label={screenCopy.googleAlt}
            disabled={isPending}
            onClick={handleGoogleAuth}
            className={cn(
              "inline-flex border-none bg-transparent p-0",
              isPending ? "cursor-default opacity-60" : "cursor-pointer",
            )}
          >
            <Image
              src={screenCopy.googleSrc}
              alt={screenCopy.googleAlt}
              width={screenCopy.googleWidth}
              height={40}
              priority
              unoptimized
              className="block h-14"
              style={{ width: googleButtonWidth }}
            />
          </button>
          <div className="mt-3">
            <Link
              href={`${mode === "sign-in" ? "/sign-in" : "/sign-up"}?method=email`}
              className="text-xs font-medium text-[#666] underline hover:text-ink"
            >
              Ou entrar com E-mail e Senha
            </Link>
          </div>
        </>
      )}'''

if target in content:
    content = content.replace(target, replacement)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Patched AuthScreen.tsx successfully')
else:
    print('Target not found in AuthScreen.tsx')

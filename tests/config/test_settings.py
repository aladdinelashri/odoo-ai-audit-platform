from database.config.settings import settings

print()
print("=" * 70)
print("SETTINGS")
print("=" * 70)
print()

print("Host      :", settings.database.host)
print("Port      :", settings.database.port)
print("Database  :", settings.database.database)
print("User      :", settings.database.user)

print()

if settings.database.password:
    print("Password  : ********")
else:
    print("Password  : NOT SET")

print()
print("Settings loaded successfully.")
print()

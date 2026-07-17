from database.discovery.discovery_engine import DiscoveryEngine


engine = DiscoveryEngine()

result = engine.discover()

print()

print("=" * 80)
print("DISCOVERY ENGINE")
print("=" * 80)

print()

print("Models      :", len(result["models"]))
print("Relations   :", len(result["relations"]))
print("Semantic    :", len(result["semantic"]))
print("Statistics  :", result["statistics"])

print()

assert len(result["models"]) > 0
assert len(result["semantic"]) > 0

print("DISCOVERY ENGINE OK")

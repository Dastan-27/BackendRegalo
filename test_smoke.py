"""Quick smoke test for the backend logic layer."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app.main import app
print("✅ app loaded successfully")

from app.services import (
    listar_emociones,
    listar_cartas,
    carta_aleatoria,
    obtener_carta_por_id,
    obtener_extras,
)

# 1. Emociones
emociones = listar_emociones()
assert len(emociones) == 8, f"Expected 8 emociones, got {len(emociones)}"
print(f"✅ /api/emociones → {len(emociones)} categorías")

# 2. Todas las cartas
cartas = listar_cartas()
assert len(cartas) == 48, f"Expected 48 cartas, got {len(cartas)}"
for c in cartas:
    assert "audio_url" in c and c["audio_url"].startswith("/static/audios/")
print(f"✅ /api/cartas → {len(cartas)} cartas, audio_url presente en todas")

# 3. Filtrar por emoción
filtradas = listar_cartas("insegura")
assert len(filtradas) == 6
assert filtradas[0]["emocion_id"] == "insegura"
print("✅ /api/cartas?emocion_id=insegura → 1 carta correcta")

# 4. Aleatoria global
al = carta_aleatoria()
assert "audio_url" in al
print(f"✅ /api/cartas/aleatoria → {al['id']}")

# 5. Aleatoria por emoción
al2 = carta_aleatoria("extrano")
assert al2["emocion_id"] == "extrano"
print(f"✅ /api/cartas/aleatoria?emocion_id=extrano → {al2['id']}")

# 6. Por ID
c = obtener_carta_por_id("feliz_01")
assert c["id"] == "feliz_01"
assert c["audio_url"] == "/static/audios/feliz_01.m4a"
print(f"✅ /api/cartas/feliz_01 → OK")

# 7. 404
try:
    obtener_carta_por_id("no_existe")
    assert False, "Should have raised"
except Exception as e:
    assert "404" in str(e.status_code)
    print(f"✅ /api/cartas/no_existe → 404 correctamente")

# 8. Extras
extras = obtener_extras()
assert extras["audio_amor_url"] == "/static/audios/amor_01.m4a"
assert len(extras["audios_amor_urls"]) >= 1
assert "link_broma_final" in extras
print(f"✅ /api/extras → audio_amor_url={extras['audio_amor_url']}, audios={len(extras['audios_amor_urls'])}")

print("\n🎉 Todos los tests pasaron correctamente!")


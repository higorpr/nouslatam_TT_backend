import time
import os

print("--- O SCRIPT hello.py COMEÇOU A RODAR ---")
print(f"Python está funcionando!")
print(f"Lendo a SECRET_KEY: {bool(os.getenv('SECRET_KEY'))}")
print("--- TESTE CONCLUÍDO. O CONTAINER IRÁ 'DORMIR' AGORA. ---")

# Mantém o container vivo para podermos inspecionar
time.sleep(3600)
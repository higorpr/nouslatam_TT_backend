# wait_for_db.py

import os
import time
import sys
import psycopg2
from psycopg2 import OperationalError

def wait_for_db():
    """
    Espera o banco de dados ficar disponível.
    """
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("Variável de ambiente DATABASE_URL não definida.", file=sys.stderr)
        sys.exit(1)

    print("Aguardando o banco de dados...")
    retries = 15
    while retries > 0:
        try:
            # Tenta se conectar ao banco
            conn = psycopg2.connect(db_url)
            conn.close()
            print("Banco de dados pronto!")
            return
        except OperationalError:
            retries -= 1
            print("Banco de dados indisponível, esperando 2 segundos...")
            time.sleep(2)
    
    print("Não foi possível conectar ao banco de dados após várias tentativas.", file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    wait_for_db()
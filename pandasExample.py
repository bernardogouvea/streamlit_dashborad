import pandas as pd
import psycopg2
from psycopg2 import sql

# 1. Ler os dados da planilha ODS usando Pandas
file_path = '/mnt/data/gastosCartaoJulho.ods'

# Vamos supor que a planilha tem uma única folha chamada "Sheet1"
df = pd.read_excel(file_path, engine='odf', sheet_name='Sheet1')

# Mostra os primeiros registros para verificação
print(df.head())

# 2. Conectar ao banco de dados PostgreSQL
conn = psycopg2.connect(
    dbname="seu_banco_de_dados",
    user="seu_usuario",
    password="sua_senha",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# 3. Inserir os dados na tabela correspondente
# Supondo que a tabela seja chamada 'gastos_cartao' e que as colunas correspondam às do DataFrame

for index, row in df.iterrows():
    cursor.execute(
        sql.SQL("INSERT INTO gastos_cartao (coluna1, coluna2, coluna3) VALUES (%s, %s, %s)"),
        [row['coluna1'], row['coluna2'], row['coluna3']]
    )

# 4. Confirmar transações e fechar a conexão
conn.commit()
cursor.close()
conn.close()

print("Dados inseridos com sucesso!")

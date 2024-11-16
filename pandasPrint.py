import pandas as pd


# 1. Definir o caminho do arquivo
file_path = '/home/bernardo/Documentos/PJe/documentos/gastosCartaoJulho.ods'

# 2. Ler os dados da planilha ODS usando Pandas
# Usando o engine 'odf' que é adequado para arquivos ODS
df = pd.read_excel(file_path, engine='odf')

# 3. Imprimir os primeiros registros para verificar os dados
print("Cabecalho")
print(df.head())

# 4. Se desejar imprimir todos os registros
print("Conteudo")
print(df)

# Se houver necessidade de imprimir de forma mais legível, pode usar o loop:
for index, row in df.iterrows():
    print(row)

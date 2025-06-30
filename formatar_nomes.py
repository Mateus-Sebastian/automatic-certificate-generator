# Nome do arquivo de entrada
arquivo_nomes = 'name-data.txt'

# Abrir o arquivo para leitura
with open(arquivo_nomes, 'r', encoding='utf-8') as arquivo:
    linhas = arquivo.readlines()

# Converter cada linha para maiúsculas e remover quebras de linha extras
linhas_maiusculas = [linha.strip().upper() + '\n' for linha in linhas]

# Escrever de volta no mesmo arquivo
with open(arquivo_nomes, 'w', encoding='utf-8') as arquivo:
    arquivo.writelines(linhas_maiusculas)

print("Nomes convertidos para MAIÚSCULAS com sucesso!")
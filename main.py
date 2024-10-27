import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Função para ler a matriz e a máscara do arquivo
def ler_arquivo_matriz_mascara(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        
    matriz = []
    mascara = []
    leitura_matriz = False
    leitura_mascara = False
    
    for line in lines:
        line = line.strip()
        if line == "MATRIZ":
            leitura_matriz = True
            leitura_mascara = False
        elif line == "MASCARA":
            leitura_mascara = True
            leitura_matriz = False
        elif leitura_matriz and line:
            matriz.append(list(map(int, line.split())))
        elif leitura_mascara and line:
            mascara.append(list(map(int, line.split())))
    
    matriz = np.array(matriz)
    mascara = np.array(mascara)
    return matriz, mascara

# Carregar a matriz e a máscara a partir do arquivo matrix.txt
matriz, mascara = ler_arquivo_matriz_mascara('matrix.txt')

# Função para extrair submatriz, aplicar a máscara e calcular as somas
def calcular_somas_padroes(matriz, x, y):
    submatriz = matriz[x-1:x+2, y-1:y+2]  # Extrai submatriz 3x3 centrada em (x, y)
    
    # Se a submatriz não for do tamanho 3x3, retorna None
    if submatriz.shape != (3, 3):
        return None
    
    submatriz_mascarada = submatriz * mascara
    soma_absoluta = np.sum(submatriz_mascarada)
    
    maximo = np.max(submatriz_mascarada)
    minimo = np.min(submatriz_mascarada[submatriz_mascarada > 0])  # Ignorar os zeros
    
    return soma_absoluta, maximo, minimo, submatriz_mascarada

# Inicializar uma matriz de controle para marcar posições já usadas
linhas, colunas = matriz.shape
marcador = np.zeros((linhas, colunas), dtype=bool)

# Armazenar posições válidas e resultados
posicoes_validas = []
resultados = []
somas_absolutas = []  # Lista para armazenar as somas absolutas

# Encontrar todas as submatrizes 3x3 válidas sem sobreposição
for x in range(1, linhas - 1):
    for y in range(1, colunas - 1):
        # Verificar se a posição e a área 3x3 ao redor estão disponíveis
        if not np.any(marcador[x-1:x+2, y-1:y+2]):
            resultado = calcular_somas_padroes(matriz, x, y)
            if resultado is not None:
                soma_abs, maximo, minimo, submatriz_mascarada = resultado
                posicoes_validas.append((x, y))
                resultados.append((soma_abs, maximo, minimo))
                somas_absolutas.append(soma_abs)  # Adiciona a soma absoluta na lista
                # Marcar as posições da submatriz 3x3 como usadas
                marcador[x-1:x+2, y-1:y+2] = True

# Visualizar a matriz e as posições possíveis
plt.figure(figsize=(8, 6))
sns.heatmap(matriz, annot=True, cmap="coolwarm", cbar=True, annot_kws={"color": "black"})

# Marcar as posições válidas onde o padrão pode ser encontrado
for (x, y) in posicoes_validas:
    plt.gca().add_patch(plt.Rectangle((y-1, x-1), 3, 3, fill=False, edgecolor='black', lw=2))

plt.title('Posições válidas para o padrão ABC-D-EFG')

plt.savefig("matriz.png")

# Exibir os resultados de somas
for idx, (x, y) in enumerate(posicoes_validas):
    soma_abs, maximo, minimo = resultados[idx]
    print(f"Posição central ({x}, {y}):")
    print(f"  Soma absoluta: {soma_abs}")
    print(f"  Máximo: {maximo}")
    print(f"  Mínimo: {minimo}")

# Exibir o maior e menor padrão encontrado

maior_padrao = max(somas_absolutas)
menor_padrao = min(somas_absolutas)
print(f"\nMaior padrão encontrado (soma absoluta): {maior_padrao}")
print(f"Menor padrão encontrado (soma absoluta): {menor_padrao}")

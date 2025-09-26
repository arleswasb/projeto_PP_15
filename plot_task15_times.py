import pandas as pd
import matplotlib.pyplot as plt
import os
import re

# Nomes dos arquivos de saída gerados pelo script shell
FILENAMES = [
    "time_v1_blocking.txt",
    "time_v2_wait.txt",
    "time_v3_overlap.txt"
]

# Rótulos para o gráfico (descrição da estratégia)
LABELS = [
    "1. Bloqueante (Baseline)",
    "2. Não Bloqueante (Wait)",
    "3. Sobreposição (Test)"
]

def extract_time_from_file(filename):
    """Lê o arquivo, extrai a última linha e faz o parsing do tempo."""
    if not os.path.exists(filename):
        print(f"Erro: Arquivo não encontrado: {filename}")
        return None
    
    with open(filename, 'r') as f:
        # Lê todas as linhas
        lines = f.readlines()
        
        # A última linha contém o resultado da medição do rank 0
        if lines:
            last_line = lines[-1].strip()
            
            # Expressão regular para encontrar um número float (o tempo) no final da linha
            # Ex: "Versao X (...): 0.107190 s" -> queremos 0.107190
            match = re.search(r'([\d\.]+)\s+s$', last_line)
            
            if match:
                try:
                    return float(match.group(1))
                except ValueError:
                    print(f"Aviso: Não foi possível converter o tempo em {filename}.")
                    return None
            else:
                print(f"Aviso: Não foi possível extrair o tempo da última linha em {filename}.")
                print(f"Linha: {last_line}")
                return None
        return None

def generate_comparison_plot(filenames, labels):
    """Gera o gráfico de barras comparando os tempos das três versões."""
    
    times = []
    
    # Extrai o tempo de cada arquivo
    for filename in filenames:
        time = extract_time_from_file(filename)
        if time is not None:
            times.append(time)
        else:
            # Usa 0 ou um valor de erro se o parsing falhar
            times.append(0.0) 
            
    # Cria o DataFrame
    df = pd.DataFrame({
        'Estratégia': labels,
        'Tempo (s)': times
    })

    # Verifica se a V3 é a mais rápida (para a análise de cor do gráfico)
    is_v3_fastest = (df.loc[df['Estratégia'] == LABELS[2], 'Tempo (s)'].iloc[0] == df['Tempo (s)'].min())

    # Define as cores: destaca a Versão 3 (Sobreposição)
    colors = ['skyblue', 'lightcoral', 'lightgreen']
    if not is_v3_fastest:
         colors = ['skyblue', 'lightcoral', 'gray'] # Se não for a mais rápida, não destaca
         
    # Cria o gráfico de barras
    plt.figure(figsize=(10, 6))
    bars = plt.bar(df['Estratégia'], df['Tempo (s)'], color=colors)
    
    # Adiciona os valores nas barras
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + df['Tempo (s)'].max() * 0.01, 
                 f'{yval:.6f}', ha='center', va='bottom', fontsize=9)

    # Configurações do gráfico
    plt.title('Comparação de Tempo de Execução: Escondendo Latência (Tarefa 15)', fontsize=14)
    plt.ylabel('Tempo Total de Execução (segundos)', fontsize=12)
    plt.xlabel('Estratégia de Comunicação', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Salva o gráfico
    plt.tight_layout()
    plt.savefig('comparacao_desempenho_T15.png')
    
    print("\n----------------------------------------------------")
    print("✅ Gráfico 'comparacao_desempenho_T15.png' gerado com sucesso!")
    if is_v3_fastest:
        print("   A Versão 3 (Sobreposição) foi a mais rápida. (Sucesso Teórico!)")
    else:
        print("   A Versão 3 NÃO foi a mais rápida. (Análise Crucial no Relatório!)")
    print("----------------------------------------------------\n")

if __name__ == "__main__":
    generate_comparison_plot(FILENAMES, LABELS)

# Tarefa 15: Escondendo Latência com Sobreposição de Computação e Comunicação

## 🎯 Objetivo

O objetivo desta tarefa é provar a eficácia da comunicação não bloqueante (\\texttt{MPI\_Isend}/\\texttt{MPI\_Irecv}) na mitigação do custo fixo de rede (latência, $\\tau$) por meio da técnica de **sobreposição de computação e comunicação**.

A tarefa compara o tempo de execução de três implementações da simulação de Difusão de Calor 1D, um problema que requer a troca de bordas (*Halo Exchange*) a cada passo de tempo.

## 🛠️ Configuração do Problema

O ganho da Versão 3 é dependente da granularidade do trabalho. Os parâmetros do problema foram ajustados para que o tempo de computação local fosse baixo, maximizando o peso relativo da latência:

| Parâmetro | Valor | Detalhe |
| :--- | :--- | :--- |
| **Domínio Global** ($\\text{GLOBAL\_N}$) | \\textbf{10.000} | Tamanho total da barra 1D. |
| **Passos de Tempo** ($\\text{STEPS}$) | \\textbf{10.000} | Alto número de iterações para acumular o custo de latência. |
| **Número de Processos** ($\\text{NP}$) | **2, 4 e 8** | Variação utilizada para provar a tese de que o ganho aumenta com a concorrência. |

## 📁 Estrutura e Versões do Código

O projeto é composto por três versões, que só diferem na estratégia de sincronização:

| Versão | Arquivo C | Primitivas Usadas | Análise |
| :--- | :--- | :--- | :--- |
| **V1: Bloqueante (Baseline)** | \\texttt{heat\_diffusion\_v1\_blocking.c} | \\texttt{MPI\_Send} / \\texttt{MPI\_Recv} | Exposto totalmente à latência ($\\tau$). |
| **V2: Não Bloqueante (Espera)** | \\texttt{heat\_diffusion\_v2\_wait.c} | \\texttt{MPI\_Isend} / \\texttt{MPI\_Irecv} + \\texttt{MPI\_Wait} | Inicia a comunicação, mas espera imediatamente. Tempo similar à V1. |
| **V3: Sobreposição (Otimizada)** | \\texttt{heat\_diffusion\_v3\_overlap.c} | \\texttt{MPI\_Isend} / \\texttt{MPI\_Irecv} + \\texttt{MPI\_Test} | Inicia a comunicação e realiza a computação interna (não dependente) enquanto a rede trabalha. |

## 🚀 Como Compilar e Executar o Benchmark

O script de automação é essencial para compilar corretamente as três versões e executar a medição de tempo de forma consistente.

### 1\. Compilação (Uma vez)

Compile os três arquivos-fonte para criar os executáveis:

```bash
mpicc -o difusão_bloqueante.c
mpicc -o difusão_Nao_bloqueante_wait.c
mpicc -o difusão_Nao_bloqueante_test.c
```

### 2\. Execução Automatizada

O script \\texttt{run\_simples.sh} executa as três versões e salva a saída de tempo para o processamento Python.

1.  **Dê permissão de execução:**
    ```bash
    chmod +x run_simples.sh
    ```
2.  **Execute o script:**
    ```bash
    # ATENÇÃO: Edite o script para definir o NUM_PROCESSOS (2, 4 ou 8) antes de rodar.
    ./run_simples.sh
    ```

**Resultado:** Criação de três arquivos de tempo (\\texttt{time\_v1\_blocking.txt}, \\texttt{time\_v2\_wait.txt}, \\texttt{time\_v3\_overlap.txt}).

### 3\. Geração do Gráfico

O script Python (\\texttt{plot\_task15\_times.py}) lerá os arquivos gerados e criará o gráfico de barras comparativo.

```bash
python3 plot_task15_times.py
```

## 📈 Análise Esperada (O Ganho da Sobreposição)

Para $P=8$ processos (cenário de Latência Dominante), o resultado ideal deve ser:

1.  \\textbf{V3 (Sobreposição) \< V2 (Wait) \< V1 (Bloqueante)}.
2.  O \\textbf{ganho substancial} na Versão 3 (aproximadamente $\\mathbf{37%}$ em relação à V1) comprova que o tempo de computação útil da simulação interna foi suficiente para esconder o custo da latência de comunicação da rede.
3.  O ganho só se manifesta significativamente em cenários de alta concorrência onde a latência é o fator limitante.


## Autor

* **Werbert Arles de Souza Barradas**

-----

**Disciplina:** DCA3703 - Programação Paralela - T01 (2025.2)  
**Docente:** Professor Doutor Samuel Xavier de Souza  
**Instituição:** Universidade Federal do Rio Grande do Norte (UFRN)
#!/bin/bash

# ===============================================
# CONFIGURAÇÕES
# ===============================================

# Número de processos (P): Ajuste este valor (ex: 4, 8, 16)
NUM_PROCESSOS=8 

# Nomes dos executáveis
V1_EXE="difusão_bloqueante"
V2_EXE="difusão_Nao_bloqueante_wait"
V3_EXE="difusão_Nao_bloqueante_test"

# Nomes dos arquivos de saída para o Python
V1_OUT="time_v1_blocking.txt"
V2_OUT="time_v2_wait.txt"
V3_OUT="time_v3_overlap.txt"

echo "--- 🛠️ INICIANDO BENCHMARK DA TAREFA 15 (NP=${NUM_PROCESSOS}) ---"

# Limpa saídas antigas (opcional)
rm -f ${V1_OUT} ${V2_OUT} ${V3_OUT}

# ===============================================
# EXECUÇÃO E CAPTURA DE TEMPOS
# ===============================================

# 1. Executa Versão 1 (Bloqueante)
echo "Executando V1 (Baseline)..."
mpirun -np ${NUM_PROCESSOS} ./${V1_EXE} > ${V1_OUT}

# 2. Executa Versão 2 (Wait)
echo "Executando V2 (Wait)..."
mpirun -np ${NUM_PROCESSOS} ./${V2_EXE} > ${V2_OUT}

# 3. Executa Versão 3 (Sobreposição)
echo "Executando V3 (Sobreposição)..."
mpirun -np ${NUM_PROCESSOS} ./${V3_EXE} > ${V3_OUT}

echo "----------------------------------------------------"
echo "✅ Execução concluída. Tempos salvos nos arquivos:"
echo "   - ${V1_OUT}"
echo "   - ${V2_OUT}"
echo "   - ${V3_OUT}"
echo ""
echo "Agora, utilize o script Python para processar e gerar o gráfico comparativo."

# FIM DO SCRIPT
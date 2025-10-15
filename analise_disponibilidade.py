

import os
import sys
import matplotlib.pyplot as plt
import numpy as np

def calcular_disponibilidade(mttf_horas, mttr_horas):
    """
    Calcula a disponibilidade de um único componente.
    A fórmula é: A = MTTF / (MTTF + MTTR)
    """
    if mttf_horas <= 0 or mttr_horas < 0:
        raise ValueError("MTTF deve ser um valor positivo e MTTR não pode ser negativo.")
    return mttf_horas / (mttf_horas + mttr_horas)

def gerar_graficos(componentes):
    """
    Gera e salva os gráficos da análise de disponibilidade.
    """
    print("\nGerando gráficos da análise...")
    
    nomes = [comp['nome'].replace('UFS', '').strip() for comp in componentes]
    disponibilidades = [calcular_disponibilidade(c['mttf_horas'], c['mttr_horas']) for c in componentes]
    
    # --- Gráfico 1: Gráfico de Barras de Disponibilidade por Componente ---
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(nomes, disponibilidades, color='steelblue')
    ax.set_ylabel('Disponibilidade (A)')
    ax.set_title('Disponibilidade Individual por Componente do Sistema')
    ax.set_ylim([max(0.99, min(disponibilidades) - 0.001), 1.0001])
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval*100:.4f}%', va='bottom', ha='center')
    plt.tight_layout()
    caminho_grafico1 = 'output/disponibilidade_componentes.png'
    plt.savefig(caminho_grafico1)
    print(f" -> Gráfico de barras salvo em: {caminho_grafico1}")
    plt.close()

    # --- Gráfico 2: Gráfico de Pizza da Contribuição para a Indisponibilidade ---
    indisponibilidades = [1 - a for a in disponibilidades]
    soma_indisponibilidades = sum(indisponibilidades)
    contribuicao = [(i / soma_indisponibilidades) * 100 for i in indisponibilidades]
    maior_contribuidor_idx = np.argmax(contribuicao)
    explode = [0] * len(nomes)
    explode[maior_contribuidor_idx] = 0.1
    fig2, ax2 = plt.subplots(figsize=(10, 8))
    ax2.pie(contribuicao, explode=explode, labels=nomes, autopct='%1.1f%%', shadow=True, startangle=90)
    ax2.axis('equal')
    ax2.set_title('Contribuição Percentual de Cada Componente para a Indisponibilidade Total')
    plt.tight_layout()
    caminho_grafico2 = 'output/contribuicao_indisponibilidade.png'
    plt.savefig(caminho_grafico2)
    print(f" -> Gráfico de pizza salvo em: {caminho_grafico2}")
    plt.close()

def modelo_disponibilidade_ufs():
    """
    Função principal que modela, calcula e gera relatórios da disponibilidade
    da conexão ao site da UFS.
    """
    componentes = [
        {"nome": "1. Equipamento Local", "mttf_horas": 2500.0, "mttr_horas": 4.0, "justificativa": "Equipamento de consumo (notebook/PC do usuário)."},
        {"nome": "2. Rede Interna UFS", "mttf_horas": 13000.0, "mttr_horas": 2.0, "justificativa": "Switches e roteadores de campus (enterprise-grade)."},
        {"nome": "3. Servidor Web UFS", "mttf_horas": 12000.0, "mttr_horas": 1.5, "justificativa": "Hardware de data center com alta confiabilidade."}
    ]

    print("="*80)
    print("Relatório de Análise de Disponibilidade da Conexão ao Site da UFS")
    print("="*80)
    print("Modelo de Componentes Derivado do Traceroute executado na rede interna da UFS:\n")
    print("[Equip. Local] ---> [Rede Interna UFS] ---> [Servidor Web UFS]\n")
    print("-"*80)

    disponibilidade_total = 1.0
    for comp in componentes:
        disponibilidade_comp = calcular_disponibilidade(comp['mttf_horas'], comp['mttr_horas'])
        disponibilidade_total *= disponibilidade_comp
        print(f"Componente: {comp['nome']}")
        print(f"  - MTTF: {comp['mttf_horas']:,.1f} horas | MTTR: {comp['mttr_horas']:.1f} horas")
        print(f"  - Disponibilidade (A_i): {disponibilidade_comp:.8f} ({disponibilidade_comp * 100:.6f}%)")
        print("-" * 50)

    indisponibilidade_total = 1.0 - disponibilidade_total
    indisponibilidade_anual_horas = indisponibilidade_total * 365 * 24
    dias = int(indisponibilidade_anual_horas // 24)
    horas = int(indisponibilidade_anual_horas % 24)
    minutos = int((indisponibilidade_anual_horas * 60) % 60)

    print("\n" + "="*80)
    print("Resultados Consolidados do Modelo")
    print("="*80)
    print(f"Disponibilidade Total do Sistema (A_total = Π A_i): {disponibilidade_total:.8f}")
    print(f"Disponibilidade Percentual (Classe de Nines): {disponibilidade_total * 100:.6f}%")
    print(f"\nIsso equivale a um tempo médio de inatividade anual de:")
    print(f" -> {indisponibilidade_anual_horas:.2f} horas por ano.")
    print(f" -> Aproximadamente: {dias} dias, {horas} horas e {minutos} minutos por ano.")
    print("="*80)

    gerar_graficos(componentes)
    
class Logger(object):
    def __init__(self, filename="output/relatorio_disponibilidade_ufs.txt"):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding='utf-8')
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
    def flush(self):
        pass

if __name__ == '__main__':
    if not os.path.exists('output'):
        os.makedirs('output')
    sys.stdout = Logger()
    modelo_disponibilidade_ufs()
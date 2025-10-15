

# Análise de Disponibilidade de Conexão com o Servidor da UFS

[](https://opensource.org/licenses/MIT)

Este repositório contém um script em Python desenvolvido como parte de uma atividade do Mestrado em Ciência da Computação. O objetivo do projeto é criar e analisar um modelo básico de disponibilidade para a conexão de rede entre um cliente local e o servidor web da Universidade Federal de Sergipe (UFS), utilizando a metodologia de Diagrama de Blocos de Confiabilidade (RBD).

## 📄 Sobre o Projeto

O script modela a conexão de rede como um sistema em série, onde a falha de qualquer componente resulta na indisponibilidade total do serviço. A análise se baseia em valores de **MTTF (Mean Time To Failure)** e **MTTR (Mean Time To Repair)** para cada componente, obtidos a partir da literatura acadêmica da área de confiabilidade de sistemas.

O modelo foi construído a partir de um `traceroute` real, executado de dentro da própria rede da UFS, resultando em um cenário mais acurado e simplificado.

### O Modelo de Disponibilidade

O `traceroute` executado revelou uma rota de rede interna, o que nos levou ao seguinte modelo RBD de 3 componentes em série:

`[Equipamento Local] ---> [Rede Interna UFS] ---> [Servidor Web UFS]`

  - **Equipamento Local:** O computador do usuário final.
  - **Rede Interna UFS:** A infraestrutura de rede do campus (switches, roteadores, firewalls).
  - **Servidor Web UFS:** O servidor que hospeda o site `www.ufs.br`.

## ✨ Funcionalidades

  - **Cálculo de Disponibilidade:** Calcula a disponibilidade individual de cada componente e a disponibilidade total do sistema.
  - **Relatório Detalhado:** Gera um relatório completo em formato `.txt` com todos os parâmetros, cálculos e resultados consolidados, incluindo o tempo de inatividade anual.
  - **Visualização de Dados:** Cria e salva automaticamente dois gráficos para análise visual:
    1.  Um **gráfico de barras** comparando a disponibilidade de cada componente.
    2.  Um **gráfico de pizza** mostrando a contribuição percentual de cada componente para a indisponibilidade total do sistema.

## 🛠️ Tecnologias Utilizadas

  - **Python 3**
  - **Matplotlib**
  - **NumPy**

## 🚀 Começando

Siga estas instruções para executar o projeto em sua máquina local.

### Pré-requisitos

  - Python 3.10 ou superior.

### Instalação e Execução

É altamente recomendado o uso de um ambiente virtual (`venv`) para evitar conflitos com pacotes do sistema.

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```

2.  **Crie e ative um ambiente virtual:**

    ```bash
    # Crie o ambiente
    python3 -m venv venv

    # Ative o ambiente (Linux/macOS)
    source venv/bin/activate

    # Ative o ambiente (Windows)
    .\venv\Scripts\activate
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

    *(Nota: Se não houver um arquivo `requirements.txt`, instale manualmente)*

    ```bash
    pip install matplotlib numpy
    ```

4.  **Execute o script:**

    ```bash
    python analise_disponibilidade.py
    ```

## 📈 Resultados Gerados

Após a execução, uma pasta chamada `output/` será criada no diretório raiz do projeto com os seguintes arquivos:

```
output/
├── contribuicao_indisponibilidade.png  # Gráfico de pizza
├── disponibilidade_componentes.png     # Gráfico de barras
└── relatorio_disponibilidade_ufs.txt   # Relatório textual completo
```


## 👨‍💻 Autor

  - **Marcos Vinícius** 
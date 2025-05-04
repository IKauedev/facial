# 🔐 Sistema de Reconhecimento Facial com OpenCV

Este é um sistema de controle de acesso baseado em **reconhecimento facial em tempo real** utilizando Python, OpenCV e SQLite. O sistema permite:

- Cadastrar usuários capturando seus rostos pela câmera
- Treinar um modelo de reconhecimento facial (LBPH)
- Validar o acesso de usuários com base em seus rostos
- Exibir uma janela interativa com feedback visual
- Registrar todos os reconhecimentos em um log CSV


## 🚀 Tecnologias Utilizadas

- **Python 3.10+**
- **OpenCV (opencv-contrib-python)**: para captura, detecção e reconhecimento facial
- **NumPy**: manipulação de arrays e dados de imagem
- **SQLite3**: banco de dados local para cadastro de usuários
- **winsound (Windows)**: para emitir som após reconhecimento
- **CSV**: registro dos acessos reconhecidos


## ⚙️ Requisitos

- Sistema operacional: Windows (ou Linux adaptado)
- Webcam funcional
- Python instalado (recomendado: 3.10 ou superior)

## 🧰 Instalação dos Pacotes

Abra o terminal na pasta do projeto e execute:


Aviso: caso não rode de primeira e recomendado a criação do (venv), para isto basta rodar o seguinte comando:

## Ambiente windows:

```bash
    python -m venv venv
```

## depois:

```bash
  venv\Scripts\activate.bat
```


## Ambiente linux


```bash
    python -m venv venv
```

## depois:


```bash
  source venv/bin/activate
```

### instalação das dependencias do projeto

```bash
  pip install requirements.txt -r
````

## Menu Inicial
Ao iniciar, o sistema exibirá o seguinte menu:

```bash
    1 - Cadastrar novo usuário
    2 - Fazer reconhecimento facial
```

## Cadastro de usuário

- Escolha a opção 1
- Informe o nome e o nível de acesso
- O sistema irá capturar 20 imagens do rosto via webcam
- O modelo será treinado automaticamente após a captura
-As imagens vão para a pasta /dataset e o modelo será salvo em /model/classifier.xml.

## Realizando o Reconhecimento
- Escolha a opção 2
- Uma janela será aberta com vídeo da câmera
-Quando o rosto for reconhecido com confiança suficiente (≥ 60%) em 5 quadros seguidos, o acesso será concedido
-Um beep sonoro será emitido e a identificação será registrada

## Log de Reconhecimentos
Todos os acessos reconhecidos são salvos no arquivo:
```bash
  log_recognitions.csv
```
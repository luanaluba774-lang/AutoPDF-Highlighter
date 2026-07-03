# AutoPDF Highlighter

Aplicação desktop desenvolvida em Python para destacar automaticamente palavras-chave em documentos PDF. O programa analisa o arquivo, identifica todas as ocorrências dos termos configurados e gera uma nova versão do documento com as marcações, preservando o arquivo original.

O projeto foi desenvolvido para facilitar a análise de documentos extensos, como contratos, editais, artigos e apostilas.

![status](https://img.shields.io/badge/status-concluído-brightgreen)
![python](https://img.shields.io/badge/python-3.10%2B-blue)



## Funcionalidades

* Seleção de arquivos por interface gráfica ou drag and drop
* Visualização da primeira página do PDF antes do processamento
* Cadastro e gerenciamento de palavras-chave com persistência em `keywords.json`
* Destaque automático de todas as ocorrências encontradas
* Processamento em segundo plano, mantendo a interface responsiva
* Exportação de relatório de ocorrências em formato CSV
* Abertura automática do PDF gerado
* Suporte aos temas claro e escuro

## Captura de tela

<img width="952" height="1015" alt="image" src="https://github.com/user-attachments/assets/2d6c6888-72b6-4c16-aa46-fb38c0c0e112" />

<img width="471" height="617" alt="image" src="https://github.com/user-attachments/assets/da4235d9-93d9-4908-b9b7-93efabd2c91a" />

<img width="1105" height="625" alt="image" src="https://github.com/user-attachments/assets/268ca093-80c1-4175-bafd-1d51bf2d77ec" />


<img width="537" height="220" alt="image" src="https://github.com/user-attachments/assets/aaf0a3da-c18f-41be-b2f1-936e47d21c2d" />



## Tecnologias

* Python 3.10+
* PyMuPDF
* CustomTkinter
* Pillow
* tkinterdnd2
* PyInstaller

## Instalação

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/autopdf-highlighter.git
cd autopdf-highlighter
```

Crie um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute a aplicação:

```bash
python main.py
```

## Gerando o executável

O projeto inclui scripts para geração do executável utilizando o PyInstaller.

```bash
# Windows
build.bat

# Linux/macOS
./build.sh
```

O executável será gerado na pasta `dist/`.

## Estrutura do projeto

```text
autopdf-highlighter/
├── main.py
├── keywords.json
├── requirements.txt
├── requirements-dev.txt
├── build.bat
├── build.sh
└── README.md
```

## Funcionamento

1. Selecione um arquivo PDF.
2. Informe as palavras-chave que deseja localizar.
3. O documento é processado utilizando o PyMuPDF.
4. Todas as ocorrências encontradas recebem uma anotação de destaque.
5. Um novo arquivo é salvo com o sufixo `_highlighted.pdf`, mantendo o documento original inalterado.

## Próximas melhorias

* [x] Suporte a drag and drop
* [x] Visualização da primeira página do PDF
* [x] Geração de executável com PyInstaller
* [x] Exportação de relatório em CSV
* [ ] Processamento de múltiplos PDFs


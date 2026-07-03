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
<img width="957" height="1017" alt="image" src="https://github.com/user-attachments/assets/2412f10a-06ce-4ac7-8bc2-2543eb936050" />
<img width="466" height="606" alt="image" src="https://github.com/user-attachments/assets/a0b9f4aa-142f-498e-beed-b6324e4a7ec8" />
<img width="937" height="585" alt="image" src="https://github.com/user-attachments/assets/ae23c97b-c406-48a1-b036-c10d519ad456" />
<img width="546" height="222" alt="image" src="https://github.com/user-attachments/assets/ae5aeefa-fb87-452a-a47c-041a30e209b5" />
<img width="977" height="826" alt="image" src="https://github.com/user-attachments/assets/b45348b9-d9f0-410e-9d0c-9c30b18e6027" />


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



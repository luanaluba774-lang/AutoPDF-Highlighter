# 📄 AutoPDF Highlighter

Aplicativo desktop em Python que destaca automaticamente palavras-chave em documentos PDF, gerando uma cópia grifada do arquivo original. Útil para acelerar a leitura de documentos extensos (contratos, editais, artigos, apostilas) onde é preciso localizar rapidamente termos específicos.

![status](https://img.shields.io/badge/status-concluído-brightgreen)
![python](https://img.shields.io/badge/python-3.10%2B-blue)
![license](https://img.shields.io/badge/license-MIT-lightgrey)

## ✨ Funcionalidades

- Seleção de PDF via drag & drop ou interface gráfica
- Preview em miniatura da primeira página do PDF selecionado
- Cadastro e gerenciamento de palavras-chave (persistidas em `keywords.json`)
- Destaque automático de todas as ocorrências no documento
- Processamento em segundo plano (a interface não trava durante a leitura do PDF)
- Relatório de ocorrências por palavra-chave, exportável em CSV
- Abertura automática do arquivo grifado ao final
- Interface moderna com suporte a tema claro/escuro

## 🖼️ Screenshot

<!-- Adicione um print da tela aqui, ex: -->
<!-- ![screenshot](assets/screenshot.png) -->

## 🛠️ Tecnologias

- [Python 3](https://www.python.org/)
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/) — leitura e manipulação de PDFs
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — interface gráfica
- [Pillow](https://pillow.readthedocs.io/) — geração da miniatura do PDF
- [tkinterdnd2](https://github.com/pmgagne/tkinterdnd2) — suporte a drag & drop
- [PyInstaller](https://pyinstaller.org/) — empacotamento em executável

## 🚀 Como executar

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/autopdf-highlighter.git
cd autopdf-highlighter

# Crie um ambiente virtual (opcional, mas recomendado)
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac

# Instale as dependências
pip install -r requirements.txt

# Execute
python main.py
```

## 📦 Gerando um executável (.exe)

O projeto já vem com scripts prontos usando [PyInstaller](https://pyinstaller.org/):

```bash
# Windows
build.bat

# Linux/Mac
./build.sh
```

O executável é gerado na pasta `dist/`.

## 📂 Estrutura do projeto

```
autopdf-highlighter/
├── main.py               # aplicação principal
├── keywords.json          # lista de palavras-chave salvas
├── requirements.txt       # dependências para rodar o app
├── requirements-dev.txt   # dependências extras para gerar o executável
├── build.bat / build.sh   # scripts de empacotamento (PyInstaller)
└── README.md
```

## 💡 Como funciona

1. O usuário seleciona um arquivo PDF.
2. Cadastra as palavras-chave que deseja localizar (ex: "Cláusula", "Confidencial", "Multa").
3. Ao clicar em "Processar PDF", o app percorre cada página do documento com o [PyMuPDF](https://pymupdf.readthedocs.io/), localiza as ocorrências de cada palavra e aplica uma anotação de destaque (highlight).
4. Um novo arquivo é salvo com o sufixo `_highlighted.pdf`, preservando o original.

## 📌 Melhorias futuras

- [x] Suporte a drag & drop de arquivos
- [x] Preview em miniatura do PDF antes de processar
- [x] Empacotamento como executável (`.exe`) via PyInstaller
- [x] Exportar relatório de ocorrências (quantidade por palavra)
- [ ] Suporte a múltiplos PDFs em lote
- [ ] Testes automatizados (pytest)

## 👨‍💻 Autor

Projeto desenvolvido por [seu nome] como parte dos estudos em Análise e Desenvolvimento de Sistemas (ADS).

- LinkedIn: [seu link]
- GitHub: [seu link]

## 📄 Licença

Este projeto está sob a licença MIT — veja o arquivo [LICENSE](LICENSE) para mais detalhes.

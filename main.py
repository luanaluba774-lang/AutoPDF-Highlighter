import fitz
import customtkinter as ctk
from tkinter import filedialog, messagebox
import json
import os
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

KEYWORDS_FILE = "keywords.json"


# =========================
# DATA
# =========================
def load_keywords():
    if os.path.exists(KEYWORDS_FILE):
        with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_keywords(keywords):
    with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(keywords, f, ensure_ascii=False, indent=4)


# =========================
# APP
# =========================
class AutoPDFApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AutoPDF Highlighter")
        self.geometry("620x680")
        self.minsize(560, 600)

        self.pdf_path = ""
        self.keywords = load_keywords()
        self.chip_widgets = []

        self._build_ui()
        self._render_keywords()

    # ---------- UI BUILD ----------
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)

        # HEADER
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=24, pady=(24, 8))
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header, text="📄 AutoPDF Highlighter",
            font=ctk.CTkFont(size=22, weight="bold")
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            header, text="Destaque palavras-chave em PDFs automaticamente",
            font=ctk.CTkFont(size=13), text_color="gray60"
        ).grid(row=1, column=0, sticky="w")

        self.switch_theme = ctk.CTkSwitch(
            header, text="Modo claro", command=self._toggle_theme, width=40
        )
        self.switch_theme.grid(row=0, column=1, rowspan=2, sticky="e")

        # PDF CARD
        pdf_card = ctk.CTkFrame(self, corner_radius=12)
        pdf_card.grid(row=1, column=0, sticky="ew", padx=24, pady=8)
        pdf_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            pdf_card, text="Arquivo PDF", font=ctk.CTkFont(size=13, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(12, 0))

        row = ctk.CTkFrame(pdf_card, fg_color="transparent")
        row.grid(row=1, column=0, sticky="ew", padx=16, pady=(6, 16))
        row.grid_columnconfigure(0, weight=1)

        self.label_pdf = ctk.CTkLabel(
            row, text="Nenhum PDF selecionado", text_color="gray60", anchor="w"
        )
        self.label_pdf.grid(row=0, column=0, sticky="ew")

        ctk.CTkButton(
            row, text="Selecionar", width=110, command=self.select_pdf
        ).grid(row=0, column=1, padx=(12, 0))

        # KEYWORDS CARD
        kw_card = ctk.CTkFrame(self, corner_radius=12)
        kw_card.grid(row=2, column=0, sticky="nsew", padx=24, pady=8)
        kw_card.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            kw_card, text="Palavras-chave", font=ctk.CTkFont(size=13, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(12, 0))

        entry_row = ctk.CTkFrame(kw_card, fg_color="transparent")
        entry_row.grid(row=1, column=0, sticky="ew", padx=16, pady=(8, 8))
        entry_row.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(entry_row, placeholder_text="Digite e pressione Enter...")
        self.entry.grid(row=0, column=0, sticky="ew")
        self.entry.bind("<Return>", lambda e: self.add_keyword())

        ctk.CTkButton(
            entry_row, text="Adicionar", width=100, command=self.add_keyword
        ).grid(row=0, column=1, padx=(8, 0))

        self.chips_frame = ctk.CTkScrollableFrame(kw_card, fg_color="transparent", height=220)
        self.chips_frame.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 12))
        kw_card.grid_rowconfigure(2, weight=1)

        # ACTION
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.grid(row=3, column=0, sticky="ew", padx=24, pady=(8, 24))
        action_frame.grid_columnconfigure(0, weight=1)

        self.progress = ctk.CTkProgressBar(action_frame, mode="indeterminate")
        self.status_label = ctk.CTkLabel(action_frame, text="", text_color="gray60")
        self.status_label.grid(row=0, column=0, sticky="w", pady=(0, 6))

        self.btn_process = ctk.CTkButton(
            action_frame, text="PROCESSAR PDF", height=42,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.process_pdf
        )
        self.btn_process.grid(row=2, column=0, sticky="ew", pady=(6, 0))

    # ---------- ACTIONS ----------
    def _toggle_theme(self):
        mode = "light" if self.switch_theme.get() else "dark"
        ctk.set_appearance_mode(mode)

    def select_pdf(self):
        path = filedialog.askopenfilename(filetypes=[("PDF", "*.pdf")])
        if path:
            self.pdf_path = path
            self.label_pdf.configure(text=os.path.basename(path), text_color=("black", "white"))

    def add_keyword(self):
        k = self.entry.get().strip()
        if k and k not in self.keywords:
            self.keywords.append(k)
            self.entry.delete(0, "end")
            save_keywords(self.keywords)
            self._render_keywords()

    def remove_keyword(self, word):
        self.keywords.remove(word)
        save_keywords(self.keywords)
        self._render_keywords()

    def _render_keywords(self):
        for w in self.chip_widgets:
            w.destroy()
        self.chip_widgets = []

        if not self.keywords:
            empty = ctk.CTkLabel(
                self.chips_frame, text="Nenhuma palavra-chave adicionada",
                text_color="gray50"
            )
            empty.pack(pady=20)
            self.chip_widgets.append(empty)
            return

        for word in self.keywords:
            chip = ctk.CTkFrame(self.chips_frame, corner_radius=8, fg_color=("gray85", "gray25"))
            chip.pack(fill="x", pady=3, padx=2)

            ctk.CTkLabel(chip, text=word, anchor="w").pack(
                side="left", padx=(10, 4), pady=6, fill="x", expand=True
            )
            ctk.CTkButton(
                chip, text="✕", width=28, height=24, fg_color="transparent",
                hover_color=("gray70", "gray35"), text_color=("gray30", "gray80"),
                command=lambda w=word: self.remove_keyword(w)
            ).pack(side="right", padx=6, pady=4)

            self.chip_widgets.append(chip)

    def process_pdf(self):
        if not self.pdf_path:
            messagebox.showerror("Erro", "Selecione um PDF")
            return
        if not self.keywords:
            messagebox.showerror("Erro", "Adicione palavras-chave")
            return

        self.btn_process.configure(state="disabled", text="Processando...")
        self.status_label.configure(text="Lendo e destacando o PDF...")
        self.progress.grid(row=1, column=0, sticky="ew", pady=(0, 4))
        self.progress.start()

        thread = threading.Thread(target=self._run_processing, daemon=True)
        thread.start()

    def _run_processing(self):
        try:
            doc = fitz.open(self.pdf_path)
            total = 0

            for page in doc:
                text = page.get_text("text")
                for word in self.keywords:
                    if word.lower() not in text.lower():
                        continue
                    try:
                        areas = page.search_for(word, quads=True)
                        if not areas:
                            continue
                        page.add_highlight_annot(areas)
                        total += len(areas)
                    except Exception:
                        # Não deixa uma palavra problemática derrubar o processo inteiro
                        continue

            output = self.pdf_path.replace(".pdf", "_highlighted.pdf")
            doc.save(output)
            doc.close()

            self.after(0, self._on_success, total, output)
        except Exception as e:
            self.after(0, self._on_error, str(e))

    def _on_success(self, total, output):
        self.progress.stop()
        self.progress.grid_forget()
        self.status_label.configure(text=f"Salvo em: {os.path.basename(output)}")
        self.btn_process.configure(state="normal", text="PROCESSAR PDF")
        self._open_file(output)
        messagebox.showinfo("Concluído", f"Destaques aplicados: {total}\nArquivo: {output}")

    def _open_file(self, path):
        try:
            if os.name == "nt":
                os.startfile(path)
            elif os.uname().sysname == "Darwin":
                os.system(f'open "{path}"')
            else:
                os.system(f'xdg-open "{path}"')
        except Exception:
            pass  # abrir automaticamente é um "bônus", não deve travar o fluxo

    def _on_error(self, message):
        self.progress.stop()
        self.progress.grid_forget()
        self.status_label.configure(text="Ocorreu um erro.")
        self.btn_process.configure(state="normal", text="PROCESSAR PDF")
        messagebox.showerror("Erro", message)


if __name__ == "__main__":
    app = AutoPDFApp()
    app.mainloop()
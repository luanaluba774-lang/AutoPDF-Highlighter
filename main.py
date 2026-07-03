import fitz
import customtkinter as ctk
from tkinter import filedialog, messagebox
import json
import os
import io
import csv
import threading
from datetime import datetime

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False

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
# BASE WINDOW (com ou sem suporte a drag & drop)
# =========================
if DND_AVAILABLE:
    class _BaseWindow(ctk.CTk, TkinterDnD.DnDWrapper):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            try:
                self.TkdndVersion = TkinterDnD._require(self)
            except Exception:
                pass
else:
    class _BaseWindow(ctk.CTk):
        pass


# =========================
# APP
# =========================
class AutoPDFApp(_BaseWindow):
    def __init__(self):
        super().__init__()

        self.title("AutoPDF Highlighter")
        self.geometry("640x780")
        self.minsize(580, 700)

        self.pdf_path = ""
        self.keywords = load_keywords()
        self.chip_widgets = []
        self.thumbnail_image = None
        self.last_report = {}

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

        # PDF CARD (drop zone + thumbnail)
        pdf_card = ctk.CTkFrame(self, corner_radius=12)
        pdf_card.grid(row=1, column=0, sticky="ew", padx=24, pady=8)
        pdf_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            pdf_card, text="Arquivo PDF", font=ctk.CTkFont(size=13, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(12, 0))

        drop_text = "🖱  Clique para selecionar um PDF"
        if DND_AVAILABLE:
            drop_text = "📂  Arraste um PDF aqui ou clique para selecionar"

        self.drop_zone = ctk.CTkFrame(
            pdf_card, corner_radius=10, height=90,
            fg_color=("gray90", "gray20"), border_width=2,
            border_color=("gray70", "gray40")
        )
        self.drop_zone.grid(row=1, column=0, sticky="ew", padx=16, pady=(8, 16))
        self.drop_zone.grid_propagate(False)
        self.drop_zone.grid_columnconfigure(1, weight=1)

        self.thumbnail_label = ctk.CTkLabel(self.drop_zone, text="", width=60, height=70)
        self.thumbnail_label.grid(row=0, column=0, rowspan=2, padx=(12, 4), pady=10, sticky="w")

        self.drop_label = ctk.CTkLabel(
            self.drop_zone, text=drop_text, text_color="gray60", anchor="w", justify="left"
        )
        self.drop_label.grid(row=0, column=1, sticky="ew", padx=(4, 12), pady=(16, 0))

        self.label_pdf = ctk.CTkLabel(
            self.drop_zone, text="Nenhum PDF selecionado", text_color="gray50", anchor="w"
        )
        self.label_pdf.grid(row=1, column=1, sticky="ew", padx=(4, 12), pady=(0, 12))

        for widget in (self.drop_zone, self.drop_label, self.label_pdf):
            widget.bind("<Button-1>", lambda e: self.select_pdf())

        if DND_AVAILABLE:
            try:
                self.drop_zone.drop_target_register(DND_FILES)
                self.drop_zone.dnd_bind("<<Drop>>", self._on_drop)
            except Exception:
                pass

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

        self.chips_frame = ctk.CTkScrollableFrame(kw_card, fg_color="transparent", height=170)
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

    # ---------- THEME ----------
    def _toggle_theme(self):
        mode = "light" if self.switch_theme.get() else "dark"
        ctk.set_appearance_mode(mode)

    # ---------- PDF SELECTION ----------
    def select_pdf(self):
        path = filedialog.askopenfilename(filetypes=[("PDF", "*.pdf")])
        if path:
            self._load_pdf(path)

    def _on_drop(self, event):
        raw = event.data.strip()
        if raw.startswith("{") and raw.endswith("}"):
            raw = raw[1:-1]
        path = raw.split("} {")[0] if "} {" in raw else raw

        if path.lower().endswith(".pdf") and os.path.exists(path):
            self._load_pdf(path)
        else:
            messagebox.showerror("Erro", "Solte um arquivo .pdf válido")

    def _load_pdf(self, path):
        self.pdf_path = path
        self.label_pdf.configure(text=os.path.basename(path), text_color=("black", "white"))
        self.drop_label.configure(text="✅  PDF carregado — clique para trocar")
        self._update_thumbnail()

    def _update_thumbnail(self):
        if not PIL_AVAILABLE:
            return
        try:
            doc = fitz.open(self.pdf_path)
            page = doc[0]
            pix = page.get_pixmap(matrix=fitz.Matrix(0.25, 0.25))
            pil_img = Image.open(io.BytesIO(pix.tobytes("ppm")))
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(pix.width, pix.height))
            self.thumbnail_image = ctk_img
            self.thumbnail_label.configure(image=ctk_img, text="")
            doc.close()
        except Exception:
            pass

    # ---------- KEYWORDS ----------
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

    # ---------- PROCESSING ----------
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
            report = {word: 0 for word in self.keywords}

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
                        report[word] += len(areas)
                    except Exception:
                        continue

            output = self.pdf_path.replace(".pdf", "_highlighted.pdf")
            doc.save(output)
            doc.close()

            self.last_report = report
            self.after(0, self._on_success, total, output, report)
        except Exception as e:
            self.after(0, self._on_error, str(e))

    def _on_success(self, total, output, report):
        self.progress.stop()
        self.progress.grid_forget()
        self.status_label.configure(text=f"Salvo em: {os.path.basename(output)}")
        self.btn_process.configure(state="normal", text="PROCESSAR PDF")
        self._open_file(output)
        self._show_report_window(report, total, output)

    def _on_error(self, message):
        self.progress.stop()
        self.progress.grid_forget()
        self.status_label.configure(text="Ocorreu um erro.")
        self.btn_process.configure(state="normal", text="PROCESSAR PDF")
        messagebox.showerror("Erro", message)

    def _open_file(self, path):
        try:
            if os.name == "nt":
                os.startfile(path)
            elif os.uname().sysname == "Darwin":
                os.system(f'open "{path}"')
            else:
                os.system(f'xdg-open "{path}"')
        except Exception:
            pass

    # ---------- RELATÓRIO ----------
    def _show_report_window(self, report, total, output):
        win = ctk.CTkToplevel(self)
        win.title("Relatório de Ocorrências")
        win.geometry("380x460")
        win.transient(self)

        ctk.CTkLabel(
            win, text="✅ Processamento concluído",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(16, 4))

        ctk.CTkLabel(
            win, text=f"Total de destaques: {total}", text_color="gray60"
        ).pack(pady=(0, 12))

        list_frame = ctk.CTkScrollableFrame(win, width=320, height=260)
        list_frame.pack(padx=16, pady=(0, 12), fill="both", expand=True)

        header_row = ctk.CTkFrame(list_frame, fg_color="transparent")
        header_row.pack(fill="x", pady=(0, 6))
        ctk.CTkLabel(header_row, text="Palavra-chave", font=ctk.CTkFont(weight="bold"), anchor="w").pack(
            side="left", fill="x", expand=True
        )
        ctk.CTkLabel(header_row, text="Qtd.", font=ctk.CTkFont(weight="bold"), width=40).pack(side="right")

        for word, count in sorted(report.items(), key=lambda x: -x[1]):
            row = ctk.CTkFrame(list_frame, fg_color="transparent")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=word, anchor="w").pack(side="left", fill="x", expand=True)
            color = ("gray30", "gray80") if count > 0 else ("gray70", "gray50")
            ctk.CTkLabel(row, text=str(count), text_color=color, width=40).pack(side="right")

        ctk.CTkButton(
            win, text="📤 Exportar relatório (CSV)",
            command=lambda: self._export_report(report, output)
        ).pack(pady=(0, 16), padx=16, fill="x")

    def _export_report(self, report, output):
        default_name = os.path.basename(output).replace("_highlighted.pdf", "_relatorio.csv")
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            initialfile=default_name
        )
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Palavra-chave", "Ocorrências"])
                for word, count in report.items():
                    writer.writerow([word, count])
                writer.writerow([])
                writer.writerow(["Total", sum(report.values())])
                writer.writerow(["Gerado em", datetime.now().strftime("%d/%m/%Y %H:%M")])
            messagebox.showinfo("Exportado", f"Relatório salvo em:\n{path}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))


if __name__ == "__main__":
    app = AutoPDFApp()
    app.mainloop()

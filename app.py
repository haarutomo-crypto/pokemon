import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import font as tkfont
import json
import os

RECORDS_FILE = "records.jsonl"

class BattleTracker:
    def __init__(self, filepath=RECORDS_FILE):
        self.filepath = filepath

    def save_record(self, name, base_stats, notes):
        record = {
            "name": name,
            "base_stats": base_stats,
            "notes": notes
        }
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def search_records(self, keyword):
        results = []
        if not os.path.exists(self.filepath):
            return results

        with open(self.filepath, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                    if (keyword.lower() in record.get("name", "").lower() or
                        keyword.lower() in record.get("base_stats", "").lower() or
                        keyword.lower() in record.get("notes", "").lower()):
                        results.append(record)
                except json.JSONDecodeError:
                    continue
        return results

class PokemonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ポケモンデータ管理システム - BW Edition")

        # UI Styling (Pokemon Black & White Theme)
        self.bg_color = "#121212" # Very dark grey/black
        self.fg_color = "#f0f0f0" # White/light grey text
        self.accent_color = "#2a2a2a" # Slightly lighter dark grey
        self.highlight_color = "#4db8ff" # Tech blue accent like C-Gear

        self.root.configure(bg=self.bg_color)

        # Dynamic Fonts for Zooming
        self.base_font_size = 11
        self.bold_font = tkfont.Font(family='Helvetica', size=self.base_font_size, weight='bold')
        self.normal_font = tkfont.Font(family='Helvetica', size=self.base_font_size)
        self.small_bold_font = tkfont.Font(family='Helvetica', size=self.base_font_size - 1, weight='bold')
        self.small_normal_font = tkfont.Font(family='Helvetica', size=self.base_font_size - 2)
        self.mono_font = tkfont.Font(family='Consolas', size=self.base_font_size - 1)

        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background=self.bg_color, borderwidth=0)
        style.configure('TNotebook.Tab', background=self.accent_color, foreground=self.fg_color, padding=[15, 5])
        # We handle tab font dynamically below
        style.map('TNotebook.Tab', background=[('selected', self.highlight_color)], foreground=[('selected', '#000000')])

        style.configure('TFrame', background=self.bg_color)

        self.tracker = BattleTracker()

        # Fullscreen functionality
        self.is_fullscreen = False
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)

        # Zoom functionality bindings
        self.root.bind("<Control-MouseWheel>", self.zoom) # Windows/Mac
        self.root.bind("<Control-Button-4>", self.zoom) # Linux scroll up
        self.root.bind("<Control-Button-5>", self.zoom) # Linux scroll down

        # Create Notebook (Tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.update_styles()

        # Tab 1: Input
        self.tab_input = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_input, text="入力")

        # Tab 2: Data List
        self.tab_data = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_data, text="データ一覧")

        self.setup_input_tab()
        self.setup_data_tab()

    def update_styles(self):
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=self.small_bold_font)

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)
        return "break"

    def exit_fullscreen(self, event=None):
        self.is_fullscreen = False
        self.root.attributes("-fullscreen", False)
        return "break"

    def zoom(self, event):
        # Respond to mouse wheel for zooming
        if event.num == 4 or getattr(event, 'delta', 0) > 0:
            # Zoom In
            self.base_font_size = min(40, self.base_font_size + 1)
        elif event.num == 5 or getattr(event, 'delta', 0) < 0:
            # Zoom Out
            self.base_font_size = max(6, self.base_font_size - 1)

        # Update dynamic font sizes
        self.bold_font.configure(size=self.base_font_size)
        self.normal_font.configure(size=self.base_font_size)
        self.small_bold_font.configure(size=self.base_font_size - 1)
        self.small_normal_font.configure(size=self.base_font_size - 2)
        self.mono_font.configure(size=self.base_font_size - 1)
        self.update_styles()

    def setup_input_tab(self):
        input_frame = tk.Frame(self.tab_input, bg=self.bg_color, padx=20, pady=20)
        input_frame.pack(fill="x", expand=True)

        tk.Label(input_frame, text="ポケモンのなまえ:", bg=self.bg_color, fg=self.fg_color, font=self.bold_font).grid(row=0, column=0, sticky="e", pady=10)
        self.name_entry = tk.Entry(input_frame, width=30, bg=self.accent_color, fg=self.fg_color, insertbackground=self.fg_color, font=self.normal_font, relief="flat")
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, ipady=3)

        tk.Label(input_frame, text="種族値:", bg=self.bg_color, fg=self.fg_color, font=self.bold_font).grid(row=1, column=0, sticky="e", pady=10)
        self.stats_entry = tk.Entry(input_frame, width=30, bg=self.accent_color, fg=self.fg_color, insertbackground=self.fg_color, font=self.normal_font, relief="flat")
        self.stats_entry.grid(row=1, column=1, padx=10, pady=10, ipady=3)

        tk.Label(input_frame, text="備考:", bg=self.bg_color, fg=self.fg_color, font=self.bold_font).grid(row=2, column=0, sticky="e", pady=10)
        self.notes_entry = tk.Entry(input_frame, width=30, bg=self.accent_color, fg=self.fg_color, insertbackground=self.fg_color, font=self.normal_font, relief="flat")
        self.notes_entry.grid(row=2, column=1, padx=10, pady=10, ipady=3)

        self.save_btn = tk.Button(input_frame, text="保存", command=self.save_record, width=20, bg=self.highlight_color, fg="#000000", font=self.bold_font, relief="flat", activebackground="#3a9acc")
        self.save_btn.grid(row=3, column=0, columnspan=2, pady=30, ipady=5)

    def setup_data_tab(self):
        search_frame = tk.Frame(self.tab_data, bg=self.bg_color, padx=10, pady=10)
        search_frame.pack(fill="x")

        tk.Label(search_frame, text="検索キーワード:", bg=self.bg_color, fg=self.fg_color, font=self.small_bold_font).pack(side="left")
        self.search_entry = tk.Entry(search_frame, width=30, bg=self.accent_color, fg=self.fg_color, insertbackground=self.fg_color, font=self.normal_font, relief="flat")
        self.search_entry.pack(side="left", padx=5, ipady=2)

        self.search_btn = tk.Button(search_frame, text="検索", command=self.search_records, bg=self.highlight_color, fg="#000000", font=self.small_bold_font, relief="flat", activebackground="#3a9acc")
        self.search_btn.pack(side="left", padx=5)

        self.show_all_btn = tk.Button(search_frame, text="すべて表示", command=self.show_all, bg=self.accent_color, fg=self.fg_color, font=self.small_bold_font, relief="flat", activebackground="#404040", activeforeground="#ffffff")
        self.show_all_btn.pack(side="left", padx=5)

        output_frame = tk.Frame(self.tab_data, bg=self.bg_color, padx=10, pady=10)
        output_frame.pack(fill="both", expand=True)

        self.text_panel = tk.Text(output_frame, height=20, width=60, bg=self.accent_color, fg=self.highlight_color, font=self.mono_font, relief="flat", insertbackground=self.fg_color)
        self.text_panel.pack(fill="both", expand=True)

        self.show_all()

    def save_record(self):
        name = self.name_entry.get().strip()
        base_stats = self.stats_entry.get().strip()
        notes = self.notes_entry.get().strip()

        if not name:
            messagebox.showwarning("警告", "ポケモンのなまえを入力してください。")
            return

        self.tracker.save_record(name, base_stats, notes)

        # Clear entries
        self.name_entry.delete(0, tk.END)
        self.stats_entry.delete(0, tk.END)
        self.notes_entry.delete(0, tk.END)

        messagebox.showinfo("成功", "データを保存しました。")
        self.show_all()

    def display_results(self, records):
        self.text_panel.config(state=tk.NORMAL)
        self.text_panel.delete(1.0, tk.END)
        if not records:
            self.text_panel.insert(tk.END, "データが見つかりません。")
        else:
            for i, rec in enumerate(records, 1):
                line = f"[{i}] なまえ: {rec.get('name', '')} | 種族値: {rec.get('base_stats', '')} | 備考: {rec.get('notes', '')}\n"
                self.text_panel.insert(tk.END, line)
        self.text_panel.config(state=tk.DISABLED)

    def search_records(self):
        keyword = self.search_entry.get().strip()
        if not keyword:
            self.show_all()
            return

        results = self.tracker.search_records(keyword)
        self.display_results(results)

    def show_all(self):
        results = self.tracker.search_records("")
        self.display_results(results)

if __name__ == "__main__":
    root = tk.Tk()
    app = PokemonApp(root)
    root.mainloop()

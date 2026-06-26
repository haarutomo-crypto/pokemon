import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
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
        self.root.title("ポケモンデータ管理システム")

        self.tracker = BattleTracker()

        # Create Notebook (Tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Tab 1: Input
        self.tab_input = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_input, text="入力")

        # Tab 2: Data List
        self.tab_data = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_data, text="データ一覧")

        self.setup_input_tab()
        self.setup_data_tab()

    def setup_input_tab(self):
        input_frame = tk.Frame(self.tab_input, padx=20, pady=20)
        input_frame.pack(fill="x", expand=True)

        tk.Label(input_frame, text="ポケモンのなまえ:").grid(row=0, column=0, sticky="e", pady=5)
        self.name_entry = tk.Entry(input_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(input_frame, text="種族値:").grid(row=1, column=0, sticky="e", pady=5)
        self.stats_entry = tk.Entry(input_frame, width=30)
        self.stats_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(input_frame, text="備考:").grid(row=2, column=0, sticky="e", pady=5)
        self.notes_entry = tk.Entry(input_frame, width=30)
        self.notes_entry.grid(row=2, column=1, padx=10, pady=5)

        self.save_btn = tk.Button(input_frame, text="保存", command=self.save_record, width=20)
        self.save_btn.grid(row=3, column=0, columnspan=2, pady=20)

    def setup_data_tab(self):
        search_frame = tk.Frame(self.tab_data, padx=10, pady=10)
        search_frame.pack(fill="x")

        tk.Label(search_frame, text="検索キーワード:").pack(side="left")
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left", padx=5)

        self.search_btn = tk.Button(search_frame, text="検索", command=self.search_records)
        self.search_btn.pack(side="left", padx=5)

        self.show_all_btn = tk.Button(search_frame, text="すべて表示", command=self.show_all)
        self.show_all_btn.pack(side="left", padx=5)

        output_frame = tk.Frame(self.tab_data, padx=10, pady=10)
        output_frame.pack(fill="both", expand=True)

        self.text_panel = tk.Text(output_frame, height=20, width=60)
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

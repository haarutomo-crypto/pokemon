import tkinter as tk
from tkinter import messagebox
import json
import os

RECORDS_FILE = "records.jsonl"

class BattleTracker:
    def __init__(self, filepath=RECORDS_FILE):
        self.filepath = filepath

    def save_record(self, my_pokemon, opp_pokemon, result, notes):
        record = {
            "my_pokemon": my_pokemon,
            "opp_pokemon": opp_pokemon,
            "result": result,
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
                    # Search in all fields
                    if (keyword.lower() in record.get("my_pokemon", "").lower() or
                        keyword.lower() in record.get("opp_pokemon", "").lower() or
                        keyword.lower() in record.get("result", "").lower() or
                        keyword.lower() in record.get("notes", "").lower()):
                        results.append(record)
                except json.JSONDecodeError:
                    continue
        return results

class PokemonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ポケモン対戦記録システム")

        self.tracker = BattleTracker()

        # Input Frame
        self.input_frame = tk.LabelFrame(root, text="記録の入力", padx=10, pady=10)
        self.input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(self.input_frame, text="自分ポケモン:").grid(row=0, column=0, sticky="e")
        self.my_poke_entry = tk.Entry(self.input_frame)
        self.my_poke_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(self.input_frame, text="相手ポケモン:").grid(row=0, column=2, sticky="e")
        self.opp_poke_entry = tk.Entry(self.input_frame)
        self.opp_poke_entry.grid(row=0, column=3, padx=5, pady=2)

        tk.Label(self.input_frame, text="勝敗:").grid(row=1, column=0, sticky="e")
        self.result_entry = tk.Entry(self.input_frame)
        self.result_entry.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(self.input_frame, text="メモ:").grid(row=1, column=2, sticky="e")
        self.notes_entry = tk.Entry(self.input_frame)
        self.notes_entry.grid(row=1, column=3, padx=5, pady=2)

        self.save_btn = tk.Button(self.input_frame, text="保存", command=self.save_record)
        self.save_btn.grid(row=2, column=0, columnspan=4, pady=10)

        # Search Frame
        self.search_frame = tk.LabelFrame(root, text="記録の検索", padx=10, pady=10)
        self.search_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(self.search_frame, text="検索キーワード:").grid(row=0, column=0, sticky="e")
        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.grid(row=0, column=1, padx=5, pady=2)

        self.search_btn = tk.Button(self.search_frame, text="検索", command=self.search_records)
        self.search_btn.grid(row=0, column=2, padx=5, pady=2)

        self.show_all_btn = tk.Button(self.search_frame, text="すべて表示", command=self.show_all)
        self.show_all_btn.grid(row=0, column=3, padx=5, pady=2)

        # Output Frame
        self.output_frame = tk.LabelFrame(root, text="検索結果", padx=10, pady=10)
        self.output_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.text_panel = tk.Text(self.output_frame, height=15, width=60)
        self.text_panel.pack(fill="both", expand=True)

        self.show_all()

    def save_record(self):
        my_pokemon = self.my_poke_entry.get().strip()
        opp_pokemon = self.opp_poke_entry.get().strip()
        result = self.result_entry.get().strip()
        notes = self.notes_entry.get().strip()

        if not my_pokemon and not opp_pokemon:
            messagebox.showwarning("警告", "ポケモン名を入力してください。")
            return

        self.tracker.save_record(my_pokemon, opp_pokemon, result, notes)

        # Clear entries
        self.my_poke_entry.delete(0, tk.END)
        self.opp_poke_entry.delete(0, tk.END)
        self.result_entry.delete(0, tk.END)
        self.notes_entry.delete(0, tk.END)

        messagebox.showinfo("成功", "記録を保存しました。")
        self.show_all()

    def display_results(self, records):
        self.text_panel.delete(1.0, tk.END)
        if not records:
            self.text_panel.insert(tk.END, "記録が見つかりません。")
            return

        for i, rec in enumerate(records, 1):
            line = f"[{i}] 自分: {rec.get('my_pokemon', '')} | 相手: {rec.get('opp_pokemon', '')} | 勝敗: {rec.get('result', '')} | メモ: {rec.get('notes', '')}\n"
            self.text_panel.insert(tk.END, line)

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

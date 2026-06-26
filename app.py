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

    def save_record(self, name, hp, attack, defense, sp_atk, sp_def, speed, notes):
        # Store stats as integers if possible for sorting, otherwise 0
        def to_int(val):
            try:
                return int(val)
            except ValueError:
                return 0

        record = {
            "name": name,
            "hp": to_int(hp),
            "attack": to_int(attack),
            "defense": to_int(defense),
            "sp_atk": to_int(sp_atk),
            "sp_def": to_int(sp_def),
            "speed": to_int(speed),
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
                    # Search text fields
                    search_target = f"{record.get('name', '')} {record.get('notes', '')}"
                    if keyword.lower() in search_target.lower():
                        results.append(record)
                except json.JSONDecodeError:
                    continue
        return results

    def get_all_names(self):
        names = set()
        if not os.path.exists(self.filepath):
            return list(names)
        with open(self.filepath, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                    if 'name' in record:
                        names.add(record['name'])
                except json.JSONDecodeError:
                    continue
        return sorted(list(names))

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
        style.map('TNotebook.Tab', background=[('selected', self.highlight_color)], foreground=[('selected', '#000000')])

        style.configure('TFrame', background=self.bg_color)
        style.configure('TCombobox', background=self.accent_color, foreground='#000000') # Combobox text color needs to be dark for some OS

        self.tracker = BattleTracker()

        # Fullscreen functionality
        self.is_fullscreen = False
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)

        # Zoom functionality bindings
        self.root.bind("<Control-MouseWheel>", self.zoom)
        self.root.bind("<Control-Button-4>", self.zoom)
        self.root.bind("<Control-Button-5>", self.zoom)

        # Click outside listbox to close it
        self.root.bind("<Button-1>", self.check_close_listbox)

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

        self.sort_descending = False

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
        if event.num == 4 or getattr(event, 'delta', 0) > 0:
            self.base_font_size = min(40, self.base_font_size + 1)
        elif event.num == 5 or getattr(event, 'delta', 0) < 0:
            self.base_font_size = max(6, self.base_font_size - 1)

        self.bold_font.configure(size=self.base_font_size)
        self.normal_font.configure(size=self.base_font_size)
        self.small_bold_font.configure(size=self.base_font_size - 1)
        self.small_normal_font.configure(size=self.base_font_size - 2)
        self.mono_font.configure(size=self.base_font_size - 1)
        self.update_styles()

    def setup_input_tab(self):
        input_frame = tk.Frame(self.tab_input, bg=self.bg_color, padx=20, pady=20)
        input_frame.pack(fill="x", expand=True)

        tk.Label(input_frame, text="ポケモンのなまえ:", bg=self.bg_color, fg=self.fg_color, font=self.bold_font).grid(row=0, column=0, sticky="e", pady=5)
        self.name_entry = tk.Entry(input_frame, width=30, bg=self.accent_color, fg=self.fg_color, insertbackground=self.fg_color, font=self.normal_font, relief="flat")
        self.name_entry.grid(row=0, column=1, columnspan=3, padx=10, pady=5, ipady=3, sticky="w")

        # Stats section
        stats_frame = tk.LabelFrame(input_frame, text="種族値", bg=self.bg_color, fg=self.fg_color, font=self.bold_font, padx=10, pady=10)
        stats_frame.grid(row=1, column=0, columnspan=4, pady=10, sticky="ew")

        stat_labels = ["HP", "こうげき", "ぼうぎょ", "とくこう", "とくぼう", "すばやさ"]
        self.stat_entries = {}

        for i, stat in enumerate(stat_labels):
            tk.Label(stats_frame, text=stat+":", bg=self.bg_color, fg=self.fg_color, font=self.normal_font).grid(row=i//2, column=(i%2)*2, sticky="e", pady=5, padx=5)
            entry = tk.Entry(stats_frame, width=10, bg=self.accent_color, fg=self.fg_color, insertbackground=self.fg_color, font=self.normal_font, relief="flat")
            entry.grid(row=i//2, column=(i%2)*2 + 1, pady=5, padx=5, ipady=2)
            self.stat_entries[stat] = entry

        tk.Label(input_frame, text="備考:", bg=self.bg_color, fg=self.fg_color, font=self.bold_font).grid(row=2, column=0, sticky="e", pady=10)
        self.notes_entry = tk.Entry(input_frame, width=40, bg=self.accent_color, fg=self.fg_color, insertbackground=self.fg_color, font=self.normal_font, relief="flat")
        self.notes_entry.grid(row=2, column=1, columnspan=3, padx=10, pady=10, ipady=3, sticky="w")

        self.save_btn = tk.Button(input_frame, text="保存", command=self.save_record, width=20, bg=self.highlight_color, fg="#000000", font=self.bold_font, relief="flat", activebackground="#3a9acc")
        self.save_btn.grid(row=3, column=0, columnspan=4, pady=20, ipady=5)

    def setup_data_tab(self):
        search_frame = tk.Frame(self.tab_data, bg=self.bg_color, padx=10, pady=10)
        search_frame.pack(fill="x")

        tk.Label(search_frame, text="検索:", bg=self.bg_color, fg=self.fg_color, font=self.small_bold_font).grid(row=0, column=0, sticky="e")

        # Search Entry with suggestion listbox
        self.search_entry = tk.Entry(search_frame, width=20, bg=self.accent_color, fg=self.fg_color, insertbackground=self.fg_color, font=self.normal_font, relief="flat")
        self.search_entry.grid(row=0, column=1, padx=5, ipady=2)
        self.search_entry.bind("<KeyRelease>", self.update_suggestions)

        # Suggestion Listbox (hidden by default)
        self.suggestion_listbox = tk.Listbox(self.root, bg=self.accent_color, fg=self.fg_color, font=self.normal_font, relief="flat", selectbackground=self.highlight_color)
        self.suggestion_listbox.bind("<<ListboxSelect>>", self.select_suggestion)

        self.search_btn = tk.Button(search_frame, text="検索", command=self.search_records, bg=self.highlight_color, fg="#000000", font=self.small_bold_font, relief="flat", activebackground="#3a9acc")
        self.search_btn.grid(row=0, column=2, padx=5)

        tk.Label(search_frame, text="並べ替え:", bg=self.bg_color, fg=self.fg_color, font=self.small_bold_font).grid(row=0, column=3, sticky="e", padx=(15,0))

        self.sort_var = tk.StringVar(value="なし")
        sort_options = ["なし", "HP", "こうげき", "ぼうぎょ", "とくこう", "とくぼう", "すばやさ"]
        self.sort_combo = ttk.Combobox(search_frame, textvariable=self.sort_var, values=sort_options, width=10, state="readonly")
        self.sort_combo.grid(row=0, column=4, padx=5)
        self.sort_combo.bind("<<ComboboxSelected>>", lambda e: self.search_records())

        self.sort_order_btn = tk.Button(search_frame, text="昇順", command=self.toggle_sort_order, bg=self.accent_color, fg=self.fg_color, font=self.small_bold_font, relief="flat", activebackground="#404040")
        self.sort_order_btn.grid(row=0, column=5, padx=5)

        self.show_all_btn = tk.Button(search_frame, text="すべて表示", command=self.show_all, bg=self.accent_color, fg=self.fg_color, font=self.small_bold_font, relief="flat", activebackground="#404040")
        self.show_all_btn.grid(row=0, column=6, padx=5)

        output_frame = tk.Frame(self.tab_data, bg=self.bg_color, padx=10, pady=10)
        output_frame.pack(fill="both", expand=True)

        self.text_panel = tk.Text(output_frame, height=20, width=80, bg=self.accent_color, fg=self.highlight_color, font=self.mono_font, relief="flat", insertbackground=self.fg_color)
        self.text_panel.pack(fill="both", expand=True)

        self.show_all()

    def update_suggestions(self, event):
        keyword = self.search_entry.get().strip()
        if not keyword:
            self.suggestion_listbox.place_forget()
            return

        all_names = self.tracker.get_all_names()
        matches = [name for name in all_names if keyword.lower() in name.lower()]

        if matches:
            self.suggestion_listbox.delete(0, tk.END)
            for match in matches:
                self.suggestion_listbox.insert(tk.END, match)

            # Position listbox exactly under search entry globally
            x = self.search_entry.winfo_rootx() - self.root.winfo_rootx()
            y = self.search_entry.winfo_rooty() - self.root.winfo_rooty() + self.search_entry.winfo_height()
            self.suggestion_listbox.place(x=x, y=y, width=self.search_entry.winfo_width())
            self.suggestion_listbox.lift()
        else:
            self.suggestion_listbox.place_forget()

    def select_suggestion(self, event):
        selection = self.suggestion_listbox.curselection()
        if selection:
            name = self.suggestion_listbox.get(selection[0])
            self.search_entry.delete(0, tk.END)
            self.search_entry.insert(0, name)
            self.suggestion_listbox.place_forget()
            self.search_records()

    def check_close_listbox(self, event):
        # Close listbox if click is outside of it and search entry
        if self.suggestion_listbox.winfo_ismapped():
            wx, wy = self.root.winfo_pointerxy()
            widget = self.root.winfo_containing(wx, wy)
            if widget not in (self.suggestion_listbox, self.search_entry):
                self.suggestion_listbox.place_forget()

    def save_record(self):
        name = self.name_entry.get().strip()
        hp = self.stat_entries["HP"].get().strip()
        attack = self.stat_entries["こうげき"].get().strip()
        defense = self.stat_entries["ぼうぎょ"].get().strip()
        sp_atk = self.stat_entries["とくこう"].get().strip()
        sp_def = self.stat_entries["とくぼう"].get().strip()
        speed = self.stat_entries["すばやさ"].get().strip()
        notes = self.notes_entry.get().strip()

        if not name:
            messagebox.showwarning("警告", "ポケモンのなまえを入力してください。")
            return

        self.tracker.save_record(name, hp, attack, defense, sp_atk, sp_def, speed, notes)

        # Clear entries
        self.name_entry.delete(0, tk.END)
        for entry in self.stat_entries.values():
            entry.delete(0, tk.END)
        self.notes_entry.delete(0, tk.END)

        messagebox.showinfo("成功", "データを保存しました。")
        self.show_all()

    def toggle_sort_order(self):
        self.sort_descending = not self.sort_descending
        self.sort_order_btn.config(text="降順" if self.sort_descending else "昇順")
        self.search_records()

    def display_results(self, records):
        # Sort records before displaying
        sort_key_map = {
            "HP": "hp",
            "こうげき": "attack",
            "ぼうぎょ": "defense",
            "とくこう": "sp_atk",
            "とくぼう": "sp_def",
            "すばやさ": "speed"
        }
        selected_sort = self.sort_var.get()

        if selected_sort in sort_key_map:
            key = sort_key_map[selected_sort]
            records.sort(key=lambda x: x.get(key, 0), reverse=self.sort_descending)

        self.text_panel.config(state=tk.NORMAL)
        self.text_panel.delete(1.0, tk.END)
        if not records:
            self.text_panel.insert(tk.END, "データが見つかりません。")
        else:
            for i, rec in enumerate(records, 1):
                # Format to align nicely
                line = (f"[{i}] {rec.get('name', '')}\n"
                        f"    HP:{rec.get('hp',0):<3} 攻:{rec.get('attack',0):<3} 防:{rec.get('defense',0):<3} "
                        f"特攻:{rec.get('sp_atk',0):<3} 特防:{rec.get('sp_def',0):<3} 素:{rec.get('speed',0):<3}\n"
                        f"    備考: {rec.get('notes', '')}\n\n")
                self.text_panel.insert(tk.END, line)
        self.text_panel.config(state=tk.DISABLED)

    def search_records(self):
        self.suggestion_listbox.place_forget()
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

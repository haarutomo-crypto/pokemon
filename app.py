import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import font as tkfont
import json
import os
import uuid
import re

RECORDS_FILE = "records.jsonl"

class BattleTracker:
    def __init__(self, filepath=RECORDS_FILE):
        self.filepath = filepath
        self._ensure_file()

    def _ensure_file(self):
        # Ensure file exists and all old records have an ID
        if not os.path.exists(self.filepath):
            return

        temp_filepath = self.filepath + ".tmp"
        needs_rewrite = False

        records = []
        with open(self.filepath, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                    if "id" not in record:
                        record["id"] = str(uuid.uuid4())
                        needs_rewrite = True
                    # Convert notes to list format if it's a string
                    if isinstance(record.get("notes"), str):
                        notes_list = [n.strip() for n in record["notes"].split('\n') if n.strip()]
                        record["notes"] = self._clean_numbering(notes_list)
                        needs_rewrite = True
                    records.append(record)
                except json.JSONDecodeError:
                    pass

        if needs_rewrite:
            with open(temp_filepath, "w", encoding="utf-8") as f:
                for rec in records:
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            os.replace(temp_filepath, self.filepath)

    def _clean_numbering(self, notes_list):
        # Remove manual numbering like "1.", "1)", "[1] " from notes
        cleaned = []
        # Require a dot or parenthesis, OR brackets with a space, to avoid stripping "100% accuracy"
        pattern = re.compile(r'^(\[?\d+\]?[\.\)]\s+|\[\d+\]\s+|\d+\.\s+)')
        for note in notes_list:
            cleaned.append(pattern.sub('', note).strip())
        return cleaned

    def save_record(self, name, hp, attack, defense, sp_atk, sp_def, speed, notes_text):
        def to_int(val):
            try:
                return int(val)
            except ValueError:
                return 0

        notes_list = [n.strip() for n in notes_text.split('\n') if n.strip()]

        record = {
            "id": str(uuid.uuid4()),
            "name": name,
            "hp": to_int(hp),
            "attack": to_int(attack),
            "defense": to_int(defense),
            "sp_atk": to_int(sp_atk),
            "sp_def": to_int(sp_def),
            "speed": to_int(speed),
            "notes": self._clean_numbering(notes_list)
        }
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def update_record(self, record_id, name, hp, attack, defense, sp_atk, sp_def, speed, notes_text):
        def to_int(val):
            try:
                return int(val)
            except ValueError:
                return 0

        notes_list = [n.strip() for n in notes_text.split('\n') if n.strip()]

        updated_record = {
            "id": record_id,
            "name": name,
            "hp": to_int(hp),
            "attack": to_int(attack),
            "defense": to_int(defense),
            "sp_atk": to_int(sp_atk),
            "sp_def": to_int(sp_def),
            "speed": to_int(speed),
            "notes": self._clean_numbering(notes_list)
        }

        records = []
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        try:
                            rec = json.loads(line)
                            if rec.get("id") == record_id:
                                records.append(updated_record)
                            else:
                                records.append(rec)
                        except json.JSONDecodeError:
                            continue

        with open(self.filepath, "w", encoding="utf-8") as f:
            for rec in records:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    def delete_record(self, record_id):
        records = []
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        try:
                            rec = json.loads(line)
                            if rec.get("id") != record_id:
                                records.append(rec)
                        except json.JSONDecodeError:
                            continue

        with open(self.filepath, "w", encoding="utf-8") as f:
            for rec in records:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")

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
                    notes_str = " ".join(record.get("notes", []))
                    search_target = f"{record.get('name', '')} {notes_str}"
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
        self.bg_color = "#121212"
        self.fg_color = "#ffffff" # Pure white for data visibility as requested
        self.accent_color = "#2a2a2a"
        self.highlight_color = "#4db8ff"

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
        style.configure('TLabelframe', background=self.bg_color, foreground=self.fg_color)
        style.configure('TLabelframe.Label', background=self.bg_color, foreground=self.fg_color)
        style.configure('TCombobox', background=self.accent_color, foreground='#000000')

        # Treeview styling (Data Table)
        style.configure('Treeview', background=self.accent_color, foreground=self.fg_color, fieldbackground=self.accent_color, rowheight=25)
        style.map('Treeview', background=[('selected', self.highlight_color)], foreground=[('selected', '#000000')])
        style.configure('Treeview.Heading', background=self.bg_color, foreground=self.fg_color, font=self.bold_font)

        self.tracker = BattleTracker()

        # Fullscreen functionality
        self.is_fullscreen = False
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)

        # Zoom functionality bindings
        self.root.bind("<Control-MouseWheel>", self.zoom)
        self.root.bind("<Control-Button-4>", self.zoom)
        self.root.bind("<Control-Button-5>", self.zoom)

        self.root.bind("<Button-1>", self.check_close_listbox)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.update_styles()

        self.tab_input = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_input, text="入力")

        self.tab_data = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_data, text="データ一覧")

        self.setup_input_tab()
        self.setup_data_tab()

        self.sort_descending = False
        self.current_records = []
        self.selected_record_id = None

    def update_styles(self):
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=self.small_bold_font)
        style.configure('Treeview', font=self.normal_font)

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

    def _create_stat_entries(self, parent_frame):
        entries = {}
        stat_labels = ["HP", "こうげき", "ぼうぎょ", "とくこう", "とくぼう", "すばやさ"]
        for i, stat in enumerate(stat_labels):
            tk.Label(parent_frame, text=stat+":", bg=self.bg_color, fg=self.fg_color, font=self.normal_font).grid(row=i//2, column=(i%2)*2, sticky="e", pady=2, padx=2)
            entry = tk.Entry(parent_frame, width=8, bg=self.accent_color, fg=self.fg_color, insertbackground=self.fg_color, font=self.normal_font, relief="flat")
            entry.grid(row=i//2, column=(i%2)*2 + 1, pady=2, padx=2)
            entries[stat] = entry
        return entries

    def setup_input_tab(self):
        input_frame = tk.Frame(self.tab_input, bg=self.bg_color, padx=20, pady=20)
        input_frame.pack(fill="x", expand=True)

        tk.Label(input_frame, text="ポケモンのなまえ:", bg=self.bg_color, fg=self.fg_color, font=self.bold_font).grid(row=0, column=0, sticky="e", pady=5)
        self.in_name_entry = tk.Entry(input_frame, width=30, bg=self.accent_color, fg=self.fg_color, insertbackground=self.fg_color, font=self.normal_font, relief="flat")
        self.in_name_entry.grid(row=0, column=1, columnspan=3, padx=10, pady=5, ipady=3, sticky="w")

        stats_frame = tk.LabelFrame(input_frame, text="種族値", bg=self.bg_color, fg=self.fg_color, font=self.bold_font, padx=10, pady=10)
        stats_frame.grid(row=1, column=0, columnspan=4, pady=10, sticky="ew")

        self.in_stat_entries = self._create_stat_entries(stats_frame)

        tk.Label(input_frame, text="備考\n(改行でリスト化):", bg=self.bg_color, fg=self.fg_color, font=self.bold_font).grid(row=2, column=0, sticky="ne", pady=10)
        self.in_notes_entry = tk.Text(input_frame, width=40, height=5, bg=self.accent_color, fg=self.fg_color, insertbackground=self.fg_color, font=self.normal_font, relief="flat")
        self.in_notes_entry.grid(row=2, column=1, columnspan=3, padx=10, pady=10, sticky="w")

        self.save_btn = tk.Button(input_frame, text="保存", command=self.save_record, width=20, bg=self.highlight_color, fg="#000000", font=self.bold_font, relief="flat", activebackground="#3a9acc")
        self.save_btn.grid(row=3, column=0, columnspan=4, pady=20, ipady=5)

    def setup_data_tab(self):
        # 1. Search Bar Area
        search_frame = tk.Frame(self.tab_data, bg=self.bg_color, padx=10, pady=10)
        search_frame.pack(fill="x")

        tk.Label(search_frame, text="検索:", bg=self.bg_color, fg=self.fg_color, font=self.small_bold_font).grid(row=0, column=0, sticky="e")
        self.search_entry = tk.Entry(search_frame, width=20, bg=self.accent_color, fg=self.fg_color, insertbackground=self.fg_color, font=self.normal_font, relief="flat")
        self.search_entry.grid(row=0, column=1, padx=5, ipady=2)
        self.search_entry.bind("<KeyRelease>", self.update_suggestions)

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

        # 2. Main Content Area (Split PanedWindow)
        paned = tk.PanedWindow(self.tab_data, orient=tk.HORIZONTAL, bg=self.bg_color, sashwidth=4)
        paned.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Left side: Treeview for displaying records
        tree_frame = tk.Frame(paned, bg=self.bg_color)
        paned.add(tree_frame, minsize=400)

        columns = ("name", "hp", "atk", "def", "spa", "spd", "spe")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        self.tree.heading("name", text="なまえ")
        self.tree.heading("hp", text="HP")
        self.tree.heading("atk", text="攻")
        self.tree.heading("def", text="防")
        self.tree.heading("spa", text="特攻")
        self.tree.heading("spd", text="特防")
        self.tree.heading("spe", text="早")

        self.tree.column("name", width=120, anchor=tk.W)
        self.tree.column("hp", width=40, anchor=tk.E)
        self.tree.column("atk", width=40, anchor=tk.E)
        self.tree.column("def", width=40, anchor=tk.E)
        self.tree.column("spa", width=40, anchor=tk.E)
        self.tree.column("spd", width=40, anchor=tk.E)
        self.tree.column("spe", width=40, anchor=tk.E)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Right side: Editing Area
        edit_frame = ttk.LabelFrame(paned, text="データ編集 (選択中)")
        paned.add(edit_frame, minsize=250)

        edit_inner = tk.Frame(edit_frame, bg=self.bg_color, padx=10, pady=10)
        edit_inner.pack(fill="both", expand=True)

        tk.Label(edit_inner, text="なまえ:", bg=self.bg_color, fg=self.fg_color, font=self.bold_font).pack(anchor="w")
        self.edit_name_entry = tk.Entry(edit_inner, bg=self.accent_color, fg=self.fg_color, insertbackground=self.fg_color, font=self.normal_font, relief="flat")
        self.edit_name_entry.pack(fill="x", pady=(0, 10), ipady=3)

        stats_inner_frame = tk.Frame(edit_inner, bg=self.bg_color)
        stats_inner_frame.pack(fill="x")
        self.edit_stat_entries = self._create_stat_entries(stats_inner_frame)

        tk.Label(edit_inner, text="備考:", bg=self.bg_color, fg=self.fg_color, font=self.bold_font).pack(anchor="w", pady=(10, 0))
        self.edit_notes_entry = tk.Text(edit_inner, height=8, bg=self.accent_color, fg=self.fg_color, insertbackground=self.fg_color, font=self.normal_font, relief="flat")
        self.edit_notes_entry.pack(fill="both", expand=True, pady=(0, 10))

        btn_frame = tk.Frame(edit_inner, bg=self.bg_color)
        btn_frame.pack(fill="x")

        self.update_btn = tk.Button(btn_frame, text="更新", command=self.update_record, bg=self.highlight_color, fg="#000000", font=self.bold_font, relief="flat", activebackground="#3a9acc")
        self.update_btn.pack(side="left", expand=True, fill="x", padx=(0, 5), ipady=3)

        self.delete_btn = tk.Button(btn_frame, text="選択消去", command=self.delete_record, bg="#ff4d4d", fg="#ffffff", font=self.bold_font, relief="flat", activebackground="#cc0000")
        self.delete_btn.pack(side="right", expand=True, fill="x", padx=(5, 0), ipady=3)

        self.disable_edit_panel()
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
        if self.suggestion_listbox.winfo_ismapped():
            wx, wy = self.root.winfo_pointerxy()
            widget = self.root.winfo_containing(wx, wy)
            if widget not in (self.suggestion_listbox, self.search_entry):
                self.suggestion_listbox.place_forget()

    def _format_notes_for_display(self, notes_list):
        if not notes_list:
            return ""
        # Auto-number the notes purely for display
        return "\n".join(f"{i+1}. {note}" for i, note in enumerate(notes_list))

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            self.disable_edit_panel()
            return

        item = self.tree.item(selected[0])
        self.selected_record_id = item['tags'][0] # Stored ID in tags

        # Find record in current memory
        record = next((r for r in self.current_records if r['id'] == self.selected_record_id), None)
        if not record:
            return

        self.enable_edit_panel()

        self.edit_name_entry.delete(0, tk.END)
        self.edit_name_entry.insert(0, record.get("name", ""))

        stats = ["hp", "attack", "defense", "sp_atk", "sp_def", "speed"]
        labels = ["HP", "こうげき", "ぼうぎょ", "とくこう", "とくぼう", "すばやさ"]

        for stat_key, label in zip(stats, labels):
            self.edit_stat_entries[label].delete(0, tk.END)
            self.edit_stat_entries[label].insert(0, str(record.get(stat_key, 0)))

        self.edit_notes_entry.delete("1.0", tk.END)
        self.edit_notes_entry.insert("1.0", self._format_notes_for_display(record.get("notes", [])))

    def disable_edit_panel(self):
        self.selected_record_id = None
        self.edit_name_entry.delete(0, tk.END)
        for entry in self.edit_stat_entries.values():
            entry.delete(0, tk.END)
        self.edit_notes_entry.delete("1.0", tk.END)

        self.edit_name_entry.config(state=tk.DISABLED)
        for entry in self.edit_stat_entries.values():
            entry.config(state=tk.DISABLED)
        self.edit_notes_entry.config(state=tk.DISABLED)
        self.update_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)

    def enable_edit_panel(self):
        self.edit_name_entry.config(state=tk.NORMAL)
        for entry in self.edit_stat_entries.values():
            entry.config(state=tk.NORMAL)
        self.edit_notes_entry.config(state=tk.NORMAL)
        self.update_btn.config(state=tk.NORMAL)
        self.delete_btn.config(state=tk.NORMAL)

    def save_record(self):
        name = self.in_name_entry.get().strip()
        hp = self.in_stat_entries["HP"].get().strip()
        attack = self.in_stat_entries["こうげき"].get().strip()
        defense = self.in_stat_entries["ぼうぎょ"].get().strip()
        sp_atk = self.in_stat_entries["とくこう"].get().strip()
        sp_def = self.in_stat_entries["とくぼう"].get().strip()
        speed = self.in_stat_entries["すばやさ"].get().strip()
        notes = self.in_notes_entry.get("1.0", tk.END).strip()

        if not name:
            messagebox.showwarning("警告", "ポケモンのなまえを入力してください。")
            return

        self.tracker.save_record(name, hp, attack, defense, sp_atk, sp_def, speed, notes)

        # Clear entries
        self.in_name_entry.delete(0, tk.END)
        for entry in self.in_stat_entries.values():
            entry.delete(0, tk.END)
        self.in_notes_entry.delete("1.0", tk.END)

        messagebox.showinfo("成功", "データを保存しました。")
        self.show_all()

    def update_record(self):
        if not self.selected_record_id:
            return

        name = self.edit_name_entry.get().strip()
        hp = self.edit_stat_entries["HP"].get().strip()
        attack = self.edit_stat_entries["こうげき"].get().strip()
        defense = self.edit_stat_entries["ぼうぎょ"].get().strip()
        sp_atk = self.edit_stat_entries["とくこう"].get().strip()
        sp_def = self.edit_stat_entries["とくぼう"].get().strip()
        speed = self.edit_stat_entries["すばやさ"].get().strip()
        notes = self.edit_notes_entry.get("1.0", tk.END).strip()

        if not name:
            messagebox.showwarning("警告", "ポケモンのなまえを入力してください。")
            return

        self.tracker.update_record(self.selected_record_id, name, hp, attack, defense, sp_atk, sp_def, speed, notes)
        messagebox.showinfo("成功", "データを更新しました。")
        self.search_records() # Refresh current view

    def delete_record(self):
        if not self.selected_record_id:
            return

        if messagebox.askyesno("確認", "選択したデータを消去しますか？\nこの操作は取り消せません。"):
            self.tracker.delete_record(self.selected_record_id)
            self.disable_edit_panel()
            self.search_records() # Refresh current view

    def toggle_sort_order(self):
        self.sort_descending = not self.sort_descending
        self.sort_order_btn.config(text="降順" if self.sort_descending else "昇順")
        self.search_records()

    def display_results(self, records):
        self.current_records = records
        self.disable_edit_panel() # Reset edit view

        # Sort records
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

        # Update Treeview
        self.tree.delete(*self.tree.get_children())
        for rec in records:
            values = (
                rec.get("name", ""),
                rec.get("hp", 0),
                rec.get("attack", 0),
                rec.get("defense", 0),
                rec.get("sp_atk", 0),
                rec.get("sp_def", 0),
                rec.get("speed", 0)
            )
            # Store ID in tags to retrieve on select
            self.tree.insert("", tk.END, values=values, tags=(rec["id"],))

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

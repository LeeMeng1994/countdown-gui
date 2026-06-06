#!/usr/bin/env python3
"""Countdown Desktop App - Python Tkinter GUI"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime, date
import os
from pathlib import Path

DATA_FILE = Path(os.environ.get('APPDATA', str(Path.home()))) / 'countdown-gui' / 'events.txt'

class CountdownApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Countdown Days')
        self.root.geometry('400x520')
        self.root.resizable(False, False)
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        self.setup_ui()
        self.refresh_list()

    def setup_ui(self):
        title = tk.Label(self.root, text='Days Remaining', font=('Arial', 22, 'bold'))
        title.pack(pady=10)

        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=5, padx=10, fill='x')

        tk.Label(input_frame, text='Event:').grid(row=0, column=0, sticky='w')
        self.name_entry = tk.Entry(input_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text='Date:').grid(row=1, column=0, sticky='w', pady=5)
        self.date_entry = tk.Entry(input_frame, width=30)
        self.date_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(input_frame, text='Format: YYYY-MM-DD', font=('Arial', 8), fg='gray').grid(row=2, column=1, sticky='w')

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text='Add', command=self.add_event, bg='#4CAF50', fg='white', width=10).pack(side='left', padx=5)
        tk.Button(btn_frame, text='Refresh', command=self.refresh_list, bg='#2196F3', fg='white', width=10).pack(side='left', padx=5)

        list_frame = tk.Frame(self.root, bg='white', bd=2, relief='groove')
        list_frame.pack(pady=10, padx=10, fill='both', expand=True)

        header = tk.Frame(list_frame, bg='#f0f0f0')
        header.pack(fill='x')
        tk.Label(header, text='Event', width=20, bg='#f0f0f0', font=('Arial', 10, 'bold')).grid(row=0, column=0)
        tk.Label(header, text='Days', width=10, bg='#f0f0f0', font=('Arial', 10, 'bold')).grid(row=0, column=1)
        tk.Label(header, text='', width=6, bg='#f0f0f0').grid(row=0, column=2)

        self.list_canvas = tk.Canvas(list_frame)
        self.list_scrollbar = tk.Scrollbar(list_frame, orient='vertical', command=self.list_canvas.yview)
        self.list_content = tk.Frame(self.list_canvas)

        self.list_canvas.configure(yscrollcommand=self.list_scrollbar.set)
        self.list_canvas.pack(side='left', fill='both', expand=True)
        self.list_scrollbar.pack(side='right', fill='y')

        self.list_canvas.create_window((0, 0), window=self.list_content, anchor='nw')
        self.list_content.bind('<Configure>', lambda e: self.list_canvas.configure(scrollregion=self.list_canvas.bbox('all')))

    def add_event(self):
        name = self.name_entry.get().strip()
        date_str = self.date_entry.get().strip()

        if not name or not date_str:
            messagebox.showwarning('Warning', 'Please fill in event name and date')
            return

        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            messagebox.showerror('Error', 'Date must be YYYY-MM-DD')
            return

        with open(DATA_FILE, 'a', encoding='utf-8') as f:
            f.write(f'{name}|{date_str}\n')

        self.name_entry.delete(0, 'end')
        self.date_entry.delete(0, 'end')
        self.refresh_list()
        messagebox.showinfo('Success', f'Added: {name}')

    def refresh_list(self):
        for widget in self.list_content.winfo_children():
            widget.destroy()

        if not DATA_FILE.exists():
            tk.Label(self.list_content, text='No events yet', fg='gray').pack(pady=20)
            return

        events = []
        today = date.today()

        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 2:
                    name, date_str = parts
                    try:
                        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                        delta = (target_date - today).days
                        events.append((name, date_str, delta, target_date))
                    except Exception:
                        pass

        if not events:
            tk.Label(self.list_content, text='No events yet', fg='gray').pack(pady=20)
            return

        events.sort(key=lambda x: x[2])

        for i, (name, date_str, delta, target_date) in enumerate(events):
            row = tk.Frame(self.list_content)
            row.pack(fill='x', pady=2)

            display_name = name[:18] + ('...' if len(name) > 18 else '')
            tk.Label(row, text=display_name, width=20, anchor='w').grid(row=0, column=0)

            if delta < 0:
                days_text = f'Passed {-delta}'
                fg_color = '#999'
            elif delta == 0:
                days_text = 'TODAY!'
                fg_color = '#f44336'
            elif delta <= 7:
                days_text = f'{delta}d'
                fg_color = '#ff9800'
            else:
                days_text = f'{delta}d'
                fg_color = '#4CAF50'

            tk.Label(row, text=days_text, width=10, fg=fg_color, font=('Arial', 10, 'bold')).grid(row=0, column=1)
            tk.Button(row, text='Del', width=6, fg='red', command=lambda n=name, d=date_str: self.delete_event(n, d)).grid(row=0, column=2)

    def delete_event(self, name, date_str):
        if messagebox.askyesno('Confirm', f'Delete "{name}"?'):
            events = []
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and line != f'{name}|{date_str}':
                        events.append(line)

            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                f.write('\n'.join(events) + ('\n' if events else ''))

            self.refresh_list()

if __name__ == '__main__':
    root = tk.Tk()
    app = CountdownApp(root)
    root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_BASE = 'http://127.0.0.1:8000/api/'

# Helper functions to fetch lists for dropdowns

def fetch_list(endpoint):
    try:
        resp = requests.get(API_BASE + endpoint)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        messagebox.showerror('Error', f'Failed to fetch {endpoint}: {e}')
        return []

class ModelTab:
    def __init__(self, parent, model, fields, fk_fields=None, choices=None):
        self.model = model
        self.fields = fields
        self.fk_fields = fk_fields or {}
        self.choices = choices or {}
        self.data = []
        self.selected_id = None
        self.frame = ttk.Frame(parent)
        self.listbox = tk.Listbox(self.frame, width=60)
        self.listbox.pack(padx=10, pady=10)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        self.entries = {}
        for field in fields:
            row = tk.Frame(self.frame)
            row.pack(fill='x', padx=10, pady=2)
            tk.Label(row, text=field.capitalize(), width=18, anchor='w').pack(side=tk.LEFT)
            var = tk.StringVar()
            if field in self.fk_fields:
                entry = ttk.Combobox(row, textvariable=var, state='readonly')
                entry.pack(side=tk.LEFT, fill='x', expand=True)
                self.entries[field] = (entry, var)
            elif field in self.choices:
                entry = ttk.Combobox(row, textvariable=var, state='readonly', values=self.choices[field])
                entry.pack(side=tk.LEFT, fill='x', expand=True)
                self.entries[field] = (entry, var)
            else:
                entry = tk.Entry(row, textvariable=var)
                entry.pack(side=tk.LEFT, fill='x', expand=True)
                self.entries[field] = (entry, var)
        btn_frame = tk.Frame(self.frame)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text='Add', command=self.add).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text='Update', command=self.update).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text='Delete', command=self.delete).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text='Refresh', command=self.load).pack(side=tk.LEFT, padx=5)
        self.load()

    def get_api_url(self):
        return API_BASE + self.model + '/'

    def load(self):
        self.data = fetch_list(self.model + '/')
        self.listbox.delete(0, tk.END)
        for obj in self.data:
            display = f"{obj['id']}: " + ', '.join(str(obj.get(f, '')) for f in self.fields)
            self.listbox.insert(tk.END, display)
        self.selected_id = None
        for field in self.fk_fields:
            fk_endpoint, fk_label = self.fk_fields[field]
            fk_list = fetch_list(fk_endpoint)
            entry, var = self.entries[field]
            entry['values'] = [f"{item['id']}: {item[fk_label]}" for item in fk_list]
        for field in self.choices:
            entry, var = self.entries[field]
            entry['values'] = self.choices[field]
        for entry, var in self.entries.values():
            var.set('')

    def on_select(self, event):
        selection = self.listbox.curselection()
        if selection:
            idx = selection[0]
            obj = self.data[idx]
            self.selected_id = obj['id']
            for field in self.fields:
                entry, var = self.entries[field]
                val = obj.get(field, '')
                if field in self.fk_fields and val:
                    fk_endpoint, fk_label = self.fk_fields[field]
                    fk_list = fetch_list(fk_endpoint)
                    for item in fk_list:
                        if item['id'] == val or (isinstance(val, dict) and item['id'] == val.get('id')):
                            var.set(f"{item['id']}: {item[fk_label]}")
                            break
                elif field in self.choices:
                    var.set(val)
                else:
                    var.set(str(val))
        else:
            self.selected_id = None
            for entry, var in self.entries.values():
                var.set('')

    def get_payload(self):
        payload = {}
        for field in self.fields:
            entry, var = self.entries[field]
            val = var.get()
            if field in self.fk_fields:
                if val:
                    payload[field] = int(val.split(':')[0])
            elif field in self.choices:
                payload[field] = val
            else:
                if val == '':
                    if self.model == 'weight-classifications' and field in ['min_weight', 'max_weight']:
                        messagebox.showwarning('Input Error', f'{field.replace("_", " ").capitalize()} is required.')
                        return None
                else:
                    try:
                        payload[field] = float(val) if '.' in val else int(val)
                    except ValueError:
                        payload[field] = val
        return payload

    def add(self):
        payload = self.get_payload()
        if payload is None:
            return
        print("DEBUG PAYLOAD:", payload)  # Add this line
        try:
            resp = requests.post(self.get_api_url(), json=payload)
            resp.raise_for_status()
            self.load()
        except Exception as e:
            messagebox.showerror('Error', f'Failed to add: {e}')

    def update(self):
        if self.selected_id is None:
            messagebox.showwarning('Selection Error', 'No item selected.')
            return
        payload = self.get_payload()
        if payload is None:
            return
        try:
            resp = requests.put(f"{self.get_api_url()}{self.selected_id}/", json=payload)
            resp.raise_for_status()
            self.load()
        except Exception as e:
            messagebox.showerror('Error', f'Failed to update: {e}')

    def delete(self):
        if self.selected_id is None:
            messagebox.showwarning('Selection Error', 'No item selected.')
            return
        if not messagebox.askyesno('Confirm Delete', 'Are you sure you want to delete this item?'):
            return
        try:
            resp = requests.delete(f"{self.get_api_url()}{self.selected_id}/")
            resp.raise_for_status()
            self.load()
        except Exception as e:
            messagebox.showerror('Error', f'Failed to delete: {e}')

class TallySystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Tally System Manager')
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)
        # Customers
        self.customers_tab = ModelTab(self.notebook, 'customers', ['name'])
        self.notebook.add(self.customers_tab.frame, text='Customers')
        # Plants
        self.plants_tab = ModelTab(self.notebook, 'plants', ['name'])
        self.notebook.add(self.plants_tab.frame, text='Plants')
        # Tally Sessions
        self.tally_sessions_tab = ModelTab(
            self.notebook, 'tally-sessions', ['customer', 'plant', 'status'],
            fk_fields={'customer': ('customers/', 'name'), 'plant': ('plants/', 'name')}
        )
        self.notebook.add(self.tally_sessions_tab.frame, text='Tally Sessions')
        # Weight Classifications
        self.weight_class_tab = ModelTab(
            self.notebook, 'weight-classifications', ['plant', 'classification', 'min_weight', 'max_weight', 'category'],
            fk_fields={'plant': ('plants/', 'name')},
            choices={'category': ['uncategorized', 'byproduct', 'dressed']}
        )
        self.notebook.add(self.weight_class_tab.frame, text='Weight Classifications')
        # Allocation Details
        self.allocations_tab = ModelTab(
            self.notebook, 'allocations', ['tally_session', 'weight_class', 'required_bags', 'allocated_bags'],
            fk_fields={'tally_session': ('tally-sessions/', 'id'), 'weight_class': ('weight-classifications/', 'classification')}
        )
        self.notebook.add(self.allocations_tab.frame, text='Allocation Details')

if __name__ == '__main__':
    root = tk.Tk()
    app = TallySystemApp(root)
    root.mainloop() 
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
        # Add a frame for the listbox and scrollbar
        list_frame = tk.Frame(self.frame)
        list_frame.pack(padx=10, pady=10, fill='both', expand=True)
        self.listbox = tk.Listbox(list_frame, width=60)
        self.listbox.pack(side=tk.LEFT, fill='both', expand=True)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        # Add a vertical scrollbar
        scrollbar = tk.Scrollbar(list_frame, orient='vertical', command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        self.listbox.config(yscrollcommand=scrollbar.set)
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
        # Verbose display for allocations tab
        if self.model == 'allocations':
            # Fetch related data for verbose display
            sessions = fetch_list('tally-sessions/')
            customers = fetch_list('customers/')
            plants = fetch_list('plants/')
            weight_classes = fetch_list('weight-classifications/')
            customer_map = {c['id']: c['name'] for c in customers}
            plant_map = {p['id']: p['name'] for p in plants}
            wc_map = {w['id']: w for w in weight_classes}
            session_map = {s['id']: s for s in sessions}
            for obj in self.data:
                session = session_map.get(obj['tally_session'])
                wc = wc_map.get(obj['weight_class'])
                customer = customer_map.get(session['customer']) if session else 'Unknown'
                plant = plant_map.get(session['plant']) if session else 'Unknown'
                status = session['status'] if session else 'Unknown'
                wc_str = wc['classification'] if wc else str(obj['weight_class'])
                self.listbox.insert(
                    tk.END,
                    f"Session: {session['id'] if session else obj['tally_session']} | Customer: {customer} | Plant: {plant} | Status: {status} | Class: {wc_str} | Required: {obj['required_bags']} | Allocated: {obj['allocated_bags'] if obj['allocated_bags'] is not None else 0}"
                )
        # Verbose display for tally-sessions tab
        elif self.model == 'tally-sessions':
            customers = fetch_list('customers/')
            plants = fetch_list('plants/')
            customer_map = {c['id']: c['name'] for c in customers}
            plant_map = {p['id']: p['name'] for p in plants}
            for obj in self.data:
                customer = customer_map.get(obj['customer'], obj['customer'])
                plant = plant_map.get(obj['plant'], obj['plant'])
                status = obj.get('status', 'Unknown')
                date = obj.get('date', '')
                self.listbox.insert(
                    tk.END,
                    f"Session: {obj['id']} | Customer: {customer} | Plant: {plant} | Status: {status} | Date: {date}"
                )
        else:
            for obj in self.data:
                display = f"{obj['id']}: " + ', '.join(str(obj.get(f, '')) for f in self.fields)
                self.listbox.insert(tk.END, display)
        self.selected_id = None
        for field in self.fk_fields:
            fk_endpoint, fk_label = self.fk_fields[field]
            entry, var = self.entries[field]
            # Special verbose dropdown for tally_session in allocations tab
            if self.model == 'allocations' and field == 'tally_session':
                sessions = fetch_list('tally-sessions/')
                customers = fetch_list('customers/')
                plants = fetch_list('plants/')
                customer_map = {c['id']: c['name'] for c in customers}
                plant_map = {p['id']: p['name'] for p in plants}
                entry['values'] = [
                    f"{s['id']}: {customer_map.get(s['customer'], s['customer'])} | {plant_map.get(s['plant'], s['plant'])} | {s.get('status', '')} | {s.get('date', '')}"
                    for s in sessions
                ]
            else:
                entry['values'] = [f"{item['id']}: {item[fk_label]}" for item in fetch_list(fk_endpoint)]
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
                    # For allocations, allow allocated_bags to be omitted if empty
                    if self.model == 'allocations' and field == 'allocated_bags':
                        continue
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
        # Custom validation for weight-classifications: check for overlapping min/max weight
        if self.model == 'weight-classifications':
            plant_id = payload.get('plant')
            min_w = payload.get('min_weight')
            max_w = payload.get('max_weight')
            if plant_id is not None and min_w is not None and max_w is not None:
                # Fetch all weight classifications for this plant
                all_wcs = fetch_list('weight-classifications/')
                for wc in all_wcs:
                    if wc['plant'] == plant_id:
                        # Check for overlap
                        if not (max_w < wc['min_weight'] or min_w > wc['max_weight']):
                            messagebox.showerror('Conflict', f"Weight range {min_w}-{max_w}kg overlaps with existing classification {wc['classification']} ({wc['min_weight']}-{wc['max_weight']}kg). Please adjust the range.")
                            return
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
        # Special logic for tally-sessions: check for allocation details
        if self.model == 'tally-sessions':
            # Fetch all allocations
            allocations = fetch_list('allocations/')
            tied_allocs = [a for a in allocations if a['tally_session'] == self.selected_id]
            if tied_allocs:
                if messagebox.askyesno('Delete Related?', f'This tally session has {len(tied_allocs)} allocation details tied to it.\nDo you also want to delete those allocation details?'):
                    # Delete all tied allocation details
                    for alloc in tied_allocs:
                        try:
                            resp = requests.delete(f"{API_BASE}allocations/{alloc['id']}/")
                            resp.raise_for_status()
                        except Exception as e:
                            messagebox.showerror('Error', f'Failed to delete allocation detail {alloc['id']}: {e}')
                else:
                    messagebox.showinfo('Orphaned Allocations', 'The allocation details tied to this session will become orphaned.\n\nSuggestions:\n- Edit the allocation details to assign them to another session.\n- Add a note or status to indicate they are orphaned.\n- Delete them manually later.')
        try:
            resp = requests.delete(f"{self.get_api_url()}{self.selected_id}/")
            resp.raise_for_status()
            self.load()
        except Exception as e:
            messagebox.showerror('Error', f'Failed to delete: {e}')

class TallyTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.history = []
        self.customers = fetch_list('customers/')
        self.plants = fetch_list('plants/')
        self.sessions = fetch_list('tally-sessions/')
        self.weight_classes = fetch_list('weight-classifications/')
        self.allocations = fetch_list('allocations/')
        # Customer selection
        customer_row = tk.Frame(self.frame)
        customer_row.pack(fill='x', padx=10, pady=2)
        tk.Label(customer_row, text='Customer', width=18, anchor='w').pack(side=tk.LEFT)
        self.customer_var = tk.StringVar()
        self.customer_combo = ttk.Combobox(customer_row, textvariable=self.customer_var, state='readonly')
        self.customer_combo['values'] = [f"{c['id']}: {c['name']}" for c in self.customers]
        self.customer_combo.pack(side=tk.LEFT, fill='x', expand=True)
        self.customer_combo.bind('<<ComboboxSelected>>', self.on_customer_select)
        # Plant selection
        plant_row = tk.Frame(self.frame)
        plant_row.pack(fill='x', padx=10, pady=2)
        tk.Label(plant_row, text='Plant', width=18, anchor='w').pack(side=tk.LEFT)
        self.plant_var = tk.StringVar()
        self.plant_combo = ttk.Combobox(plant_row, textvariable=self.plant_var, state='readonly')
        self.plant_combo.pack(side=tk.LEFT, fill='x', expand=True)
        self.plant_combo.bind('<<ComboboxSelected>>', self.on_plant_select)
        # Session selection
        session_row = tk.Frame(self.frame)
        session_row.pack(fill='x', padx=10, pady=2)
        tk.Label(session_row, text='Tally Session', width=18, anchor='w').pack(side=tk.LEFT)
        self.session_var = tk.StringVar()
        self.session_combo = ttk.Combobox(session_row, textvariable=self.session_var, state='readonly')
        self.session_combo.pack(side=tk.LEFT, fill='x', expand=True)
        self.session_combo.bind('<<ComboboxSelected>>', self.on_session_select)
        # Allocation details table
        self.alloc_table = tk.Listbox(self.frame, width=80)
        self.alloc_table.pack(padx=10, pady=10)
        # Calculator interface
        calc_row = tk.Frame(self.frame)
        calc_row.pack(fill='x', padx=10, pady=2)
        tk.Label(calc_row, text='Bag Weight', width=18, anchor='w').pack(side=tk.LEFT)
        self.weight_var = tk.StringVar()
        self.weight_entry = tk.Entry(calc_row, textvariable=self.weight_var, width=10)
        self.weight_entry.pack(side=tk.LEFT)
        tk.Label(calc_row, text='Quantity', width=10, anchor='w').pack(side=tk.LEFT)
        self.qty_var = tk.StringVar(value='1')
        tk.Entry(calc_row, textvariable=self.qty_var, width=5).pack(side=tk.LEFT)
        tk.Button(calc_row, text='Add', command=self.add_bag).pack(side=tk.LEFT, padx=5)
        # Number pad
        pad_frame = tk.Frame(self.frame)
        pad_frame.pack(padx=10, pady=2)
        btns = [
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            ['0', '.', 'Del'],
            ['C']
        ]
        for r, row in enumerate(btns):
            for c, char in enumerate(row):
                tk.Button(pad_frame, text=char, width=4, command=lambda ch=char: self.numpad_press(ch)).grid(row=r, column=c, padx=1, pady=1)
        # History
        tk.Label(self.frame, text='History').pack(padx=10, anchor='w')
        self.history_list = tk.Listbox(self.frame, width=80)
        self.history_list.pack(padx=10, pady=5)
        # Internal state
        self.current_customer_id = None
        self.current_plant_id = None
        self.current_session_id = None
        self.filtered_allocs = []

    def numpad_press(self, char):
        if char == 'C':
            self.weight_var.set('')
        elif char == 'Del':
            self.weight_var.set(self.weight_var.get()[:-1])
        else:
            self.weight_var.set(self.weight_var.get() + char)

    def on_customer_select(self, event=None):
        val = self.customer_var.get()
        if not val:
            return
        customer_id = int(val.split(':')[0])
        self.current_customer_id = customer_id
        # Filter plants that have sessions for this customer
        customer_sessions = [s for s in self.sessions if s['customer'] == customer_id]
        # Check for unfinished inactive sessions
        unfinished_inactive = [s for s in customer_sessions if s.get('status') == 'Unfinished (Inactive)']
        if not unfinished_inactive:
            messagebox.showwarning('No Unfinished (Inactive) Session', 'This customer has no Unfinished (Inactive) tally session.')
        plant_ids = sorted(set(s['plant'] for s in customer_sessions))
        filtered_plants = [p for p in self.plants if p['id'] in plant_ids]
        self.plant_combo['values'] = [f"{p['id']}: {p['name']}" for p in filtered_plants]
        self.plant_var.set('')
        self.session_combo['values'] = []
        self.session_var.set('')
        self.alloc_table.delete(0, tk.END)
        self.history_list.delete(0, tk.END)
        self.current_plant_id = None
        self.current_session_id = None

    def on_plant_select(self, event=None):
        val = self.plant_var.get()
        if not val or not self.current_customer_id:
            return
        plant_id = int(val.split(':')[0])
        self.current_plant_id = plant_id
        # Filter sessions for this customer and plant
        filtered_sessions = [s for s in self.sessions if s['plant'] == plant_id and s['customer'] == self.current_customer_id]
        self.session_combo['values'] = [f"{s['id']}: {s['status']} ({s['date']})" for s in filtered_sessions]
        self.session_var.set('')
        self.alloc_table.delete(0, tk.END)
        self.history_list.delete(0, tk.END)
        self.current_session_id = None

    def on_session_select(self, event=None):
        val = self.session_var.get()
        if not val:
            return
        session_id = int(val.split(':')[0])
        self.current_session_id = session_id
        self.update_alloc_table()
        self.history_list.delete(0, tk.END)
        self.history = []

    def update_alloc_table(self):
        self.allocations = fetch_list('allocations/')
        self.weight_classes = fetch_list('weight-classifications/')
        # Filter allocations for this session and plant
        self.filtered_allocs = []
        for alloc in self.allocations:
            # Get weight class for this alloc
            wc = next((w for w in self.weight_classes if w['id'] == alloc['weight_class']), None)
            if not wc:
                continue
            if alloc['tally_session'] == self.current_session_id and wc['plant'] == self.current_plant_id:
                self.filtered_allocs.append((alloc, wc))
        self.alloc_table.delete(0, tk.END)
        for alloc, wc in self.filtered_allocs:
            self.alloc_table.insert(tk.END, f"{wc['classification']} ({wc['min_weight']}-{wc['max_weight']}kg) | Required: {alloc['required_bags']} | Allocated: {alloc['allocated_bags'] if alloc['allocated_bags'] is not None else 0}")

    def add_bag(self):
        if not self.current_customer_id or not self.current_plant_id or not self.current_session_id:
            messagebox.showwarning('Selection Error', 'Please select a customer, plant, and session.')
            return
        try:
            weight = float(self.weight_var.get())
        except ValueError:
            messagebox.showwarning('Input Error', 'Please enter a valid decimal weight.')
            return
        try:
            qty = int(self.qty_var.get())
        except ValueError:
            messagebox.showwarning('Input Error', 'Please enter a valid integer quantity.')
            return
        # Find matching weight class for this plant
        plant_wcs = [w for w in self.weight_classes if w['plant'] == self.current_plant_id]
        match_wc = None
        for wc in plant_wcs:
            if wc['min_weight'] <= weight <= wc['max_weight']:
                match_wc = wc
                break
        if not match_wc:
            messagebox.showerror('No Match', 'No weight classification matches this weight for the selected plant.')
            return
        # Find allocation detail for this session, plant, and weight class
        alloc = next((a for a, w in self.filtered_allocs if w['id'] == match_wc['id']), None)
        if not alloc:
            messagebox.showerror('No Allocation', 'No allocation detail found for this weight class in the selected session.')
            return
        # Update allocated_bags
        new_allocated = (alloc['allocated_bags'] or 0) + qty
        patch = {'allocated_bags': new_allocated}
        try:
            resp = requests.patch(f"{API_BASE}allocations/{alloc['id']}/", json=patch)
            resp.raise_for_status()
        except Exception as e:
            messagebox.showerror('Error', f'Failed to update allocation: {e}')
            return
        self.update_alloc_table()
        # Add to history
        import datetime
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.history.append((now, weight, qty, match_wc['classification']))
        self.history_list.insert(tk.END, f"[{now}] Weight: {weight}kg | Qty: {qty} | Class: {match_wc['classification']}")
        self.weight_var.set('')
        self.qty_var.set('1')

class TallySystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Tally System Manager')
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.notebook = ttk.Notebook(root)
        self.notebook.grid(row=0, column=0, sticky='nsew')
        # Customers
        self.customers_tab = ModelTab(self.notebook, 'customers', ['name'])
        self.notebook.add(self.customers_tab.frame, text='Customers')
        # Plants
        self.plants_tab = ModelTab(self.notebook, 'plants', ['name'])
        self.notebook.add(self.plants_tab.frame, text='Plants')
        # Tally Sessions
        self.tally_sessions_tab = ModelTab(
            self.notebook, 'tally-sessions', ['customer', 'plant', 'status'],
            fk_fields={'customer': ('customers/', 'name'), 'plant': ('plants/', 'name')},
            choices={'status': ['Unfinished (Active)', 'Unfinished (Inactive)', 'Finished']}
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
        # Add Tally tab
        self.tally_tab = TallyTab(self.notebook)
        self.notebook.add(self.tally_tab.frame, text='Tally')

if __name__ == '__main__':
    root = tk.Tk()
    app = TallySystemApp(root)
    root.mainloop() 
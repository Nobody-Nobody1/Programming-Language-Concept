#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import VmPython
import ByteCodeReader


class VMGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('SimpleVM GUI')
        self.geometry('900x600')

        self.vm = VmPython.SimpleVM()
        self.bytecode = []
        self.running = False
        self.breakpoint = None

        self._build_ui()

    def _build_ui(self):
        top = ttk.Frame(self)
        top.pack(fill='x', padx=8, pady=6)

        self.file_entry = ttk.Entry(top)
        self.file_entry.pack(side='left', fill='x', expand=True)
        self.file_entry.insert(0, 'ByteCode.txt')

        ttk.Button(top, text='Load', command=self.load_file).pack(side='left', padx=4)
        ttk.Button(top, text='Reset', command=self.reset_vm).pack(side='left', padx=4)
        ttk.Button(top, text='Step', command=self.gui_step).pack(side='left', padx=4)
        ttk.Button(top, text='Run', command=self.gui_run).pack(side='left', padx=4)
        ttk.Button(top, text='Stop', command=self.gui_stop).pack(side='left', padx=4)

        bp_label = ttk.Label(top, text='Breakpoint (pc):')
        bp_label.pack(side='left', padx=(10, 2))
        self.bp_entry = ttk.Entry(top, width=6)
        self.bp_entry.pack(side='left')

        main = ttk.Frame(self)
        main.pack(fill='both', expand=True, padx=8, pady=6)

        left = ttk.Frame(main)
        left.pack(side='left', fill='y')

        pc_frame = ttk.LabelFrame(left, text='PC / Instruction')
        pc_frame.pack(fill='x', padx=4, pady=4)
        self.pc_var = tk.StringVar(value='0')
        ttk.Label(pc_frame, text='PC:').pack(side='left')
        ttk.Label(pc_frame, textvariable=self.pc_var).pack(side='left')
        self.instr_var = tk.StringVar(value='')
        ttk.Label(pc_frame, text='   Instr:').pack(side='left', padx=(10,0))
        ttk.Label(pc_frame, textvariable=self.instr_var).pack(side='left')

        stack_frame = ttk.LabelFrame(left, text='Stack (top at bottom)')
        stack_frame.pack(fill='y', padx=4, pady=4, expand=True)
        self.stack_list = tk.Listbox(stack_frame, height=20, width=30)
        self.stack_list.pack(fill='both', expand=True)

        mem_frame = ttk.LabelFrame(main, text='Memory')
        mem_frame.pack(side='left', fill='both', expand=True, padx=4, pady=4)
        self.mem_list = tk.Listbox(mem_frame)
        self.mem_list.pack(fill='both', expand=True)

        right = ttk.Frame(main)
        right.pack(side='left', fill='both', expand=True)

        code_frame = ttk.LabelFrame(right, text='Bytecode')
        code_frame.pack(fill='both', expand=True, padx=4, pady=4)
        self.code_text = ScrolledText(code_frame, height=12)
        self.code_text.pack(fill='both', expand=True)

        console_frame = ttk.LabelFrame(right, text='Console')
        console_frame.pack(fill='both', expand=True, padx=4, pady=4)
        self.console = ScrolledText(console_frame, height=10, state='disabled')
        self.console.pack(fill='both', expand=True)

    def append_console(self, text):
        self.console.configure(state='normal')
        self.console.insert('end', str(text) + '\n')
        self.console.see('end')
        self.console.configure(state='disabled')

    def load_file(self):
        path = self.file_entry.get()
        try:
            bc = ByteCodeReader.read_text_file_to_list(path)
        except Exception as e:
            messagebox.showerror('Error', str(e))
            return
        self.bytecode = bc
        # update code view
        self.code_text.delete('1.0', 'end')
        for i, tok in enumerate(self.bytecode):
            self.code_text.insert('end', f'{i}: {tok}\n')
        self.reset_vm()

    def reset_vm(self):
        self.vm.reset()
        self.running = False
        self.update_views()

    def gui_step(self):
        if not self.bytecode:
            self.append_console('No bytecode loaded')
            return
        try:
            cont = self.vm.step(self.bytecode, output_callback=self.append_console)
        except Exception as e:
            messagebox.showerror('Runtime error', str(e))
            return
        self.update_views()

    def _run_step(self):
        # internal runner called via after
        if not self.running:
            return
        # check breakpoint
        bp = None
        try:
            bp_text = self.bp_entry.get().strip()
            if bp_text != '':
                bp = int(bp_text)
        except Exception:
            bp = None

        if bp is not None and self.vm.program_counter == bp:
            self.append_console(f'Hit breakpoint at {bp}')
            self.running = False
            return

        try:
            cont = self.vm.step(self.bytecode, output_callback=self.append_console)
        except Exception as e:
            messagebox.showerror('Runtime error', str(e))
            self.running = False
            return
        self.update_views()
        if cont and self.running:
            # schedule next step
            self.after(50, self._run_step)
        else:
            self.running = False

    def gui_run(self):
        if not self.bytecode:
            self.append_console('No bytecode loaded')
            return
        if self.running:
            return
        self.running = True
        self.after(1, self._run_step)

    def gui_stop(self):
        self.running = False

    def update_views(self):
        self.pc_var.set(str(self.vm.program_counter))
        instr = ''
        if 0 <= self.vm.program_counter < len(self.bytecode):
            instr = str(self.bytecode[self.vm.program_counter])
        self.instr_var.set(instr)

        # stack
        self.stack_list.delete(0, 'end')
        for item in reversed(self.vm.stack):
            self.stack_list.insert('end', repr(item))

        # memory
        self.mem_list.delete(0, 'end')
        for k, v in sorted(self.vm.memory.items()):
            self.mem_list.insert('end', f'{k}: {v}')

        # refresh code highlighting (simple)
        self.code_text.tag_remove('pc', '1.0', 'end')
        if 0 <= self.vm.program_counter < len(self.bytecode):
            line = self.vm.program_counter + 1
            start = f'{line}.0'
            end = f'{line}.end'
            self.code_text.tag_add('pc', start, end)
            self.code_text.tag_config('pc', background='#ffffcc')


if __name__ == '__main__':
    app = VMGui()
    # try to load default file
    try:
        app.load_file()
    except Exception:
        pass
    app.mainloop()

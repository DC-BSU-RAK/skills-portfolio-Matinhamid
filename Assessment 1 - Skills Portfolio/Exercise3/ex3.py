import tkinter as tk
from tkinter import ttk, messagebox
import os
from functools import partial
from PIL import Image, ImageTk 

DATA_FILE = "studentMarks.txt"
BG_IMAGE_FILE = "background.png" 

def ensure_datafile():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            f.write("0\n")

def read_students():
    ensure_datafile()
    students = []
    with open(DATA_FILE, "r") as f:
        lines = [ln.rstrip("\n") for ln in f if ln.strip() != ""]
    if not lines:
        return students
    try:
        count = int(lines[0])
    except Exception:
        lines.insert(0, "0")
        count = 0
    for line in lines[1:]:
        parts = [p.strip() for p in line.split(",")]
        if len(parts) != 6:
            continue
        code, name, c1, c2, c3, exam = parts
        try:
            students.append({
                "code": code,
                "name": name,
                "c1": int(c1),
                "c2": int(c2),
                "c3": int(c3),
                "exam": int(exam)
            })
        except ValueError:
            continue
    return students

def write_students(students):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        f.write(f"{len(students)}\n")
        for s in students:
            f.write(f"{s['code']},{s['name']},{s['c1']},{s['c2']},{s['c3']},{s['exam']}\n")

def coursework_total(s):
    return s["c1"] + s["c2"] + s["c3"]

def overall_percentage(s):
    total = coursework_total(s) + s["exam"]
    return round((total / 160.0) * 100.0, 2)

def grade_from_percentage(p):
    if p >= 70: return "A"
    if p >= 60: return "B"
    if p >= 50: return "C"
    if p >= 40: return "D"
    return "F"

class StudentManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Manager")
        self.geometry("1000x650") 
        self.minsize(800, 500)

        self.students = read_students()

        top = tk.Frame(self, bg="#2c3e50") 
        top.pack(fill="x")
        tk.Label(top, text="Student Manager System", font=("Segoe UI", 18, "bold"), bg="#2c3e50", fg="white", pady=10).pack(side="left", padx=10)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        menu_frame = tk.Frame(container, width=220, bg="#ecf0f1") 
        menu_frame.pack(side="left", fill="y")
        menu_frame.pack_propagate(False)

        btn_specs = [
            ("View All Students", self.show_view_all),
            ("View Individual", self.show_view_one_form),
            ("Highest Score", self.show_highest),
            ("Lowest Score", self.show_lowest),
            ("Sort Records", self.show_sort_options),
            ("Add Student", self.show_add_form),
            ("Delete Student", self.show_delete_form),
            ("Update Student", self.show_update_form),
            ("Save to File", self.save_to_file),
        ]

        for (text, cmd) in btn_specs:
            b = tk.Button(
                menu_frame, 
                text=text, 
                anchor="center",
                command=cmd,
                font=("Segoe UI", 11),
                bg="white", 
                relief="groove",
                bd=1
            )
            b.pack(fill="x", pady=5, padx=10, ipady=5)

        self.content_canvas = tk.Canvas(container, bg="gray")
        self.content_canvas.pack(side="left", fill="both", expand=True)

        self.bg_image_ref = None 
        self.set_background_image()

        self.frames = {}
        self.create_frames()
        
    def set_background_image(self):
        try:
            pil_image = Image.open(BG_IMAGE_FILE)
            pil_image = pil_image.resize((1200, 800)) 
            self.bg_image_ref = ImageTk.PhotoImage(pil_image)
            self.content_canvas.create_image(0, 0, image=self.bg_image_ref, anchor="nw")
            
        except Exception as e:
            print(f"Resim hatası: {e}")
            self.content_canvas.config(bg="#34495e") 

    def create_frames(self):
        f_text = tk.Frame(self.content_canvas, bd=2, relief="raised")
        txt = tk.Text(f_text, wrap="none", font=("Consolas", 11))
        txt.pack(fill="both", expand=True, side="left")
        ysb = tk.Scrollbar(f_text, orient="vertical", command=txt.yview)
        txt.config(yscrollcommand=ysb.set); ysb.pack(side="right", fill="y")
        self.frames["text"] = {"frame": f_text, "widget": txt}


        f_one = tk.Frame(self.content_canvas, bd=2, relief="raised", padx=20, pady=20)
        tk.Label(f_one, text="SEARCH STUDENT", font=("Segoe UI", 14, "bold")).pack(pady=10)
        lbl = tk.Label(f_one, text="Enter Code or Name:", anchor="w")
        lbl.pack(fill="x")
        entry = tk.Entry(f_one, font=("Segoe UI", 11)); entry.pack(fill="x", pady=5)
        btn = tk.Button(f_one, text="Search", bg="#3498db", fg="white", command=lambda e=entry: self.do_search_one(e.get()))
        btn.pack(pady=10, fill="x")
        res = tk.Text(f_one, wrap="none", height=10, font=("Consolas", 11), bg="#f9f9f9")
        res.pack(fill="both", expand=True)
        self.frames["one"] = {"frame": f_one, "entry": entry, "result": res}

        f_sort = tk.Frame(self.content_canvas, bd=2, relief="raised", padx=20, pady=20)
        tk.Label(f_sort, text="SORT OPTIONS", font=("Segoe UI", 14, "bold")).pack(pady=10)
        order_var = tk.StringVar(value="desc")
        tk.Radiobutton(f_sort, text="Descending (Highest First)", variable=order_var, value="desc", font=("Segoe UI", 11)).pack(anchor="w", pady=5)
        tk.Radiobutton(f_sort, text="Ascending (Lowest First)", variable=order_var, value="asc", font=("Segoe UI", 11)).pack(anchor="w", pady=5)
        tk.Button(f_sort, text="Sort Now", bg="#e67e22", fg="white", command=lambda: self.do_sort(order_var.get())).pack(pady=15, fill="x")
        self.frames["sort"] = {"frame": f_sort, "order_var": order_var}

        f_add = tk.Frame(self.content_canvas, bd=2, relief="raised", padx=20, pady=20)
        tk.Label(f_add, text="ADD NEW STUDENT", font=("Segoe UI", 14, "bold")).pack(pady=10)
        form = {}
        fields = [("Code", "code"), ("Name", "name"), ("CW1 (0-20)", "c1"), ("CW2 (0-20)", "c2"), ("CW3 (0-20)", "c3"), ("Exam (0-100)", "exam")]
        for label_text, key in fields:
            row = tk.Frame(f_add); row.pack(fill="x", pady=2)
            tk.Label(row, text=label_text, width=15, anchor="w").pack(side="left")
            ent = tk.Entry(row); ent.pack(side="left", fill="x", expand=True)
            form[key] = ent
        tk.Button(f_add, text="Save Student", bg="#27ae60", fg="white", command=lambda: self.do_add_student(form)).pack(pady=15, fill="x")
        self.frames["add"] = {"frame": f_add, "form": form}

        f_del = tk.Frame(self.content_canvas, bd=2, relief="raised", padx=20, pady=20)
        tk.Label(f_del, text="DELETE STUDENT", font=("Segoe UI", 14, "bold")).pack(pady=10)
        tk.Label(f_del, text="Student Code:", anchor="w").pack(fill="x")
        del_entry = tk.Entry(f_del, font=("Segoe UI", 11)); del_entry.pack(fill="x", pady=5)
        tk.Button(f_del, text="Delete Permanently", bg="#c0392b", fg="white", command=lambda: self.do_delete_student(del_entry.get())).pack(pady=15, fill="x")
        self.frames["delete"] = {"frame": f_del, "entry": del_entry}

        f_upd = tk.Frame(self.content_canvas, bd=2, relief="raised", padx=20, pady=20)
        tk.Label(f_upd, text="UPDATE STUDENT", font=("Segoe UI", 14, "bold")).pack(pady=10)
        up_code = tk.Entry(f_upd); up_code.pack(fill="x", pady=5)
        tk.Button(f_upd, text="Load Data", command=lambda: self.load_student_for_update(up_code.get())).pack(fill="x")
        
        edit_cont = tk.Frame(f_upd, pady=10); edit_cont.pack(fill="both", expand=True)
        edit_widgets = {}
        for label_text, key in fields:
            row = tk.Frame(edit_cont); row.pack(fill="x", pady=2)
            tk.Label(row, text=label_text, width=15, anchor="w").pack(side="left")
            ent = tk.Entry(row); ent.pack(side="left", fill="x", expand=True)
            edit_widgets[key] = ent
        tk.Button(edit_cont, text="Save Changes", bg="#2980b9", fg="white", command=lambda: self.do_save_updated_student(edit_widgets)).pack(pady=10, fill="x")
        self.frames["update"] = {"frame": f_upd, "code_entry": up_code, "widgets": edit_widgets}


    def hide_all_frames(self):
        for info in self.frames.values():
            info["frame"].place_forget()

    def show_frame(self, key):
        self.hide_all_frames()
        info = self.frames[key]
        info["frame"].place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.85)

    def show_view_all(self):
        self.show_frame("text")
        txt = self.frames["text"]["widget"]
        txt.delete("1.0", "end")
        if not self.students:
            txt.insert("end", "No student records found.\n")
            return

        headers = f"{'Name':<25} {'Code':<8} {'CW Total':<10} {'Exam':<6} {'%':<6} {'Grade':<6}"
        txt.insert("end", headers + "\n")
        txt.insert("end", "-" * 85 + "\n")
        
        total_percent = 0.0
        for s in self.students:
            percent = overall_percentage(s)
            total_percent += percent
            row = f"{s['name'][:25]:<25} {s['code']:<8} {coursework_total(s):<10} {s['exam']:<6} {percent:<6.1f} {grade_from_percentage(percent):<6}\n"
            txt.insert("end", row)
            
        avg = round(total_percent / len(self.students), 2)
        txt.insert("end", "\n" + "-" * 30 + "\n")
        txt.insert("end", f"Total students: {len(self.students)}\n")
        txt.insert("end", f"Class average:  {avg}%\n")

    def show_view_one_form(self):
        self.show_frame("one")
        self.frames["one"]["entry"].delete(0, "end")
        self.frames["one"]["result"].delete("1.0", "end")

    def do_search_one(self, query):
        q = query.strip().lower()
        res = self.frames["one"]["result"]
        res.delete("1.0", "end")
        if not q:
            res.insert("end", "Please enter a code or name.\n"); return
        found = [s for s in self.students if q == s["code"].lower() or q in s["name"].lower()]
        if not found: res.insert("end", "No matching student found.\n"); return
        for s in found:
            p = overall_percentage(s)
            res.insert("end", f"Name: {s['name']} (Code: {s['code']})\n")
            res.insert("end", f"Overall: {p}% - Grade: {grade_from_percentage(p)}\n")
            res.insert("end", "-" * 40 + "\n")

    def show_highest(self):
        if not self.students: messagebox.showinfo("Info", "No data"); return
        best = max(self.students, key=lambda s: overall_percentage(s))
        self.show_frame("text")
        self.frames["text"]["widget"].delete("1.0", "end")
        self.frames["text"]["widget"].insert("end", f"HIGHEST SCORE: {best['name']} ({overall_percentage(best)}%)")

    def show_lowest(self):
        if not self.students: messagebox.showinfo("Info", "No data"); return
        worst = min(self.students, key=lambda s: overall_percentage(s))
        self.show_frame("text")
        self.frames["text"]["widget"].delete("1.0", "end")
        self.frames["text"]["widget"].insert("end", f"LOWEST SCORE: {worst['name']} ({overall_percentage(worst)}%)")

    def show_sort_options(self): self.show_frame("sort")
    
    def do_sort(self, order):
        self.students.sort(key=lambda s: overall_percentage(s), reverse=(order == "desc"))
        write_students(self.students)
        messagebox.showinfo("Sorted", "Done.")
        self.show_view_all()

    def show_add_form(self):
        self.show_frame("add")
        for ent in self.frames["add"]["form"].values(): ent.delete(0, "end")

    def do_add_student(self, form):
        try:
            code, name = form["code"].get(), form["name"].get()
            c1, c2, c3, ex = int(form["c1"].get()), int(form["c2"].get()), int(form["c3"].get()), int(form["exam"].get())
            if not code or not name: raise ValueError
        except: messagebox.showerror("Error", "Check inputs"); return
        
        self.students.append({"code": code, "name": name, "c1": c1, "c2": c2, "c3": c3, "exam": ex})
        write_students(self.students)
        messagebox.showinfo("Success", "Added")
        self.show_view_all()

    def show_delete_form(self):
        self.show_frame("delete")
        self.frames["delete"]["entry"].delete(0, "end")

    def do_delete_student(self, code):
        found = next((s for s in self.students if s["code"] == code), None)
        if found and messagebox.askyesno("Confirm", "Delete?"):
            self.students.remove(found)
            write_students(self.students)
            self.show_view_all()

    def show_update_form(self):
        self.show_frame("update")
    
    def load_student_for_update(self, code):
        found = next((s for s in self.students if s["code"] == code), None)
        if not found: messagebox.showerror("Error", "Not found"); return
        w = self.frames["update"]["widgets"]
        w["code"].delete(0,"end"); w["code"].insert(0, found["code"])
        w["name"].delete(0,"end"); w["name"].insert(0, found["name"])
        w["c1"].delete(0,"end"); w["c1"].insert(0, str(found["c1"]))
        w["c2"].delete(0,"end"); w["c2"].insert(0, str(found["c2"]))
        w["c3"].delete(0,"end"); w["c3"].insert(0, str(found["c3"]))
        w["exam"].delete(0,"end"); w["exam"].insert(0, str(found["exam"]))

    def do_save_updated_student(self, widgets):
        self.do_add_student(widgets) 

    def save_to_file(self):
        write_students(self.students)
        messagebox.showinfo("Saved", "File updated")

if __name__ == "__main__":
    app = StudentManagerApp()
    app.mainloop()
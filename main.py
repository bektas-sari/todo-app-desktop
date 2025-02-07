import customtkinter as ctk
import datetime
import tkinter.messagebox as messagebox
from tkcalendar import DateEntry  # pip install tkcalendar

# --- Task Modeli ---
class Task:
    def __init__(self, title, description, due_date, priority="Medium"):
        self.title = title
        self.description = description
        self.due_date = due_date  # dd/mm/yyyy formatında string
        self.priority = priority
        self.completed = False

# --- Uygulama Sınıfı ---
class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("To-Do Application")
        self.geometry("800x600")

        # Uygulamadaki görevleri saklayacağımız liste
        self.tasks = []

        # Sol tarafta görev ekleme formu için frame
        self.create_task_input_frame()

        # Sağ tarafta görev listesini göstereceğimiz frame
        self.create_task_list_frame()

    def create_task_input_frame(self):
        self.input_frame = ctk.CTkFrame(self, width=300)
        self.input_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Görev Başlığı
        self.title_label = ctk.CTkLabel(self.input_frame, text="Task Title:")
        self.title_label.pack(pady=(10, 0))
        self.title_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Enter task title")
        self.title_entry.pack(pady=5, padx=10)

        # Açıklama
        self.desc_label = ctk.CTkLabel(self.input_frame, text="Description:")
        self.desc_label.pack(pady=(10, 0))
        self.desc_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Enter description")
        self.desc_entry.pack(pady=5, padx=10)

        # Son Tarih (DateEntry widget'ı kullanılıyor)
        self.date_label = ctk.CTkLabel(self.input_frame, text="Due Date:")
        self.date_label.pack(pady=(10, 0))
        # Kullanıcı takvimden tarih seçebilsin; format: dd/mm/yyyy
        self.date_entry = DateEntry(self.input_frame, date_pattern="dd/mm/yyyy")
        self.date_entry.pack(pady=5, padx=10)

        # Öncelik
        self.priority_label = ctk.CTkLabel(self.input_frame, text="Priority:")
        self.priority_label.pack(pady=(10, 0))
        self.priority_var = ctk.StringVar(value="Medium")
        self.priority_dropdown = ctk.CTkOptionMenu(
            self.input_frame,
            values=["High", "Medium", "Low"],
            variable=self.priority_var
        )
        self.priority_dropdown.pack(pady=5, padx=10)

        # Görev Ekleme Butonu
        self.add_task_button = ctk.CTkButton(self.input_frame, text="Add Task", command=self.add_task)
        self.add_task_button.pack(pady=20)

    def create_task_list_frame(self):
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Scrollable alanda görevlerin listeleneceği frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self.list_frame)
        self.scrollable_frame.pack(fill="both", expand=True)

    def add_task(self):
        title = self.title_entry.get().strip()
        description = self.desc_entry.get().strip()
        due_date = self.date_entry.get().strip()  # dd/mm/yyyy formatında
        priority = self.priority_var.get()

        if not title:
            messagebox.showerror("Input Error", "Task title is required.")
            return

        # Tarih formatını doğrulama (dd/mm/yyyy)
        try:
            datetime.datetime.strptime(due_date, "%d/%m/%Y").date()
        except ValueError:
            messagebox.showerror("Input Error", "Due date must be in dd/mm/yyyy format.")
            return

        new_task = Task(title, description, due_date, priority)
        self.tasks.append(new_task)
        self.display_task(new_task)
        self.clear_input_fields()

    def clear_input_fields(self):
        self.title_entry.delete(0, "end")
        self.desc_entry.delete(0, "end")
        # DateEntry widget'ı için mevcut tarih ayarlanıyor
        self.date_entry.set_date(datetime.datetime.today())
        self.priority_var.set("Medium")

    def display_task(self, task):
        # Her görevi göstermek için ayrı bir frame oluşturuyoruz
        task_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent", border_width=1, border_color="gray")
        task_frame.pack(fill="x", padx=5, pady=5)

        # Görev başlığı (tamamlanmışsa üzerinde değişiklik yapılacak)
        title_label = ctk.CTkLabel(task_frame, text=task.title, font=("Helvetica", 16, "bold"))
        title_label.pack(anchor="w", padx=5, pady=(5, 0))

        # Açıklama
        desc_label = ctk.CTkLabel(task_frame, text=task.description)
        desc_label.pack(anchor="w", padx=5)

        # Son tarih ve öncelik bilgisi
        info_label = ctk.CTkLabel(task_frame,
                                  text=f"Due: {task.due_date}   Priority: {task.priority}")
        info_label.pack(anchor="w", padx=5, pady=(0, 5))

        # İşlem butonlarının bulunduğu alan
        btn_frame = ctk.CTkFrame(task_frame, fg_color="transparent")
        btn_frame.pack(anchor="e", padx=5, pady=(0, 5))

        complete_btn = ctk.CTkButton(btn_frame, text="Complete",
                                     command=lambda: self.mark_complete(task, title_label))
        complete_btn.pack(side="left", padx=5)

        edit_btn = ctk.CTkButton(btn_frame, text="Edit",
                                 command=lambda: self.edit_task(task, task_frame))
        edit_btn.pack(side="left", padx=5)

        delete_btn = ctk.CTkButton(btn_frame, text="Delete",
                                   command=lambda: self.delete_task(task, task_frame))
        delete_btn.pack(side="left", padx=5)

    def mark_complete(self, task, title_label):
        task.completed = True
        # Başlık güncelleniyor: tamamlanmış ise (Completed) ifadesi ekleniyor ve renk yeşile dönüyor
        title_label.configure(text=f"{task.title} (Completed)", text_color="green")

    def edit_task(self, task, task_frame):
        # Düzenleme için ayrı bir pencere (Toplevel) açıyoruz
        edit_window = ctk.CTkToplevel(self)
        edit_window.title("Edit Task")
        edit_window.geometry("400x350")
        # Pencereyi modal hale getiriyoruz
        edit_window.grab_set()
        edit_window.focus_force()

        # Görev Başlığı
        title_lbl = ctk.CTkLabel(edit_window, text="Task Title:")
        title_lbl.pack(pady=(10, 0))
        title_entry = ctk.CTkEntry(edit_window, placeholder_text="Enter task title")
        title_entry.insert(0, task.title)
        title_entry.pack(pady=5, padx=10)

        # Açıklama
        desc_lbl = ctk.CTkLabel(edit_window, text="Description:")
        desc_lbl.pack(pady=(10, 0))
        desc_entry = ctk.CTkEntry(edit_window, placeholder_text="Enter description")
        desc_entry.insert(0, task.description)
        desc_entry.pack(pady=5, padx=10)

        # Son Tarih (DateEntry widget'ı kullanılıyor)
        date_lbl = ctk.CTkLabel(edit_window, text="Due Date:")
        date_lbl.pack(pady=(10, 0))
        date_entry = DateEntry(edit_window, date_pattern="dd/mm/yyyy")
        try:
            current_date = datetime.datetime.strptime(task.due_date, "%d/%m/%Y")
            date_entry.set_date(current_date)
        except ValueError:
            date_entry.set_date(datetime.datetime.today())
        date_entry.pack(pady=5, padx=10)

        # Öncelik
        priority_lbl = ctk.CTkLabel(edit_window, text="Priority:")
        priority_lbl.pack(pady=(10, 0))
        priority_var = ctk.StringVar(value=task.priority)
        priority_dropdown = ctk.CTkOptionMenu(edit_window,
                                              values=["High", "Medium", "Low"],
                                              variable=priority_var)
        priority_dropdown.pack(pady=5, padx=10)

        def save_changes():
            new_title = title_entry.get().strip()
            new_desc = desc_entry.get().strip()
            new_date = date_entry.get().strip()  # dd/mm/yyyy formatında
            new_priority = priority_var.get()

            if not new_title:
                messagebox.showerror("Input Error", "Task title is required.")
                return

            try:
                datetime.datetime.strptime(new_date, "%d/%m/%Y").date()
            except ValueError:
                messagebox.showerror("Input Error", "Due date must be in dd/mm/yyyy format.")
                return

            # Görev bilgilerini güncelle
            task.title = new_title
            task.description = new_desc
            task.due_date = new_date
            task.priority = new_priority

            # Eski task widget'ını kaldırıp, güncellenmiş halini yeniden ekliyoruz
            task_frame.destroy()
            self.display_task(task)
            edit_window.destroy()

        save_btn = ctk.CTkButton(edit_window, text="Save Changes", command=save_changes)
        save_btn.pack(pady=20)

    def delete_task(self, task, task_frame):
        if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this task?"):
            self.tasks.remove(task)
            task_frame.destroy()

if __name__ == "__main__":
    # CustomTkinter ayarları: "System", "Dark" veya "Light" modları kullanılabilir.
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")  # Temalar: "blue", "green", "dark-blue", vb.
    app = TodoApp()
    app.mainloop()

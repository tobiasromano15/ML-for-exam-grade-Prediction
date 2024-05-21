import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import pandas as pd
from joblib import dump, load


class AppV2:
    file_path = 'C:\\Users\\Tobi\\Desktop\\Investigacion Operativa\\unload_20220722\\002_materias_cursadas.csv'

    try:
        df = pd.read_csv(file_path, delimiter='|', encoding='latin-1')
    except UnicodeDecodeError as e:
        print("Error with Latin-1, trying another encoding:", e)

    try:
        df = pd.read_csv(file_path, delimiter='|', encoding='windows-1252')
    except UnicodeDecodeError as e:
        print("Error with Windows-1252, trying another encoding:", e)
    df = df[df['plan'] == '2011']
    df.sort_values(by=['id', 'fecha_regularidad'], inplace=True)
    df = df.groupby(['id', 'materia']).last().reset_index()

    def __init__(self, root,plan):
        self.plan = plan
        self.root = root
        root.title('Información de Estudiantes')
        root.geometry("600x400")
        self.label = tk.Label(root, text="Ingrese ID del Estudiante:")
        self.label.pack()

        self.entry = tk.Entry(root)
        self.entry.pack()

        self.search_button = tk.Button(root, text="Buscar", command=self.search_student)
        self.search_button.pack()

        self.result_text = tk.Text(root, height=10, width=80)
        self.result_text.pack()

        self.prediction_label = tk.Label(root, text="Seleccione una materia para predecir:")
        self.prediction_label.pack()

        self.materia_combobox = ttk.Combobox(root)
        self.materia_combobox.pack()

        self.predict_button = tk.Button(root, text="Predecir Nota", command=self.predict_grade)
        self.predict_button.pack()

        self.current_student_data = None  # Para almacenar los datos del estudiante actual

    def search_student(self):
        student_id = self.entry.get()
        if student_id.isdigit():
            student_id = int(student_id)
            self.display_student_info(student_id)
        else:
            messagebox.showerror("Error", "Por favor, ingrese un ID válido.")

    def display_student_info(self, student_id):
        self.current_student_data = self.df[self.df['id'] == student_id]
        if not self.current_student_data.empty:
            self.result_text.delete(1.0, tk.END)
            materias = []
            for index, row in self.current_student_data.iterrows():
                self.result_text.insert(tk.END, f"Materia: {row['nombre_materia']}, Nota: {row['nota']}\n")
                materias.append(row['nombre_materia'])
            self.materia_combobox['values'] = materias
        else:
            messagebox.showinfo("Información", "No se encontró información para el ID proporcionado.")

    def predict_grade(self):
        materia = self.materia_combobox.get()
        if materia:
            # Obtener la nota de prerequisito de los datos actuales del estudiante
            nota = self.current_student_data[self.current_student_data['nombre_materia'] == materia]['nota'].values[0]

            # Cargar el modelo de regresión logística
            model = load('modelo_entrenado.joblib')
            # Crear un DataFrame con la estructura requerida por el modelo
            feature_names = model.feature_names_in_
            input_data = pd.DataFrame(False, index=[0], columns=feature_names)
            nota = nota.replace(',', '.')
            nota = float(nota)
            if materia and nota is not None and nota > 0 and nota < 10:
                if nota >= 4:
                    input_data['res_A'] = True
                else:
                    input_data['res_R'] = True
                mat = 'prereq_' + str(float(self.plan.getSubjectbyName(materia).id))
                input_data[mat] = True
                input_data.at[0, 'nota_prereq'] = nota
                for m in self.plan.getSubjectbyName(materia).correlativas:
                    corr = 'corr_' + str(m.id)
                    input_data[corr] = True
                    # Aquí debes ajustar cómo se crea el DataFrame en base a cómo se entrenó tu modelo
                    prediction = model.predict(input_data)  # Ajusta esto según tus características
                    if prediction[0] == 1:
                        msg = 'el alumno aprobara'
                    else:
                        msg = 'el alumno reprobara'

                    messagebox.showinfo("Predicción",
                                        f"Lo mas probable es que para la materia {m.nombre} que es correlativa de {materia} {msg} {prediction}")
                    input_data[corr] = False
                    input_data['res_A'] = False
                    input_data['res_R'] = False
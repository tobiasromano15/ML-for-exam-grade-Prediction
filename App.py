import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, Listbox
from joblib import dump, load
import pandas as pd

class App:
    def __init__(self, root,plan):
        self.plan = plan
        self.root = root
        root.title('Modelo de Predicción de Notas')
        root.geometry("600x400")  # Ajusta el tamaño de la ventana principal

        # Lista de materias
        self.materias_listbox = Listbox(root)
        self.materias_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.load_materias()

        # Botón para predecir datos
        self.predict_button = tk.Button(root, text="Predecir Notas", command=self.predict_data)
        self.predict_button.pack(side=tk.RIGHT)

    def load_materias(self):
        # Supongamos que tienes una lista de materias así:
        for materia in self.plan.materias:
            self.materias_listbox.insert(tk.END, materia.nombre)
    def predict_data(self):
        selected_index = self.materias_listbox.curselection()
        materia = self.materias_listbox.get(selected_index)
        model = load('modelo_entrenado.joblib')
        print(self.plan.getSubjectbyName(materia))
        feature_names = model.feature_names_in_

        # Crear un DataFrame vacío con las características especificadas
        input_data = pd.DataFrame(False, index=[0], columns=feature_names)

        nota = simpledialog.askfloat("Entrada", "Ingrese la nota obtenida:")
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
                    msg= 'aprobaras'
                else:
                    msg = 'desaprobaras'

                messagebox.showinfo("Predicción",
                                    f"Lo mas probable es que para la materia {m.nombre} que es correlativa de {materia} {msg} {prediction}")
                input_data[corr] = False
                input_data['res_A'] = False
                input_data['res_R'] = False


import AppV2
import studyPlan
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score
from joblib import dump


import tkinter as tk

import App
def createPlan():
    carrera = studyPlan.studyPlan("Ingenieria de Sistemas", 2011)
    file_path = 'C:\\Users\\Tobi\\Desktop\\Investigacion Operativa\\unload_20220722\\000_atrib_plan.csv'

    # Try different encodings
    try:
        df = pd.read_csv(file_path, delimiter='|', encoding='latin-1')
    except UnicodeDecodeError as e:
        print("Error with Latin-1, trying another encoding:", e)

    # If Latin-1 doesn't work, you might try 'windows-1252'
    try:
        df = pd.read_csv(file_path, delimiter='|', encoding='windows-1252')
    except UnicodeDecodeError as e:
        print("Error with Windows-1252, trying another encoding:", e)

    df_filter = df[df['plan'] == '2011']
    df_filter2 = df_filter[df_filter['obligatoria'] == 'S']

    plan = studyPlan.studyPlan()

    for materia, nombre_materia in zip(df_filter2['materia'], df_filter2['nombre_materia']):
        subj = studyPlan.subject(materia, nombre_materia)
        plan.addSubject(subj)
    plan.asignarCorrelativa()
    #print(plan)
    return plan
def createDataSet(plan):
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
    #print(df)
    df_merged2 = pd.DataFrame()
    for i in plan.materias:
        df_prereq = df[df['materia'] == i.id][['id', 'nota','materia']]
        df_prereq.rename(columns={'nota': 'nota_prereq'}, inplace=True)
        df_prereq.rename(columns={'nombre_materia': 'materia_prereq'}, inplace=True)
        #print(df_prereq)
        # Hacer un merge con las notas de la materia correlativa.
        for j in i.correlativas:
            df_corr = df[df['materia'] == j.id]
            df_merged1 = pd.merge(df_corr, df_prereq, on='id', how='left')
            df_merged1 = df_merged1.dropna(subset='nota_prereq')
            df_merged2 = pd.concat([df_merged2, df_merged1], ignore_index=True)
    df_merged2.drop(columns=['Unnamed: 12'], inplace=True)
    # Ahora df_merged contiene las notas de la materia y de su correlativa.
    #print(df_merged2)
    return df_merged2




def model(df):
    # Convertir 'nota_prereq' y 'nota' a flotantes, manejar comas como decimales
    df['nota_prereq'] = df['nota_prereq'].str.replace(',', '.').astype(float)
    df['nota'] = pd.to_numeric(df['nota'], errors='coerce')
    df['nota_prereq'] = pd.to_numeric(df['nota_prereq'], errors='coerce')
    df['resultado'] = df['resultado'].replace({'P': 'A', 'U': 'R'})
    materia_prereq_dummies = pd.get_dummies(df['materia_y'], prefix='prereq')
    materia_corr_dummies = pd.get_dummies(df['materia_x'], prefix='corr')
    result_dummies = pd.get_dummies(df['resultado'], prefix='res')
    print(result_dummies)
    # Unir las variables dummy al DataFrame original
    df = pd.concat([df, materia_prereq_dummies, materia_corr_dummies, result_dummies], axis=1)

    # Definir las características para el entrenamiento
    feature_columns = ['nota_prereq'] + list(materia_prereq_dummies.columns) + list(
        materia_corr_dummies.columns) + list(result_dummies.columns)
    X = df[feature_columns]
    # Convertir las notas a clasificación binaria, asumiendo que 4 es la nota de aprobación
    df['passed'] = (df['nota'] >= 4).astype(int)

    # Definir características y objetivo
    y = df['passed']
    print(X)
    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Crear y entrenar el modelo de regresión logística
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    # Hacer predicciones
    y_pred = model.predict(X_test)
    # Evaluar el modelo
    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])

    # Imprimir las métricas
    print(f'Accuracy: {accuracy}')
    print(f'Confusion Matrix:\n{conf_matrix}')
    print(f'ROC-AUC Score: {roc_auc}')
    #print(model.feature_names_in_)
    # Guardar el modelo entrenado
    dump(model, 'modelo_entrenado.joblib')


def main():
    plan = createPlan()
    df = createDataSet(plan)
    model(df)
    root = tk.Tk()
    app = AppV2.AppV2(root,plan)
    root.mainloop()

if __name__ == "__main__":
    main()
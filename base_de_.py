# -- coding: utf-8 --

import streamlit as st
from pymongo import MongoClient
from bson.objectid import ObjectId
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="🐾 Veterinaria Caramelo 🐾",
    layout="wide"
) 

st.markdown("""
<style>

.block-container{
    padding-top: 0rem !important;
    margin-top: 0rem !important;
}

.stApp{
    background:linear-gradient(
    135deg,
    #FFF8F0,
    #F4ECE2
    );
}

[data-testid="stSidebar"]{
    background:#F7ECE3;
}

<h1>{
    color:#C45B3D !important;
    text-align:center;
    font-size:50px !important;
}

h2,h3{
    color:#C45B3D !important;
} 
.stButton>button{
    background:#C45B3D;
    color:white;
    border:none;
    border-radius:15px;
    padding:10px 20px;
    font-weight:bold;
} 
.stButton>button:hover{
    background:#A5472F;
}

.card{
    background:white;
    border-radius:20px;
    padding:20px;
    box-shadow:0px 5px 15px rgba(0,0,0,0.15);
    margin-bottom:15px;
}

.banner{
    background:linear-gradient(
    90deg,
    #C45B3D,
    #E08A68
    );
    padding:35px;
    border-radius:25px;
    color:white;
    text-align:center;
    box-shadow:0px 6px 18px rgba(0,0,0,0.15);
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* Oculta menú */
#MainMenu{
    visibility:hidden;
}

/* Oculta footer */
footer{
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="banner">

<h1 style="color:white;">
🐾 Veterinaria Caramelo 🐾
</h1>

<h3 style="color:white;">
❤️ Para ofrecerle un buen trato y cariño a tus mascotas ❤️
</h3>

</div>
""", unsafe_allow_html=True)

URI = 'mongodb+srv://VMJesusA:saido2009@cluster0.95oxbsm.mongodb.net/?appName=Cluster0'

@st.cache_resource
def init_connection():
    return MongoClient(URI)

cliente = init_connection()

db = cliente["Veterinaria"]

coleccion_mascota = db["mascota"]
coleccion_vacuna = db["vacuna"]
coleccion_adoptante = db["Adoptante"]

try:
    total_mascotas = coleccion_mascota.count_documents({})
    total_vacunas = coleccion_vacuna.count_documents({})
    total_adoptantes = coleccion_adoptante.count_documents({})

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("🐶 Mascotas", total_mascotas)

    with c2:
        st.metric("💉 Vacunas", total_vacunas)

    with c3:
        st.metric("👨‍👩‍👧 Adoptantes", total_adoptantes)
except:
    pass

st.markdown("---")

st.sidebar.image(
    "[https://cdn-icons-png.flaticon.com/512/616/616408.png](https://cdn-icons-png.flaticon.com/512/616/616408.png)",
    width=150
)

st.sidebar.title("Menú")

modulo = st.sidebar.selectbox(
    "Seleccione la colección",
    [
        "🐶 Mascotas",
        "💉 Vacunas",
        "👨‍👩‍👧 Adoptantes"
    ]
)

if modulo == "🐶 Mascotas":

    st.title("🐾 Gestión de Mascotas🐾")

    tab1, tab2, tab3 = st.tabs([
        "Ver",
        "Agregar",
        "Eliminar"
    ])

    # ---------------- VER MASCOTAS ----------------
    with tab1:
        mascotas = list(coleccion_mascota.find())

        if mascotas:
            datos = []
            for m in mascotas:
                datos.append({
                    "ID": m.get("id_mascota"),
                    "Nombre": m.get("Nombre"),
                    "Nacimiento": m.get("F_de_nacimiento"),
                    "Especie": m.get("Especie"),
                    "Raza": m.get("Raza"),
                    "Tamaño": m.get("Tamaño"),
                    "Peso": m.get("Peso"),
                    "Genero": m.get("Genero"),
                    "Frecuencia": m.get("Frecuencia_Cardiaca")
                })

            st.dataframe(
                pd.DataFrame(datos),
                use_container_width=True
            )
            st.markdown("## 🐶 Mascotas Registradas")

            for mascota in mascotas:
                st.markdown(f"""
                <div class="card">
                <h3>🐾 {mascota.get('Nombre','')}</h3>
                <p>🧬 Raza: {mascota.get('Raza','')}</p>
                <p>🐶 Especie: {mascota.get('Especie','')}</p>
                <p>⚖️ Peso: {mascota.get('Peso','')} Kg</p>
                <p>❤️ FC: {mascota.get('Frecuencia_Cardiaca','')} ppm</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No hay mascotas registradas.")

    # ---------------- AGREGAR MASCOTAS ----------------
    with tab2:
        with st.form("agregar_mascota"):
            col1, col2 = st.columns(2)

            with col1:
                id_mascota = st.number_input("ID Mascota", min_value=1, step=1)
                nombre = st.text_input("Nombre")
                fecha = st.text_input("Fecha Nacimiento")
                especie = st.selectbox("Especie", ["Perro", "Gato", "Ave", "Conejo", "Otro"])
                raza = st.text_input("Raza")

            with col2:
                tamaño = st.selectbox("Tamaño", ["Pequeño", "Mediano", "Grande"])
                peso = st.number_input("Peso", min_value=0.0)
                genero = st.selectbox("Genero", ["Macho", "Femenino"])
                frecuencia = st.number_input("Frecuencia Cardiaca", min_value=0)

            guardar = st.form_submit_button("Guardar Mascota")

            if guardar:
                coleccion_mascota.insert_one({
                    "id_mascota": int(id_mascota),
                    "Nombre": nombre,
                    "F_de_nacimiento": fecha,
                    "Especie": especie,
                    "Raza": raza,
                    "Tamaño": tamaño,
                    "Peso": peso,
                    "Genero": genero,
                    "Frecuencia_Cardiaca": frecuencia
                })
                st.success("Mascota registrada")
                st.rerun()

    # ---------------- ELIMINAR MASCOTAS ----------------
    with tab3:
        mascotas = list(coleccion_mascota.find())

        if mascotas:
            opciones = {
                f"{m['Nombre']} (ID:{m['id_mascota']})": m
                for m in mascotas
            }

            seleccion = st.selectbox("Mascota", opciones.keys())
            mascota = opciones[seleccion]

            if st.button("Eliminar Mascota"):
                coleccion_mascota.delete_one({"_id": mascota["_id"]})
                st.success("Mascota eliminada")
                st.rerun()

# VACUNAS
elif modulo == "💉 Vacunas":

    st.title("💉 Gestión de Vacunas")

    tab1, tab2, tab3 = st.tabs([
        "Ver",
        "Agregar",
        "Eliminar"
    ])

    # ---------------- VER VACUNAS ----------------
    with tab1:
        vacunas = list(coleccion_vacuna.find())

        if vacunas:
            datos = []
            for v in vacunas:
                datos.append({
                    "ID": v.get("id_vacuna"),
                    "Nombre": v.get("Nombre"),
                    "Precio": v.get("Precio"),
                    "Tipo": v.get("Tipo"),
                    "Aplicación": v.get("Fecha_aplicacion"),
                    "Caducidad": v.get("Fecha_caducidad"),
                    "Contenido": v.get("Contenido"),
                    "Dosis": v.get("Dosis"),
                    "Estado": v.get("Estado")
                })

            st.dataframe(
                pd.DataFrame(datos),
                use_container_width=True
            )
        else:
            st.info("No hay vacunas registradas.")

    # ---------------- AGREGAR VACUNAS ----------------
    with tab2:
        with st.form("agregar_vacuna"):
            id_vacuna = st.number_input("ID Vacuna", min_value=1, step=1)
            nombre = st.text_input("Nombre")
            precio = st.number_input("Precio", min_value=0.0)
            tipo = st.text_input("Tipo")
            fecha_aplicacion = st.text_input("Fecha Aplicación")
            fecha_caducidad = st.text_input("Fecha Caducidad")
            contenido = st.text_input("Contenido")
            dosis = st.text_input("Dosis")
            estado = st.selectbox("Estado", ["Comprado", "Aplicado", "Caducado"])

            guardar = st.form_submit_button("Guardar Vacuna")

            if guardar:
                coleccion_vacuna.insert_one({
                    "id_vacuna": int(id_vacuna),
                    "Nombre": nombre,
                    "Precio": precio,
                    "Tipo": tipo,
                    "Fecha_aplicacion": fecha_aplicacion,
                    "Fecha_caducidad": fecha_caducidad,
                    "Contenido": contenido,
                    "Dosis": dosis,
                    "Estado": estado
                })
                st.success("Vacuna registrada")
                st.rerun()

    # ---------------- ELIMINAR VACUNAS ----------------
    with tab3:
        vacunas = list(coleccion_vacuna.find())

        if vacunas:
            opciones = {
                f"{v['Nombre']} (ID:{v['id_vacuna']})": v
                for v in vacunas
            }

            seleccion = st.selectbox("Vacuna", opciones.keys())
            vacuna = opciones[seleccion]

            if st.button("Eliminar Vacuna"):
                coleccion_vacuna.delete_one({"_id": vacuna["_id"]})
                st.success("Vacuna eliminada")
                st.rerun()

# ADOPTANTES
elif modulo == "👨‍👩‍👧 Adoptantes":

    st.title("👨‍👩‍👧 Gestión de Adoptantes")

    tab1, tab2, tab3 = st.tabs([
        "Ver",
        "Agregar",
        "Eliminar"
    ])

    # ---------------- VER ADOPTANTES ----------------
    with tab1:
        adoptantes = list(coleccion_adoptante.find())

        if adoptantes:
            datos = []
            for a in adoptantes:
                datos.append({
                    "ID": a.get("id_adoptante"),
                    "Nombre": a.get("Nombre"),
                    "Apellido": a.get("Apellido"),
                    "Edad": a.get("Edad"),
                    "INE": a.get("INE"),
                    "Domicilio": a.get("Domicilio"),
                    "Telefono": a.get("Telefono"),
                    "Correo": a.get("Gmail"),
                    "Vivienda": a.get("T_Vivienda")
                })

            st.dataframe(
                pd.DataFrame(datos),
                use_container_width=True
            )
        else:
            st.info("No existen adoptantes.")

    # ---------------- AGREGAR ADOPTANTES ----------------
    with tab2:
        with st.form("adoptante"):
            id_adoptante = st.number_input("ID Adoptante", min_value=1, step=1)
            nombre = st.text_input("Nombre")
            apellido = st.text_input("Apellido")
            edad = st.number_input("Edad", min_value=18)
            ine = st.text_input("INE")
            domicilio = st.text_input("Domicilio")
            telefono = st.text_input("Telefono")
            gmail = st.text_input("Correo")
            vivienda = st.selectbox("Tipo de Vivienda", ["Casa", "Departamento", "Rancho", "Otro"])

            guardar = st.form_submit_button("Guardar Adoptante")

            if guardar:
                coleccion_adoptante.insert_one({
                    "id_adoptante": int(id_adoptante),
                    "Nombre": nombre,
                    "Apellido": apellido,
                    "Edad": edad,
                    "INE": ine,
                    "Domicilio": domicilio,
                    "Telefono": telefono,
                    "Gmail": gmail,
                    "T_Vivienda": vivienda
                })
                st.success("Adoptante registrado")
                st.rerun()

    # ---------------- ELIMINAR ADOPTANTES ----------------
    with tab3:
        adoptantes = list(coleccion_adoptante.find())

        if adoptantes:
            opciones = {
                f"{a['Nombre']} {a['Apellido']}": a
                for a in adoptantes
            }

            seleccion = st.selectbox("Adoptante", opciones.keys())
            adoptante = opciones[seleccion]

            if st.button("Eliminar Adoptante"):
                coleccion_adoptante.delete_one({"_id": adoptante["_id"]})
                st.success("Adoptante eliminado")
                st.rerun()

```

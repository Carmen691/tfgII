import pandas as pd
import data.querys as qr


def cargar_tipo_entidades():
    tipos_entidad = pd.DataFrame(qr.obtener_tipos_entidad())
    return tipos_entidad.to_dict(orient="records"),
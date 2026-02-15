from fastapi import APIRouter
from controllers.reporte_controller import ReporteController
from models.reporte_informacion_model import ReporteInformacion

router = APIRouter()
nuevo_reporte = ReporteController()

@router.post("/create_reporte", response_model=ReporteInformacion)
async def create_reporte(reporte: ReporteInformacion):
    return nuevo_reporte.create(
        reporte.mascota_id,
        reporte.usuario_id,
        reporte.mensaje
    )

@router.get("/get_reporte/{reporte_id}", response_model=ReporteInformacion)
async def get_reporte(reporte_id: int):
    return nuevo_reporte.get_reporte(reporte_id)

@router.get("/get_reportes", response_model=list[ReporteInformacion])
async def get_reportes():
    return nuevo_reporte.get_reportes()

@router.put("/update_reporte/{reporte_id}")
async def update_reporte(reporte_id: int, reporte: ReporteInformacion):
    return nuevo_reporte.update_reporte(reporte_id, reporte.mensaje)

@router.delete("/delete_reporte/{reporte_id}")
async def delete_reporte(reporte_id: int):
    return nuevo_reporte.delete_reporte(reporte_id)

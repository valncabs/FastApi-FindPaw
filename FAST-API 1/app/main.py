from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from router.usuario_router import router as usuario_router
from router.rol_router import router as rol_router
from router.usuario_rol_router import router as usuario_rol_router
from router.mascota_perdida_router import router as mascota_router
from router.imagen_mascota_router import router as imagen_router
from router.modulo_router import router as modulo_router
from router.permiso_router import router as permiso_router
from router.reporte_informacion_router import router as reporte_router
from router.auth_router import router as auth_router


app = FastAPI()


@app.get("/")
def inicio():
    return {"mensaje": "La API está funcionando correctamente"}





app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(usuario_router)
app.include_router(auth_router)
app.include_router(rol_router)
app.include_router(usuario_rol_router)
app.include_router(mascota_router)
app.include_router(imagen_router)
app.include_router(modulo_router)
app.include_router(permiso_router)
app.include_router(reporte_router)

"""
AutoShield-AI - Sistema de Detecção de Fraudes em Imagens Automotivas
API Principal usando FastAPI
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
from datetime import datetime
from PIL import Image
import io

from detector.ai_detector import predict_ai
from detector.metadata import analyze_metadata
from detector.noise_analysis import analyze_noise
from utils.report import generate_report

app = FastAPI(
    title="AutoShield-AI",
    description="Sistema de detecção de fraudes em imagens automotivas usando IA",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("reports", exist_ok=True)

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/")
async def root():
    """Endpoint raiz - redireciona para interface web"""
    return FileResponse("frontend/index.html")

@app.get("/download-report/{filename}")
async def download_report(filename: str):
    """
    Endpoint para download do relatório PDF
    
    Args:
        filename: Nome do arquivo PDF
    
    Returns:
        Arquivo PDF para download
    """
    file_path = os.path.join("reports", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Relatório não encontrado")
    
    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename=filename,
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    """
    Analisa uma imagem para detectar possível fraude por IA
    
    Args:
        file: Arquivo de imagem (JPEG, PNG, etc.)
    
    Returns:
        JSON com análise completa:
        - status: "Suspeita de fraude" ou "Provavelmente real"
        - ai_probability: Probabilidade de ser gerada por IA (0-1)
        - noise_analysis: Análise de ruído da imagem
        - metadata_analysis: Análise de metadados EXIF
        - report_path: Caminho do relatório PDF gerado
    """
    
    try:

        contents = await file.read()

        try:
            image = Image.open(io.BytesIO(contents))
            image.verify()  
            image = Image.open(io.BytesIO(contents)) 
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Arquivo inválido: {str(e)}")

        print("Executando análise de IA...")
        ai_probability = predict_ai(image)

        print("Analisando metadados...")
        metadata_analysis = analyze_metadata(contents)

        print("Analisando padrões de ruído...")
        noise_analysis = analyze_noise(image)

        is_suspicious = (
            ai_probability > 0.6 or  
            (ai_probability > 0.4 and metadata_analysis["suspicious"]) or  
            (noise_analysis["suspicious"] and metadata_analysis["suspicious"])  
        )
        
        status = "Suspeita de fraude" if is_suspicious else "Provavelmente real"

        print("Gerando relatório PDF...")
        report_path = generate_report(
            filename=file.filename,
            ai_probability=ai_probability,
            noise_analysis=noise_analysis,
            metadata_analysis=metadata_analysis,
            status=status
        )

        response = {
            "status": status,
            "ai_probability": round(ai_probability, 4),
            "noise_analysis": noise_analysis,
            "metadata_analysis": metadata_analysis,
            "report_path": report_path,
            "timestamp": datetime.now().isoformat(),
            "filename": file.filename
        }
        
        print(f"Análise concluída: {status}")
        return JSONResponse(content=response)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na análise: {str(e)}")

@app.get("/health")
async def health_check():
    """Endpoint para verificar saúde da API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

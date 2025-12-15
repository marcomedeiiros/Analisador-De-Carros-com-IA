"""
Análise de Metadados EXIF
Extrai e analisa metadados de imagens para detectar manipulações
ou ausência de informações esperadas em fotos reais
"""

import exifread
import io
from datetime import datetime

def analyze_metadata(image_bytes: bytes) -> dict:
    """
    Analisa metadados EXIF de uma imagem
    
    Imagens geradas por IA geralmente não possuem metadados EXIF
    completos ou apresentam inconsistências reveladoras.
    
    Verifica:
    - Presença de dados EXIF
    - Modelo da câmera
    - Data/hora de captura
    - Software usado
    - Configurações de exposição
    
    Args:
        image_bytes: bytes da imagem
    
    Returns:
        dict com análise de metadados:
        - has_exif: bool
        - camera_model: str ou None
        - datetime: str ou None
        - software: str ou None
        - suspicious: bool (se metadados são suspeitos)
        - details: lista de observações
    """
    
    details = []
    
    try:

        tags = exifread.process_file(io.BytesIO(image_bytes), details=False)
        
        has_exif = len(tags) > 0

        camera_model = tags.get('Image Model', None)
        camera_model = str(camera_model) if camera_model else None
        
        datetime_original = tags.get('EXIF DateTimeOriginal', None)
        datetime_original = str(datetime_original) if datetime_original else None
        
        software = tags.get('Image Software', None)
        software = str(software) if software else None

        suspicious = False

        if not has_exif:
            suspicious = True
            details.append("Imagem não possui metadados EXIF (comum em imagens geradas por IA)")

        if software:
            ai_software_keywords = ['stable', 'midjourney', 'dall-e', 'dalle', 
                                   'diffusion', 'generator', 'synthesis']
            for keyword in ai_software_keywords:
                if keyword.lower() in software.lower():
                    suspicious = True
                    details.append(f"Software suspeito detectado: {software}")

        if has_exif and not camera_model:
            suspicious = True
            details.append("Metadados presentes mas sem modelo de câmera")

        if datetime_original:
            try:
                dt = datetime.strptime(datetime_original, '%Y:%m:%d %H:%M:%S')
                if dt > datetime.now():
                    suspicious = True
                    details.append("Data/hora no futuro - possível manipulação")
            except:
                pass
        
        if not suspicious and has_exif:
            details.append("Metadados consistentes com foto real")
        
        return {
            "has_exif": has_exif,
            "camera_model": camera_model,
            "datetime": datetime_original,
            "software": software,
            "suspicious": suspicious,
            "details": details
        }
    
    except Exception as e:

        return {
            "has_exif": False,
            "camera_model": None,
            "datetime": None,
            "software": None,
            "suspicious": True,
            "details": [f"Erro ao processar metadados: {str(e)}"]
        }

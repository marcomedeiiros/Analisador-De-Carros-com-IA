"""
Análise de Ruído Digital - Versão Pure Python
Examina padrões de ruído na imagem para detectar características
de imagens sintéticas geradas por IA
"""

from PIL import Image, ImageFilter, ImageStat
import statistics

def analyze_noise(image: Image.Image) -> dict:
    """
    Analisa padrões de ruído digital na imagem usando apenas Pillow
    
    Imagens geradas por IA tendem a ter:
    - Ruído excessivamente uniforme
    - Ausência de ruído de sensor natural
    - Padrões de ruído artificiais
    - Inconsistências entre regiões
    
    Args:
        image: Imagem PIL para análise
    
    Returns:
        dict com análise de ruído
    """

    gray = image.convert('L')

    denoised = gray.filter(ImageFilter.MedianFilter(size=5))

    width, height = gray.size
    gray_pixels = list(gray.getdata())
    denoised_pixels = list(denoised.getdata())

    noise_values = [abs(g - d) for g, d in zip(gray_pixels, denoised_pixels)]

    mean_noise = statistics.mean(noise_values)
    std_noise = statistics.stdev(noise_values) if len(noise_values) > 1 else 0

    regions = []
    half_w, half_h = width // 2, height // 2
    
    for y_offset in [0, half_h]:
        for x_offset in [0, half_w]:
            region = gray.crop((x_offset, y_offset, x_offset + half_w, y_offset + half_h))
            region_denoised = denoised.crop((x_offset, y_offset, x_offset + half_w, y_offset + half_h))
            
            region_pixels = list(region.getdata())
            region_denoised_pixels = list(region_denoised.getdata())
            region_noise = [abs(r - d) for r, d in zip(region_pixels, region_denoised_pixels)]
            regions.append(statistics.mean(region_noise))

    region_mean = statistics.mean(regions)
    region_std = statistics.stdev(regions) if len(regions) > 1 else 0
    uniformity = 1.0 - (region_std / (region_mean + 1e-10))

    edges = gray.filter(ImageFilter.FIND_EDGES)
    edge_stats = ImageStat.Stat(edges)
    jpeg_artifacts = edge_stats.var[0] if edge_stats.var else 0
    
    details = []
    suspicious = False

    if mean_noise < 3.0:
        suspicious = True
        details.append(f"Ruído extremamente baixo ({mean_noise:.2f}) - típico de imagens sintéticas")

    if uniformity > 0.95:
        suspicious = True
        details.append(f"Ruído excessivamente uniforme ({uniformity:.3f}) - padrão não natural")

    if std_noise < 5.0:
        suspicious = True
        details.append(f"Variação de ruído muito baixa ({std_noise:.2f})")

    entropy = gray.entropy()
    if entropy < 5.0:
        suspicious = True
        details.append(f"Entropia muito baixa ({entropy:.2f}) - falta de aleatoriedade natural")

    if jpeg_artifacts < 50:
        suspicious = True
        details.append("Ausência de artefatos típicos de compressão")
    
    if not suspicious:
        details.append("Padrões de ruído consistentes com foto real")
    
    return {
        "mean_noise": round(mean_noise, 4),
        "std_noise": round(std_noise, 4),
        "uniformity": round(uniformity, 4),
        "jpeg_artifacts_variance": round(jpeg_artifacts, 4),
        "entropy": round(entropy, 4),
        "suspicious": suspicious,
        "details": details
    }

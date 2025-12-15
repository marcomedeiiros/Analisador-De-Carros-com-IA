"""
Detector de Imagens Geradas por IA - Versão Simplificada
Utiliza análise heurística sem dependências pesadas
"""

from PIL import Image, ImageStat, ImageFilter
import statistics

_analysis_cache = {}

def analyze_color_distribution(image: Image.Image) -> dict:
    """
    Analisa distribuição de cores para detectar padrões artificiais
    
    Args:
        image: Imagem PIL
        
    Returns:
        dict com métricas de cor
    """

    if image.mode != 'RGB':
        image = image.convert('RGB')

    stats = ImageStat.Stat(image)

    means = stats.mean
    stddevs = stats.stddev

    mean_uniformity = statistics.stdev(means) / (statistics.mean(means) + 1e-10)
    std_uniformity = statistics.stdev(stddevs) / (statistics.mean(stddevs) + 1e-10)
    
    return {
        "mean_uniformity": mean_uniformity,
        "std_uniformity": std_uniformity,
        "channel_means": means,
        "channel_stddevs": stddevs
    }

def analyze_texture_patterns(image: Image.Image) -> dict:
    """
    Analisa padrões de textura para detectar características de IA
    
    Args:
        image: Imagem PIL
        
    Returns:
        dict com métricas de textura
    """

    gray = image.convert('L')

    edges = gray.filter(ImageFilter.FIND_EDGES)
    edge_stats = ImageStat.Stat(edges)
    

    details = gray.filter(ImageFilter.DETAIL)
    detail_stats = ImageStat.Stat(details)

    sharpness = gray.filter(ImageFilter.SHARPEN)
    sharp_stats = ImageStat.Stat(sharpness)
    
    return {
        "edge_mean": edge_stats.mean[0],
        "detail_mean": detail_stats.mean[0],
        "sharpness_mean": sharp_stats.mean[0],
        "edge_stddev": edge_stats.stddev[0]
    }

def analyze_spatial_consistency(image: Image.Image) -> dict:
    """
    Analisa consistência espacial da imagem
    
    Args:
        image: Imagem PIL
        
    Returns:
        dict com métricas de consistência
    """

    width, height = image.size
    half_w, half_h = width // 2, height // 2
    
    regions = [
        image.crop((0, 0, half_w, half_h)),
        image.crop((half_w, 0, width, half_h)),
        image.crop((0, half_h, half_w, height)),
        image.crop((half_w, half_h, width, height))
    ]

    region_means = []
    region_stds = []
    
    for region in regions:
        stats = ImageStat.Stat(region.convert('L'))
        region_means.append(stats.mean[0])
        region_stds.append(stats.stddev[0])

    mean_variation = statistics.stdev(region_means) if len(region_means) > 1 else 0
    std_variation = statistics.stdev(region_stds) if len(region_stds) > 1 else 0
    
    return {
        "mean_variation": mean_variation,
        "std_variation": std_variation,
        "consistency_score": 1.0 - (mean_variation / (statistics.mean(region_means) + 1e-10))
    }

def predict_ai(image: Image.Image) -> float:
    """
    Prediz a probabilidade de uma imagem ser gerada por IA
    usando análise heurística
    
    Analisa características como:
    - Padrões de textura irreais
    - Inconsistências em detalhes
    - Distribuição de cores não naturais
    - Uniformidade excessiva
    
    Args:
        image: Imagem PIL para análise
    
    Returns:
        float: Probabilidade de ser IA (0.0 = real, 1.0 = IA)
    """
    
    print("[AI Detector] Executando análise heurística...")

    max_size = 512
    if image.width > max_size or image.height > max_size:
        image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

    color_analysis = analyze_color_distribution(image)

    texture_analysis = analyze_texture_patterns(image)

    spatial_analysis = analyze_spatial_consistency(image)

    suspicion_score = 0.0

    if color_analysis["mean_uniformity"] < 0.15:
        suspicion_score += 0.25

    if spatial_analysis["consistency_score"] > 0.95:
        suspicion_score += 0.20

    if texture_analysis["sharpness_mean"] > 140:
        suspicion_score += 0.20

    if texture_analysis["edge_stddev"] < 10:
        suspicion_score += 0.15

    if texture_analysis["detail_mean"] < 100:
        suspicion_score += 0.20

    probability = min(1.0, suspicion_score)

    gray = image.convert('L')
    entropy = gray.entropy()

    if entropy < 6.0:
        probability = min(1.0, probability + 0.15)
    elif entropy > 7.8:
        probability = min(1.0, probability + 0.10)
    
    print(f"[AI Detector] Probabilidade calculada: {probability:.4f}")
    
    return probability

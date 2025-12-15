"""
Script para iniciar o servidor AutoShield-AI
"""

import sys
import os

backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("Sistema de Detecção de Fraudes")
    print("=" * 60)
    print("\n🚀 Iniciando servidor API...")
    print("📍 URL: http://localhost:8000")
    print("📚 Documentação: http://localhost:8000/docs")
    print("\n💡 Pressione Ctrl+C para parar o servidor\n")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

"""
Script de instalação de dependências
Instala pacotes um por um para evitar falhas
"""

import subprocess
import sys

packages = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",
    "python-multipart>=0.0.9",
    "pillow>=10.4.0",
    "opencv-python>=4.10.0",
    "torch",
    "torchvision", 
    "numpy",
    "exifread>=3.0.0",
    "reportlab>=4.2.0",
]

def install_package(package):
    """Instala um pacote individualmente"""
    print(f"\n{'='*60}")
    print(f"Instalando: {package}")
    print('='*60)
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} instalado com sucesso!")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Erro ao instalar {package}")
        return False

def main():
    """Instala todas as dependências"""
    print("\n" + "="*60)
    print("🛡️  AutoShield-AI - Instalador de Dependências")
    print("="*60)
    
    failed = []
    
    for package in packages:
        if not install_package(package):
            failed.append(package)
    
    print("\n" + "="*60)
    print("Resumo da Instalação")
    print("="*60)
    
    if not failed:
        print("✅ Todas as dependências foram instaladas com sucesso!")
        print("\nPara iniciar o servidor, execute:")
        print("  python scripts/run_api.py")
    else:
        print(f"❌ {len(failed)} pacote(s) falharam:")
        for pkg in failed:
            print(f"  - {pkg}")
        print("\nTente instalar manualmente os pacotes que falharam.")

if __name__ == "__main__":
    main()

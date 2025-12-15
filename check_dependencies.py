"""
Verifica quais dependências estão instaladas
"""

def check_import(module_name, package_name=None):
    """Verifica se um módulo pode ser importado"""
    if package_name is None:
        package_name = module_name
    
    try:
        __import__(module_name)
        print(f"✅ {package_name} - OK")
        return True
    except ImportError:
        print(f"❌ {package_name} - FALTANDO")
        print(f"   Instale com: pip install {package_name}")
        return False

def main():
    """Verifica todas as dependências"""
    print("\n" + "="*60)
    print("🔍 Verificando Dependências do AutoShield-AI")
    print("="*60 + "\n")
    
    dependencies = [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("PIL", "pillow"),
        ("cv2", "opencv-python"),
        ("torch", "torch"),
        ("torchvision", "torchvision"),
        ("numpy", "numpy"),
        ("exifread", "exifread"),
        ("reportlab", "reportlab"),
    ]
    
    missing = []
    
    for module, package in dependencies:
        if not check_import(module, package):
            missing.append(package)
    
    print("\n" + "="*60)
    if not missing:
        print("✅ TODAS as dependências estão instaladas!")
        print("\nVocê pode iniciar o servidor:")
        print("  python scripts/run_api.py")
    else:
        print(f"❌ {len(missing)} dependência(s) faltando")
        print("\nPara instalar as dependências faltantes:")
        for pkg in missing:
            print(f"  pip install {pkg}")
        print("\nOu execute:")
        print("  python install_dependencies.py")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()

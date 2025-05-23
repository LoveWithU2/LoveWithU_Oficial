from invoke import task
import os
import shutil
from datetime import datetime, timedelta
import zipfile


@task
def empacotador(c):
    """Cria um backup simples dos diretórios e arquivos do projeto."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    zip_name = f'backup_flask_{timestamp}.zip'
    incluir = ['app', 'src', 'template', 'tasks.py']

    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for item in incluir:
            if os.path.exists(item):
                if os.path.isdir(item):
                    for root, _, files in os.walk(item):
                        for f in files:
                            path = os.path.join(root, f)
                            zipf.write(path, arcname=os.path.relpath(path))
                else:
                    zipf.write(item)
    print(f"Backup criado: {zip_name}")


@task
def backup(c, source='.', destination='backup', dias_max=7):
    """Cria backup zipado do projeto e armazena em um diretório destino."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    temp_backup_dir = os.path.join(destination, f'temp_{timestamp}')
    zip_filename = os.path.join(destination, f'backup_temp_{timestamp}.zip')

    os.makedirs(temp_backup_dir, exist_ok=True)
    incluir = ['app', 'template', 'src', 'tasks.py']

    for item in incluir:
        if os.path.exists(item):
            destino_item = os.path.join(temp_backup_dir, item)
            try:
                if os.path.isdir(item):
                    shutil.copytree(item, destino_item)
                else:
                    shutil.copy2(item, destino_item)
                print(f'Copiado: {item}')
            except Exception as e:
                print(f'Erro ao copiar {item}: {e}')

    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_backup_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, arcname=os.path.relpath(file_path, temp_backup_dir))

    print(f'\nBackup criado em: {zip_filename}')


@task
def descompactar(c, last=True, source='.', destination='backup'):

    # Garante que o diretório de destino exista
    if not os.path.exists(destination):
        os.makedirs(destination)

    # Lista arquivos .zip no diretório source
    arquivos_zip = [
        f for f in os.listdir(source)
        if f.endswith('.zip') and os.path.isfile(os.path.join(source, f))
    ]

    if not arquivos_zip:
        print("Nenhum arquivo .zip encontrado.")
        return

    # Seleciona o mais recente, se last=True
    if last:
        arquivos_zip.sort(
            key=lambda f: os.path.getmtime(os.path.join(source, f)),
            reverse=True
        )
    
    zip_path = os.path.join(source, arquivos_zip[0])
    print(f"Descompactando arquivo: {zip_path}")

    with zipfile.ZipFile(zip_path, 'r') as zipf:
        zipf.extractall(destination)

    print(f"Arquivos extraídos com sucesso para o diretório: {destination}")
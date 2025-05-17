if ( -Not (Test-Path "venv")) {
    py -m venv venv
}
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

. .\venv\Scripts\Activate.ps1
py -m pip install --upgrade pip

New-Item -ItemType Directory -Path "static\uploads" -Force

pip install -e .
pip install invoke

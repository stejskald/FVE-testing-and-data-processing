# -*- mode: python ; coding: utf-8 -*-

add_paths = [
    'C:/Data/Projekty/GitHub/FVE-testing-and-data-processing/dp_app/data',
    'C:/Data/Projekty/GitHub/FVE-testing-and-data-processing/dp_app/icons',
    'C:/Data/Projekty/GitHub/FVE-testing-and-data-processing/dp_app/include/UIs',
    'C:/Data/Projekty/GitHub/FVE-testing-and-data-processing/dp_app/include/AbstractDataModels'
]

add_data = [
    ( 'dp_app/icons', 'icons' ),
    ( 'dp_app/include/AbstractDataModels', 'AbstractDataModels' ),
    ( 'dp_app/include/UIs/*.py', 'UIs' ),
    ( 'dp_app/appConfig.ini', '.' )
]

add_hidden_imports = [
    'resource', 'platformdirs', 'pyqtgraph.opengl'
]

a = Analysis(
    ['dp_app/app-main.py'],
    pathex=add_paths,
    binaries=[],
    datas=add_data,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Analysing FVE test data',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='dp_app/icons/solar-panel.ico'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='app-main',
)

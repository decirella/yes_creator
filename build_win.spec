# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['yes_creator.py'],  
    pathex=['./yes_creator.py'],  
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['_bootlocale'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False)

pyz = PYZ(a.pure)

options = [('u', None, 'OPTION'), ('v', None, 'OPTION'), ('w', None, 'OPTION')]

exe = EXE(pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,  
    [],
    name='YES Creator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None )

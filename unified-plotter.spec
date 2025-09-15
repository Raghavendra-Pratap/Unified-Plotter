# -*- mode: python ; coding: utf-8 -*-

import os

block_cipher = None

a = Analysis(
    ['unified-plotter.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('version.py', '.'),
        ('auto_updater.py', '.'),
        ('README.md', '.'),
        ('CHANGELOG.md', '.'),
        ('LICENSE', '.'),
        ('plotter_white.png', '.'),
    ],
    hiddenimports=[
        'matplotlib.backends._tkagg',
        'matplotlib.backends.backend_tkagg',
        'PIL._tkinter_finder',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.simpledialog',
        'tkinter.colorchooser',
        'tkinter.font',
        'tkinter.scrolledtext',
        'pandas',
        'numpy',
        'matplotlib',
        'matplotlib.backends',
        'matplotlib.backends.backend_tkagg',
        'matplotlib.figure',
        'matplotlib.pyplot',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'requests',
        'auto_updater',
        'version',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='unified-plotter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='plotter_white.png' if os.path.exists('plotter_white.png') else None,
)

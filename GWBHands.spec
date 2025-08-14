# -*- mode: python ; coding: utf-8 -*-
import mediapipe as mp
import os
from PyInstaller.utils.hooks import collect_submodules

# Collect all mediapipe and cv2 submodules to prevent ModuleNotFoundError
extra_mediapipe = collect_submodules('mediapipe')
extra_cv2 = collect_submodules('cv2')
mp_path = os.path.dirname(mp.__file__)
block_cipher = None

a = Analysis(
    ['gui\\GWBHands.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('gui', 'gui'),
        ('gui/model', 'model'),
        (os.path.join(mp_path, 'modules'), 'mediapipe/modules')
    ],
    hiddenimports=[
        'keyboard',
        'pyautogui',
        'mediapipe',
        'nbformat',
        'nbconvert',
    ] + extra_mediapipe + extra_cv2,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GWBHands',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None
)

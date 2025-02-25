# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['farconfig.py'],
    pathex=[],
    binaries=[],
    datas=[('resources', 'resources')],
    hiddenimports=['pyserial'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PyQt5', 'PyQt6', 'PyInstaller'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
#    [],
#    exclude_binaries=True,
    name='Ekdahl FAR Configuration utility',
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
)
#coll = COLLECT(
#    exe,
#    a.binaries,
#    a.datas,
#    strip=False,
#    upx=True,
#    upx_exclude=[],
#    name='Ekdahl FAR Configuration utility',
#)
app = BUNDLE(#coll,
         exe,
         name='Ekdahl FAR Configuration utility.app',
         icon='_internal/resources/far_icon.icns',
         bundle_identifier=None)

# -*- mode: python ; coding: utf-8 -*-

import os
project_dir = os.path.abspath(os.path.dirname(SPEC))

import PySide6
import os
pysidedir = os.path.dirname(PySide6.__file__)

a = Analysis(
    ['farconfig.py'],
    pathex=[project_dir, project_dir + "/GraphNode"],
    binaries=[],
    
    #'../.venv/lib/python3.12/site-packages/PySide6/Qt', 'PySide6/Qt'
    
    datas=[('resources', 'resources'),(pysidedir, 'PySide6'), (project_dir + "/GraphNode/hotkeys", "GraphNode/hotkeys"), 
		(project_dir + "/GraphNode/nodetemplates", "GraphNode/nodetemplates")],
    hiddenimports=[
        'pyserial',
        'equationParsingHelpers',
        'nodehandler',
        'pluginhandler',
        'CommandSets',
        'stringModule',
        'timedChart',
        'commandReference',
        'serialWidget',
        'cveventhandling',
        'midieventhandling',
        'ui_form',
        'general_helpers',
        'commandparser',
        'commanddefinitions',
        'tableTest',
        'waitdialog',
        'dynamicnodes',
        'midihandler',
        'averager',
        'form',
        'ui_plugin_ahdsr',
        'ui_plugin_lfo',
        'ui_plugin_mult',
        'ui_plugin_numbermap',
        'ui_prompt',
        'ui_reference',
        'Qt',
        'PySide6.QtSvg',
        'PySide6.QtSvgWidgets',
        'customgroupnode',
        'customnode',
        'customnodewidgets',
        'graphassemblies',
        'nodeblocks',
        'nodeorganizer'
    ],
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

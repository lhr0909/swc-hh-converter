# -*- mode: python -*-
a = Analysis(['GUI.py'],
             pathex=['C:\\Users\\Simon\\Documents\\GitHub\\swc-hh-converter'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='SealsHEM2HUD.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False )

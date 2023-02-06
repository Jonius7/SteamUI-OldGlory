# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['old_glory.py'],
             binaries=[],
             datas=[('steam_oldglory.ico', '.')],
             hiddenimports=['six'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['lzma', 'bz2', 'tcl', 'pygments', 'matplotlib', 'IPython', 'ipython_genutils', 'ipykernel', 'jupyter_client', 'asyncio', 'hook', 'distutils', 'hooks', 'tornado', 'sqlite3', 'PyInstaller', 'jedi', 'test', 'site', 'pycparser'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)	 
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='old_glory_32',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
		  icon='steam_oldglory.ico')

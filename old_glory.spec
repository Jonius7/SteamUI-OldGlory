# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['old_glory.py'],
             pathex=['D:\\New Horizons\\Hearthstone\\SteamUI-OldGlory'],
             binaries=[],
             datas=[('*.png', '.'), ('steam_oldglory.ico', '.')],
             hiddenimports=['six'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
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
          name='old_glory',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
		  icon='steam_oldglory.ico')
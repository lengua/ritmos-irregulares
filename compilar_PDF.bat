@echo off
powershell -Command "python .\join_md_files.py"
powershell -Command "python .\clean_md4PDF.py .\_FULL_DUMMY.md"
@REM powershell -Command "pandoc _FULL_DUMMY_filtrado.md -o _FULL_DUMMY.pdf --include-in-header=music-header.tex  --metadata-file=meta.yaml --pdf-engine=lualatex -V classoption=twoside --template=custom-template.tex"
@REM powershell -Command "start firefox 'file:///C:/Users/lalen/Desktop/RITMOS%%20IRREGULARES/TEXTOS/_FINALES/_FULL_DUMMY.pdf#page=2'"
powershell -Command "pandoc _FULL_DUMMY_filtrado.md -o Ritmos_irregulares-Judith_de_Leon-Santiago_Chavez_Novaro-v0.8.pdf --include-in-header=music-header.tex --metadata-file=meta.yaml --toc --pdf-engine=lualatex -V classoption=twoside -V fontsize=12pt --template=custom-template.tex"
powershell -Command "start firefox 'file:///C:/Users/lalen/Desktop/RITMOS%%20IRREGULARES/TEXTOS/_FINALES/Ritmos_irregulares-Judith_de_Leon-Santiago_Chavez_Novaro-v0.8.pdf#page=82'"
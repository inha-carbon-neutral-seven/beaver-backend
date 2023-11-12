@echo offfor 
for /f "tokens=1" %%a in ('docker ps ^| findstr biber') do set image_name=%%a
echo %image_name%


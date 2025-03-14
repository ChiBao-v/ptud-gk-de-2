@echo off
echo Đang thiết lập môi trường ảo...
python -m venv venv

echo Kích hoạt môi trường ảo...
call venv\Scripts\activate

echo Cài đặt các thư viện cần thiết...
pip install --upgrade pip
pip install -r requirements.txt

echo Chạy ứng dụng Flask...
set FLASK_APP=app.py
set FLASK_ENV=production
flask run

pause
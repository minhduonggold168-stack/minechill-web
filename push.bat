@echo off
echo [*] Dang day ma nguon len GitHub repository...
echo [*] Neu co hop thoai trinh duyet hien ra, vui long xac nhan dang nhap GitHub.
git push -u origin main
if %errorlevel% neq 0 (
    echo [!] Neu gap loi xac thuc, ban co the su dung GitHub Personal Access Token.
) else (
    echo [OK] Day code len GitHub thanh cong!
)
pause

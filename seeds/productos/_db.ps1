$G = 'C:\Users\isaac\Desktop\sofosy\germiva'
$env_ = Get-Content "$G\Germiva-api\.env"
$env:MYSQL_PWD = (($env_ | Select-String '^DB_PASSWORD=').Line -replace '^DB_PASSWORD=','').Trim('"')
$MYSQL = "C:/Program Files/MySQL/MySQL Server 9.7/bin/mysql.exe"
$DUMP = "C:/Program Files/MySQL/MySQL Server 9.7/bin/mysqldump.exe"
$CANON = "C:\Users\isaac\Desktop\sofosy\claude-tutorial\seeds\productos\canon-productos.sql"
function Sql($q) { & $MYSQL -uroot germiva --default-character-set=utf8mb4 -e $q 2>&1 | Where-Object { $_ -notmatch 'Using a password' } }

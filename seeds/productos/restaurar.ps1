# Devuelve la base al canon del tutorial de Productos (carga completa, sin binlog: R14).
. "$PSScriptRoot\_db.ps1"
$t0 = Get-Date
cmd /c "`"$MYSQL`" -uroot --default-character-set=utf8mb4 --init-command=`"SET SESSION sql_log_bin=0`" germiva < `"$CANON`"" 2>&1 | Where-Object { $_ -notmatch 'Using a password' }
if ($LASTEXITCODE) { throw "restauración falló ($LASTEXITCODE)" }
"restaurado en {0:N0} s" -f ((Get-Date)-$t0).TotalSeconds

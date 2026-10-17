. "$PSScriptRoot\_db.ps1"
& $DUMP -uroot --single-transaction --routines --triggers --events --hex-blob --set-gtid-purged=OFF --default-character-set=utf8mb4 --result-file="$CANON" germiva 2>&1 | Where-Object { $_ -notmatch 'Using a password' }
"canon: {0:N1} MB" -f ((Get-Item $CANON).Length/1MB)

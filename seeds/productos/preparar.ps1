# Estado de partida del tutorial de Productos sobre la empresa 1 («Tienda Germiva») y canon.
. "$PSScriptRoot\_db.ps1"
cmd /c "`"$MYSQL`" -uroot --default-character-set=utf8mb4 germiva < `"$PSScriptRoot\preparar.sql`"" 2>&1
$tok = (Invoke-RestMethod -Method Post -Uri http://localhost:3001/api/auth/dev/login -ContentType 'application/json' -Body '{"username":"admin","password":"admin"}').accessToken
$h = @{ Authorization = "Bearer $tok" }
function Api($p, $b) { try { $r = Invoke-RestMethod -Method Post -Uri "http://localhost:3001/api$p" -Headers $h -ContentType 'application/json; charset=utf-8' -Body ([Text.Encoding]::UTF8.GetBytes($b)); "OK $p id=$($r.id)" } catch { "ERROR $p : $($_.Exception.Message) $($_.ErrorDetails.Message)" } }
Api '/v1/inventory/location' '{"position":"Pasillo A - Estante 1","warehouse":1}'
Api '/v1/partner' '{"name":"Textiles Germiva del Caribe","tin":"130555002","partnerType":["SUPPLIER"],"partnerCategory":"BUSINESS"}'

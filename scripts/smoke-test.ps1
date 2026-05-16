param(
    [string]$ApiBase = "https://in-31b9193aea6e431e9cdfc54cbf0e44ff.ecs.us-east-2.on.aws"
)

$ErrorActionPreference = "Stop"

Write-Host "Running backend smoke test..."
Write-Host "API base: $ApiBase"

Write-Host "Testing /health..."
$health = Invoke-RestMethod "$ApiBase/health"
Write-Host "Health response:" ($health | ConvertTo-Json -Compress)

Write-Host "Testing /api/items..."
$items = Invoke-RestMethod "$ApiBase/api/items"
$itemCount = @($items).Count
Write-Host "Items returned: $itemCount"

if ($itemCount -eq 0) {
    Write-Warning "API is reachable, but /api/items returned 0 items. Database may be empty or not seeded."
}

Write-Host "Smoke test passed."
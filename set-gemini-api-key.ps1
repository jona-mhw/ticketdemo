param(
    [Parameter(Mandatory=$true)]
    [string]$ApiKey
)

# Establecer la variable de entorno para la sesión actual
$env:GEMINI_API_KEY = $ApiKey

# Establecer la variable de entorno permanentemente para el usuario actual
[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", $ApiKey, "User")

Write-Host "✓ Variable GEMINI_API_KEY establecida correctamente" -ForegroundColor Green
Write-Host "  - Sesión actual: $env:GEMINI_API_KEY" -ForegroundColor Cyan
Write-Host "  - Variable permanente establecida para el usuario" -ForegroundColor Cyan

# Verificar que se haya establecido correctamente
$storedValue = [Environment]::GetEnvironmentVariable("GEMINI_API_KEY", "User")
if ($storedValue -eq $ApiKey) {
    Write-Host "✓ Verificación exitosa: Variable almacenada correctamente" -ForegroundColor Green
} else {
    Write-Host "✗ Error: No se pudo verificar la variable almacenada" -ForegroundColor Red
}

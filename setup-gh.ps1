<#
.SYNOPSIS
    Einmalig ausführen, um GitHub CLI (gh) zu installieren (falls fehlt) und dich anzumelden.

.DESCRIPTION
    - Prüft, ob `gh` bereits verfügbar ist
    - Installiert bei Bedarf über winget (offizielle empfohlene Methode für Windows)
    - Startet `gh auth login` (interaktiv: Browser oder Personal Access Token)
    - Zeigt Status + passende git-Befehle für dieses Projekt
    - Hilft bei der Korrektur des Remotes (h4sch vs. aktuell angelegter Owner)
#>

$ErrorActionPreference = 'Stop'

$projectDir = $PSScriptRoot

Write-Host "=== GitHub CLI (gh) Setup für qwen-image-edit-rapid-aio-v23 ===" -ForegroundColor Cyan
Write-Host "Verzeichnis: $projectDir" -ForegroundColor Gray
Write-Host ""

# 1. gh CLI erkennen
$ghCmd = Get-Command gh -ErrorAction SilentlyContinue

if (-not $ghCmd) {
    Write-Host "gh CLI nicht gefunden." -ForegroundColor Yellow
    Write-Host "Installiere jetzt über winget (empfohlen)..." -ForegroundColor White

    try {
        winget install --id GitHub.cli --source winget --accept-package-agreements --accept-source-agreements
        Write-Host "✅ winget Installation abgeschlossen." -ForegroundColor Green
    }
    catch {
        Write-Host "⚠️  Automatische winget-Installation fehlgeschlagen." -ForegroundColor Red
        Write-Host "Bitte manuell ausführen:" -ForegroundColor Yellow
        Write-Host '   winget install --id GitHub.cli --source winget' -ForegroundColor White
        Write-Host "Oder lade von https://github.com/cli/cli/releases/latest herunter." -ForegroundColor Gray
        Write-Host ""
        Write-Host "Nach der Installation ein NEUES PowerShell-Fenster öffnen und das Skript erneut starten." -ForegroundColor Cyan
        exit 1
    }

    # PATH im aktuellen Prozess aktualisieren
    $machinePath = [Environment]::GetEnvironmentVariable('Path', 'Machine')
    $userPath    = [Environment]::GetEnvironmentVariable('Path', 'User')
    $env:Path    = "$machinePath;$userPath"

    # Erneut prüfen
    $ghCmd = Get-Command gh -ErrorAction SilentlyContinue
    if (-not $ghCmd) {
        Write-Host "gh immer noch nicht im PATH. Bitte neues Terminal öffnen." -ForegroundColor Red
        exit 1
    }
}
else {
    Write-Host "✅ gh CLI bereits installiert: $($ghCmd.Source)" -ForegroundColor Green
}

# 2. Authentifizierung
Write-Host ""
Write-Host "Starte GitHub Authentifizierung..." -ForegroundColor Cyan
Write-Host "Es öffnet sich ein Browser-Fenster oder du wirst nach einem Token gefragt." -ForegroundColor Yellow
Write-Host "Empfehlung: Browser-Flow (https) wählen." -ForegroundColor Gray

& gh auth login

# 3. Status prüfen
Write-Host ""
Write-Host "=== gh auth status ===" -ForegroundColor Cyan
& gh auth status

# 4. Projekt-spezifische Git-Informationen
Write-Host ""
Write-Host "=== Aktueller Git-Status (dieses Projekt) ===" -ForegroundColor Cyan

git remote -v
$gitUser  = git config user.name
$gitEmail = git config user.email
Write-Host "Git user: $gitUser <$gitEmail>"

# 5. Praktische Push-Befehle
Write-Host ""
Write-Host "=== Nächste Schritte ===" -ForegroundColor Green
Write-Host "Falls du noch nichts gepusht hast:" -ForegroundColor White
Write-Host "   git push -u origin main" -ForegroundColor White
Write-Host ""
Write-Host "Hinweis zum aktuellen Remote:" -ForegroundColor Yellow
Write-Host "   Der Remote zeigt derzeit wahrscheinlich auf LucyFairies (wurde über MCP angelegt)." -ForegroundColor Gray
Write-Host ""
Write-Host "Falls du stattdessen unter deinem h4sch-Account arbeiten möchtest:" -ForegroundColor Yellow
Write-Host '   git remote set-url origin https://github.com/h4sch/qwen-image-edit-rapid-aio-v23.git' -ForegroundColor White
Write-Host '   git push -u origin main' -ForegroundColor White
Write-Host ""
Write-Host "Tipp: Das MCP-Tool (grok_com_github) bleibt weiterhin für AI-gestützte Aktionen (Issues, Datei-Updates, etc.) verfügbar." -ForegroundColor Gray
Write-Host ""
Write-Host "Fertig! Öffne bei Bedarf ein neues Terminal und teste:" -ForegroundColor Cyan
Write-Host "   gh --version" -ForegroundColor White
Write-Host "   gh repo view" -ForegroundColor White

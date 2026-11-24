# Creation du dossier de rapports
New-Item -ItemType Directory -Force reports | Out-Null

# Generation de l'horodatage
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"

# Definition du nom du rapport
$reportPath = "reports/bdd_report_$timestamp.txt"

# Execution des tests BDD et generation du rapport
python -m behave --format plain --no-color 2>&1 |
    Tee-Object -FilePath $reportPath

# Conservation du code de retour des tests
$exitCode = $LASTEXITCODE

# Affichage du chemin du rapport
Write-Host "`nRapport disponible : $reportPath"

# Transmission du statut de l'execution
exit $exitCode

#===============================================================
#commande dans terminal : 
#.\run_bdd.ps1
#===============================================================
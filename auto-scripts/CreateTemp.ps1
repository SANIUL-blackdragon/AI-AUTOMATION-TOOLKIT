# Get the directory where this script is located
$currentDir = $PSScriptRoot

# If running line-by-line in a console (where PSScriptRoot is empty), 
# it defaults to the current working directory.
if (-not $currentDir) { $currentDir = Get-Location }

$baseFolder = Join-Path -Path $currentDir -ChildPath "temp"

# 1. Create the 'temp' folder and the 'agent_playground' subfolder
# This matches the '└───agent_playground' in your tree
New-Item -Path "$baseFolder\agent_playground" -ItemType Directory -Force

# 2. Define the exact files from your updated list
$files = @(
    "CRITIQUE.MD",
    "INPUT.MD",
    "OUTPUT.MD",
    "scratchpad.md",
    "todo"
)

# 3. Create the files inside the \temp folder
foreach ($file in $files) {
    $filePath = Join-Path -Path $baseFolder -ChildPath $file
    New-Item -Path $filePath -ItemType File -Force
}

Write-Host "Structure created successfully in: $baseFolder" -ForegroundColor Green

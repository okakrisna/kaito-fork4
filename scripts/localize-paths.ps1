param(
    [string]$FilePath = "",
    [string]$RootDir = "c:\Users\okakr\Downloads\new 2\groovepublic.com\groovepublic.com"
)

function Update-FilePaths {
    param([string]$TargetFile)

    if (-not (Test-Path -Path $TargetFile)) { return }
    $ext = [System.IO.Path]::GetExtension($TargetFile).ToLower()
    $textExts = @('.html','.htm','.css','.js','.json','.svg','.xml','.txt','.map','.md','.php')
    if ($textExts -notcontains $ext) { return }

    $backupPath = "$TargetFile.bak"
    Copy-Item -Path $TargetFile -Destination $backupPath -Force

    $content = Get-Content -Raw -Path $TargetFile
    $content = $content -replace "https?://groovepublic\.com/wp-content/", "./wp-content/"
    $content = $content -replace "https?://groovepublic\.com/wp-includes/", "./wp-includes/"
    $content = $content -replace "//groovepublic\.com/wp-content/", "./wp-content/"
    $content = $content -replace "//groovepublic\.com/wp-includes/", "./wp-includes/"
    # Escaped variants in JS strings (https:\/\/groovepublic.com\/wp-...)
    $content = $content -replace "https:\\/\\/groovepublic\.com\\/wp-content/", "./wp-content/"
    $content = $content -replace "https:\\/\\/groovepublic\.com\\/wp-includes/", "./wp-includes/"

    Set-Content -Path $TargetFile -Value $content -Encoding UTF8
    Write-Output "Updated: $TargetFile"
}

if ($FilePath -and $FilePath.Trim().Length -gt 0) {
    Update-FilePaths -TargetFile $FilePath
    Write-Output "Done single file: $FilePath"
} else {
    if (-not (Test-Path -Path $RootDir)) {
        Write-Error "Root directory not found: $RootDir"; exit 1
    }
    Get-ChildItem -Path $RootDir -Recurse -File | ForEach-Object {
        try { Update-FilePaths -TargetFile $_.FullName } catch { Write-Warning "Skip: $($_.FullName) - $($_.Exception.Message)" }
    }
    Write-Output "Completed updating local paths under: $RootDir"
}
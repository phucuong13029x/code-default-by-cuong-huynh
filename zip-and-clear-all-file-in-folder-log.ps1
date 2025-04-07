$drive = "C:\"
Write-Host "[+] Folder source: $($drive)"
$logFolders = Get-ChildItem -Path $drive -Recurse -Directory -Filter "Log"
Write-Host "[+] Folder filter: $($logFolders)"
$thresholdDate = (Get-Date).AddDays(-7)

foreach ($logFolder in $logFolders) {
    Write-Host "[-] Folder in process: $($folder.FullName)"
    # Lấy toàn bộ file trong cây thư mục Log (bao gồm thư mục con)
    $allFiles = Get-ChildItem -Path $logFolder.FullName -Recurse -File | Where-Object {
        $_.LastWriteTime -lt $thresholdDate
    }

    foreach ($file in $allFiles) {
        $zipFile = "$($file.FullName).zip"

        try {
            Compress-Archive -Path $file.FullName -DestinationPath $zipFile -Force

            if (Test-Path $zipFile) {
                Remove-Item -Path $file.FullName -Force
                Write-Host "[!] Zip and delete success: $($file.Name)"
            } else {
                Write-Host "[!] Does not Zip: $($file.Name)"
            }
        } catch {
            Write-Host "[!] Error: $($file.FullName) - $($_.Exception.Message)"
        }
    }
}

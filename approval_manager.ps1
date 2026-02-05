<#
.SYNOPSIS
Approval Manager for FTE Bronze Tier Project

.DESCRIPTION
This script allows you to approve tasks from the Pending_Approval folder from PowerShell.
Usage:
    .\approval_manager.ps1 -List
    .\approval_manager.ps1 -Approve "filename.md"
    .\approval_manager.ps1 -Reject "filename.md"
    .\approval_manager.ps1 -Help

.PARAMETER List
Lists all pending approval items

.PARAMETER Approve
Approves a specific file from Pending_Approval

.PARAMETER Reject
Rejects a specific file from Pending_Approval

.PARAMETER VaultPath
Path to the AI Employee Vault

.PARAMETER PendingDir
Specific path to Pending_Approval directory
#>

param(
    [Parameter(Mandatory=$false)]
    [switch]$List,

    [Parameter(Mandatory=$false)]
    [string]$Approve,

    [Parameter(Mandatory=$false)]
    [string]$Reject,

    [Parameter(Mandatory=$false)]
    [string]$VaultPath,

    [Parameter(Mandatory=$false)]
    [string]$PendingDir
)

function Find-VaultPath {
    # Look for vault directory in common locations
    $possiblePaths = @(
        "AI_Employee_Vault",
        ".\AI_Employee_Vault",
        "..\AI_Employee_Vault",
        "vault",
        ".\vault"
    )

    foreach ($path in $possiblePaths) {
        if (Test-Path $path -PathType Container) {
            return $path
        }
    }

    # If not found, look for directories containing the expected subdirectories
    $items = Get-ChildItem -Directory
    foreach ($item in $items) {
        $vaultPath = Join-Path "." $item.Name
        $requiredDirs = @("Needs_Action", "Done", "Pending_Approval")
        $hasAllDirs = $true
        foreach ($dir in $requiredDirs) {
            if (!(Test-Path (Join-Path $vaultPath $dir))) {
                $hasAllDirs = $false
                break
            }
        }
        if ($hasAllDirs) {
            return $vaultPath
        }
    }

    # Default to a reasonable path
    return "AI_Employee_Vault"
}

function Show-PendingApprovals {
    param([string]$VaultPath)

    $pendingDir = Join-Path $VaultPath "Pending_Approval"

    if (!(Test-Path $pendingDir)) {
        Write-Host "[ERROR] Pending_Approval directory does not exist: $pendingDir" -ForegroundColor Red
        return
    }

    Write-Host "`n[APPROVALS] Pending Approval Items in $pendingDir:" -ForegroundColor Green
    Write-Host "=" * 70 -ForegroundColor Yellow

    $items = @()
    $files = Get-ChildItem -Path $pendingDir -Filter "*.md"

    foreach ($file in $files) {
        $filepath = Join-Path $pendingDir $file.Name
        $mtime = (Get-ItemProperty $filepath).LastWriteTime

        # Read the content to extract description
        try {
            $content = Get-Content $filepath -Raw -Encoding UTF8

            # Extract content after YAML frontmatter if present
            if ($content -match '^---\s*\r?\n(.|\r?\n)*?\r?\n---\s*\r?\n(.*)') {
                $body = $matches[2]
                if ($body.Length -gt 100) {
                    $preview = $body.Substring(0, 100) + "..."
                } else {
                    $preview = $body
                }
            } else {
                if ($content.Length -gt 100) {
                    $preview = $content.Substring(0, 100) + "..."
                } else {
                    $preview = $content
                }
            }

            # Clean up content for display
            $preview = $preview.Replace("`n", " ").Replace("`r", "").Trim()

            $items += [PSCustomObject]@{
                Name = $file.Name
                Date = $mtime.ToString("yyyy-MM-dd HH:mm:ss")
                Content = $preview
            }
        } catch {
            $items += [PSCustomObject]@{
                Name = $file.Name
                Date = $mtime.ToString("yyyy-MM-dd HH:mm:ss")
                Content = "[Could not read: $($_.Exception.Message)]"
            }
        }
    }

    if ($items.Count -eq 0) {
        Write-Host "[INFO] No pending approval items found." -ForegroundColor Cyan
    } else {
        foreach ($item in $items) {
            Write-Host "[$($item.Date)] $($item.Name)" -ForegroundColor White
            Write-Host "  Content preview: $($item.Content)..." -ForegroundColor Gray
            Write-Host ""
        }
    }
}

function Approve-Item {
    param(
        [string]$VaultPath,
        [string]$Filename
    )

    $pendingDir = Join-Path $VaultPath "Pending_Approval"
    $doneDir = Join-Path $VaultPath "Done"
    $needsActionDir = Join-Path $VaultPath "Needs_Action"

    $pendingFile = Join-Path $pendingDir $Filename

    if (!(Test-Path $pendingFile)) {
        Write-Host "[ERROR] File does not exist in Pending_Approval: $Filename" -ForegroundColor Red
        return $false
    }

    try {
        # Read the file to update its status
        $content = Get-Content $pendingFile -Raw -Encoding UTF8

        # If there's YAML frontmatter, update the status
        if ($content -match '^---\s*\r?\n(.|\r?\n)*?\r?\n---\s*\r?\n(.*)') {
            $yamlStr = $matches[1]
            $body = $matches[2]

            # Parse and update the YAML frontmatter
            # Since PowerShell doesn't have native YAML support, we'll manually update common fields
            $currentDate = Get-Date -Format "yyyy-MM-ddTHH:mm:ss.fffZ"

            # Find if status already exists and update it, otherwise add it
            if ($yamlStr -match 'status:') {
                $updatedYaml = $yamlStr -replace '(status:\s*)(.*)', "`${1}approved"
            } else {
                $updatedYaml = $yamlStr.TrimEnd() + "`nstatus: approved"
            }

            if ($yamlStr -match 'approved_at:') {
                $updatedYaml = $updatedYaml -replace '(approved_at:\s*)(.*)', "`${1}$currentDate"
            } else {
                $updatedYaml = $updatedYaml.TrimEnd() + "`napproved_at: $currentDate"
            }

            if ($yamlStr -match 'approved_by:') {
                $updatedYaml = $updatedYaml -replace '(approved_by:\s*)(.*)', "`${1}command_line_user"
            } else {
                $updatedYaml = $updatedYaml.TrimEnd() + "`napproved_by: command_line_user"
            }

            # Reconstruct the file with updated frontmatter
            $updatedContent = "---`n$updatedYaml`n---`n$body"
        } else {
            $updatedContent = $content
        }

        # Move to Done directory
        $doneFile = Join-Path $doneDir $Filename

        # Write the updated content back to the file temporarily
        Set-Content -Path $pendingFile -Value $updatedContent -Encoding UTF8

        # Move the file to Done
        Move-Item -Path $pendingFile -Destination $doneFile

        Write-Host "[SUCCESS] Approved and moved to Done: $Filename" -ForegroundColor Green
        return $true

    } catch {
        Write-Host "[ERROR] Failed to approve $Filename`: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

function Reject-Item {
    param(
        [string]$VaultPath,
        [string]$Filename
    )

    $pendingDir = Join-Path $VaultPath "Pending_Approval"

    $pendingFile = Join-Path $pendingDir $Filename

    if (!(Test-Path $pendingFile)) {
        Write-Host "[ERROR] File does not exist in Pending_Approval: $Filename" -ForegroundColor Red
        return $false
    }

    try {
        # Read the file to update its status
        $content = Get-Content $pendingFile -Raw -Encoding UTF8

        # If there's YAML frontmatter, update the status
        if ($content -match '^---\s*\r?\n(.|\r?\n)*?\r?\n---\s*\r?\n(.*)') {
            $yamlStr = $matches[1]
            $body = $matches[2]

            # Parse and update the YAML frontmatter
            $currentDate = Get-Date -Format "yyyy-MM-ddTHH:mm:ss.fffZ"

            # Find if status already exists and update it, otherwise add it
            if ($yamlStr -match 'status:') {
                $updatedYaml = $yamlStr -replace '(status:\s*)(.*)', "`${1}rejected"
            } else {
                $updatedYaml = $yamlStr.TrimEnd() + "`nstatus: rejected"
            }

            if ($yamlStr -match 'rejected_at:') {
                $updatedYaml = $updatedYaml -replace '(rejected_at:\s*)(.*)', "`${1}$currentDate"
            } else {
                $updatedYaml = $updatedYaml.TrimEnd() + "`nrejected_at: $currentDate"
            }

            if ($yamlStr -match 'rejected_by:') {
                $updatedYaml = $updatedYaml -replace '(rejected_by:\s*)(.*)', "`${1}command_line_user"
            } else {
                $updatedYaml = $updatedYaml.TrimEnd() + "`nrejected_by: command_line_user"
            }

            if ($yamlStr -match 'reason:') {
                $updatedYaml = $updatedYaml -replace '(reason:\s*)(.*)', "`${1}Rejected via command line"
            } else {
                $updatedYaml = $updatedYaml.TrimEnd() + "`nreason: Rejected via command line"
            }

            # Reconstruct the file with updated frontmatter
            $updatedContent = "---`n$updatedYaml`n---`n$body"
        } else {
            $updatedContent = $content
        }

        # Update the file with rejection status
        Set-Content -Path $pendingFile -Value $updatedContent -Encoding UTF8

        Write-Host "[SUCCESS] Rejected item: $Filename" -ForegroundColor Yellow
        Write-Host "[INFO] File remains in Pending_Approval with rejection status." -ForegroundColor Cyan
        return $true

    } catch {
        Write-Host "[ERROR] Failed to reject $Filename`: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Main execution
try {
    # Determine vault path
    if ($VaultPath) {
        $vaultPath = $VaultPath
    } elseif ($PendingDir) {
        # If pending dir is specified, derive vault path from it
        $vaultPath = Split-Path $PendingDir -Parent
    } else {
        $vaultPath = Find-VaultPath
    }

    if ($List) {
        Show-PendingApprovals -VaultPath $vaultPath
        return
    }

    if ($Approve) {
        $success = Approve-Item -VaultPath $vaultPath -Filename $Approve
        exit $(if ($success) { 0 } else { 1 })
    }

    if ($Reject) {
        $success = Reject-Item -VaultPath $vaultPath -Filename $Reject
        exit $(if ($success) { 0 } else { 1 })
    }

    # If no parameters provided, show help
    if (!$List -and !$Approve -and !$Reject) {
        Write-Host "Approval Manager for AI Employee System" -ForegroundColor Green
        Write-Host ""
        Write-Host "USAGE:" -ForegroundColor Yellow
        Write-Host "    .\approval_manager.ps1 -List" -ForegroundColor White
        Write-Host "    .\approval_manager.ps1 -Approve `"filename.md`"" -ForegroundColor White
        Write-Host "    .\approval_manager.ps1 -Reject `"filename.md`"" -ForegroundColor White
        Write-Host ""
        Write-Host "EXAMPLES:" -ForegroundColor Yellow
        Write-Host "  .\approval_manager.ps1 -List" -ForegroundColor White
        Write-Host "  .\approval_manager.ps1 -Approve `"approval_20231201_123456_sometask.md`"" -ForegroundColor White
        Write-Host "  .\approval_manager.ps1 -Reject `"approval_20231201_123456_sometask.md`"" -ForegroundColor White
    }

} catch {
    Write-Host "[ERROR] $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
chcp 65001 >nul
$ErrorActionPreference = 'SilentlyContinue'
Write-Host "=== 666项目环境检测 ==="
Write-Host ""
Write-Host "--- 包管理器 ---"
foreach ($pm in "scoop","winget","choco") {
    $c = Get-Command $pm -ErrorAction SilentlyContinue
    if ($c) { Write-Host "$pm : $($c.Source)" } else { Write-Host "$pm : 未安装" }
}
Write-Host ""
Write-Host "--- 基础运行时 ---"
foreach ($cmd in "node","npm","python","pip","git","curl") {
    $c = Get-Command $cmd -ErrorAction SilentlyContinue
    if ($c) {
        try { $v = & $cmd --version 2>$null | Select-Object -First 1; Write-Host "$cmd : $v" }
        catch { Write-Host "$cmd : 已安装 (版本获取失败)" }
    } else { Write-Host "$cmd : 未安装" }
}
Write-Host ""
Write-Host "--- CLI工具 ---"
foreach ($cmd in "gh","jq","rg","ffmpeg") {
    $c = Get-Command $cmd -ErrorAction SilentlyContinue
    if ($c) { Write-Host "$cmd : 已安装" } else { Write-Host "$cmd : 未安装" }
}
Write-Host ""
Write-Host "--- Scoop buckets ---"
scoop bucket list 2>$null

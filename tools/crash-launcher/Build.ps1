param(
    [string]$OutputDirectory = (Join-Path $PSScriptRoot 'build'),
    [switch]$IntegrationTests
)
$ErrorActionPreference = 'Stop'
$compiler = Join-Path $env:WINDIR 'Microsoft.NET\Framework\v4.0.30319\csc.exe'
if (!(Test-Path $compiler)) { throw 'The x86 .NET Framework 4 compiler is required.' }
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
$output = Join-Path (Resolve-Path $OutputDirectory).Path 'CrashFixLauncher.exe'
$sources = @('Native.cs', 'PatchData.g.cs', 'ArbiterEndpoint.cs', 'Program.cs') | ForEach-Object { Join-Path $PSScriptRoot $_ }
& $compiler /nologo /target:exe /platform:x86 /optimize+ /checked+ "/out:$output" @sources
if ($LASTEXITCODE -ne 0) { throw 'Launcher compilation failed.' }
& $output --self-test
if ($LASTEXITCODE -ne 0) { throw 'Launcher self-test failed.' }
if ($IntegrationTests) {
    $testOutput = Join-Path (Resolve-Path $OutputDirectory).Path 'LauncherIntegrationTests.exe'
    & $compiler /nologo /target:exe /platform:x86 /optimize+ /checked+ /define:LAUNCHER_TESTS /main:DarkAgesCrashLauncher.IntegrationTests "/out:$testOutput" @sources (Join-Path $PSScriptRoot 'IntegrationTests.cs')
    if ($LASTEXITCODE -ne 0) { throw 'Integration test compilation failed.' }
}
Write-Output "Built $output"

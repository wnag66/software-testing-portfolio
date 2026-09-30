param(
    [string]$JmeterHome = "",
    [int]$Port = 18080
)

$ErrorActionPreference = "Stop"
$ApiRoot = Split-Path -Parent $PSScriptRoot
$RepositoryRoot = Split-Path -Parent $ApiRoot
$OutputRoot = Join-Path $ApiRoot "jmeter\reports"
$JmxFile = Join-Path $ApiRoot "jmeter\device-order-api.jmx"
$JarFile = Join-Path $ApiRoot "target\api-testlab-1.0.0.jar"

New-Item -ItemType Directory -Force -Path $OutputRoot | Out-Null

if (-not (Test-Path -LiteralPath $JarFile)) {
    & mvn -q -f (Join-Path $RepositoryRoot "pom.xml") -pl api-testlab package "-DskipTests"
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to package the API test lab"
    }
}

$JmeterExecutable = if ($JmeterHome) {
    Join-Path $JmeterHome "bin\jmeter.bat"
} else {
    (Get-Command jmeter -ErrorAction Stop).Source
}

$Process = Start-Process `
    -FilePath "java" `
    -ArgumentList @("-jar", $JarFile, "--server.port=$Port") `
    -PassThru `
    -WindowStyle Hidden `
    -RedirectStandardOutput (Join-Path $OutputRoot "application.log") `
    -RedirectStandardError (Join-Path $OutputRoot "application-error.log")

try {
    $Ready = $false
    for ($Attempt = 1; $Attempt -le 60; $Attempt++) {
        try {
            $Response = Invoke-RestMethod -Uri "http://localhost:$Port/actuator/health" -TimeoutSec 2
            if ($Response.status -eq "UP") {
                $Ready = $true
                break
            }
        } catch {
            Start-Sleep -Seconds 1
        }
    }
    if (-not $Ready) {
        throw "API did not become ready on port $Port"
    }

    $Scenarios = @(
        @{ Name = "smoke"; Threads = 1; RampUp = 1; Duration = 10 },
        @{ Name = "baseline"; Threads = 20; RampUp = 10; Duration = 60 },
        @{ Name = "load"; Threads = 50; RampUp = 20; Duration = 120 }
    )

    foreach ($Scenario in $Scenarios) {
        $ScenarioRoot = Join-Path $OutputRoot $Scenario.Name
        if (Test-Path -LiteralPath $ScenarioRoot) {
            Remove-Item -LiteralPath $ScenarioRoot -Recurse -Force
        }
        New-Item -ItemType Directory -Force -Path $ScenarioRoot | Out-Null
        $JtlFile = Join-Path $ScenarioRoot "results.jtl"
        $Dashboard = Join-Path $ScenarioRoot "html"

        & $JmeterExecutable `
            -n `
            -t $JmxFile `
            "-Jhost=localhost" `
            "-Jport=$Port" `
            "-Jthreads=$($Scenario.Threads)" `
            "-JrampUp=$($Scenario.RampUp)" `
            "-Jduration=$($Scenario.Duration)" `
            -l $JtlFile `
            -e `
            -o $Dashboard

        if ($LASTEXITCODE -ne 0) {
            throw "JMeter scenario failed: $($Scenario.Name)"
        }
    }
} finally {
    if ($Process -and -not $Process.HasExited) {
        Stop-Process -Id $Process.Id -Force
    }
    $Listeners = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    foreach ($Listener in $Listeners) {
        if ($Listener.OwningProcess -gt 0) {
            Stop-Process -Id $Listener.OwningProcess -Force -ErrorAction SilentlyContinue
        }
    }
}

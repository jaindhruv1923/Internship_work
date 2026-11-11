param(
    [int]$Port = 3000
)

$root = $PSScriptRoot
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:$Port/")

try {
    $listener.Start()
    Write-Host "[Digii Campus Dev Server] Serving $root at http://localhost:$Port/" -ForegroundColor Green
    Write-Host "Press Ctrl+C to terminate the server." -ForegroundColor Gray

    while ($listener.IsListening) {
        try {
            $context = $listener.GetContext()
            $request = $context.Request
            $response = $context.Response

            $path = $request.Url.LocalPath.TrimStart('/')
            if ([string]::IsNullOrWhiteSpace($path)) {
                $path = "index.html"
            }

            # Security sanitization
            $path = $path.Replace('/', [System.IO.Path]::DirectorySeparatorChar)
            $filePath = Join-Path $root $path

            # Allow CORS for dev
            $response.AddHeader("Access-Control-Allow-Origin", "*")
            $response.AddHeader("Access-Control-Allow-Methods", "GET, POST, HEAD, OPTIONS")
            $response.AddHeader("Access-Control-Allow-Headers", "*")

            if ($request.HttpMethod -eq 'OPTIONS') {
                $response.StatusCode = 200
                $response.OutputStream.Close()
                continue
            }

            if (Test-Path $filePath -PathType Leaf) {
                $ext = [System.IO.Path]::GetExtension($filePath).ToLower()
                $mime = switch ($ext) {
                    ".html" { "text/html; charset=utf-8" }
                    ".json" { "application/json; charset=utf-8" }
                    ".js"   { "application/javascript; charset=utf-8" }
                    ".css"  { "text/css; charset=utf-8" }
                    ".svg"  { "image/svg+xml" }
                    ".png"  { "image/png" }
                    default { "application/octet-stream" }
                }

                $bytes = [System.IO.File]::ReadAllBytes($filePath)
                $response.ContentType = $mime
                $response.ContentLength64 = $bytes.Length
                $response.StatusCode = 200
                if ($request.HttpMethod -ne 'HEAD') {
                    $response.OutputStream.Write($bytes, 0, $bytes.Length)
                }
            } else {
                $response.StatusCode = 404
                $errBytes = [System.Text.Encoding]::UTF8.GetBytes("404 - File Not Found: $path")
                $response.ContentType = "text/plain"
                $response.ContentLength64 = $errBytes.Length
                if ($request.HttpMethod -ne 'HEAD') {
                    $response.OutputStream.Write($errBytes, 0, $errBytes.Length)
                }
            }

            $response.OutputStream.Close()
        } catch {
            Write-Host "Request error: $_" -ForegroundColor DarkGray
        }
    }
} catch {
    Write-Host "Server stopped: $_" -ForegroundColor Yellow
} finally {
    if ($listener.IsListening) {
        $listener.Stop()
    }
    $listener.Close()
}

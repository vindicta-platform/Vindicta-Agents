@echo off
REM Local build pipeline for Windows (PowerShell/CMD)
REM Usage:
REM   automation\build.cmd              # build both
REM   automation\build.cmd base         # base only
REM   automation\build.cmd slim         # slim only

setlocal
set TARGET=%1
if "%TARGET%"=="" set TARGET=all

set CONTEXT=%~dp0..\. devcontainer

if "%TARGET%"=="base" goto :base
if "%TARGET%"=="slim" goto :slim
if "%TARGET%"=="all" goto :all
echo Usage: automation\build.cmd [base^|slim^|all]
exit /b 1

:all
call :base
call :slim
goto :done

:base
echo === Building base image (vindicta-agent) ===
docker build -t vindicta-agent .devcontainer\
echo.
goto :eof

:slim
echo === Building slim image (vindicta-agent-slim) ===
docker build -f .devcontainer\Dockerfile.slim -t vindicta-agent-slim .devcontainer\
echo.
goto :eof

:done
echo === Done ===
docker images --filter "reference=vindicta-agent*" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

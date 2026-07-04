@echo off
title Odoo AI Audit Platform Bootstrap v0.1
color 0A

echo.
echo ===========================================
echo   Odoo AI Audit Platform Bootstrap v0.1
echo ===========================================
echo.

REM ===============================
REM Create Folders
REM ===============================

mkdir docs 2>nul
mkdir builder 2>nul
mkdir templates 2>nul
mkdir scripts 2>nul
mkdir sql 2>nul
mkdir data 2>nul
mkdir workflows 2>nul
mkdir mcp 2>nul
mkdir prompts 2>nul
mkdir assets 2>nul
mkdir tests 2>nul
mkdir .vscode 2>nul
mkdir .github 2>nul

REM ===============================
REM Create README Files
REM ===============================

(
echo # Odoo AI Audit Platform
echo.
echo Version: 0.1.0-alpha
echo.
echo ## Vision
echo Build an AI-powered Accounting ^& POS Audit Platform for Odoo 18 Community Edition.
echo.
echo ## Current Status
echo Foundation Phase
) > README.md

(
echo # Project Status
echo.
echo Current Sprint: Sprint-001
echo.
echo Current Task:
echo Build Foundation
echo.
echo Progress:
echo 5%%
) > PROJECT_STATUS.md

(
echo # Roadmap
echo.
echo - Foundation
echo - Documentation
echo - Data Dictionary
echo - SQL Library
echo - MCP
echo - n8n
echo - AI Assistant
) > ROADMAP.md

(
echo # Changelog
echo.
echo ## v0.1.0-alpha
echo.
echo - Initial Project
) > CHANGELOG.md

(
echo MIT License
echo.
echo Copyright ^(c^) 2026
) > LICENSE

(
echo __pycache__/
echo *.pyc
echo .venv/
echo .env
echo *.log
echo .DS_Store
) > .gitignore

REM ===============================
REM Folder README Files
REM ===============================

for %%d in (
docs
builder
templates
scripts
sql
data
workflows
mcp
prompts
assets
tests
) do (
(
echo # %%d
echo.
echo This folder is part of the Odoo AI Audit Platform.
) > %%d\README.md
)

echo.
echo ===========================================
echo Foundation Pack Created Successfully
echo ===========================================
echo.

pause
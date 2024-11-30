@echo off
REM Remove output directory if it exists
if exist "output" (
    rmdir /s /q "output"
)

REM Remove build directory if it exists
if exist "build" (
    rmdir /s /q "build"
)

REM Remove dist directory if it exists
if exist "dist" (
    rmdir /s /q "dist"
)

REM Remove .spec files if they exist
for %%f in (*.spec) do del "%%f"

REM Remove .zip files if they exist
for %%f in (*.zip) do del "%%f"

echo Cleanup complete.
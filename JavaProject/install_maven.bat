@echo off
:: Install Maven
@powershell -Command Set-ExecutionPolicy -Scope CurrentUser -Force; iwr -useb https://raw.githubusercontent.com/NateTheGreat/maven-installer/master/maven-installer.ps1 -OutFile maven-installer.ps1; .\maven-installer.ps1
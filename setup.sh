#!/usr/bin/bash
script_dir=$(dirname "$0")
echo "Updating APT package list..."
sudo apt update
echo "Installing JAVA..."
sudo apt install openjdk-17-jdk -y

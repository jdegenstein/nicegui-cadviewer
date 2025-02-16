package main

import (
    "log"
    "os/exec"
)

func main() {
    cmd := exec.Command("./python/python.exe", "-m", "cadviewer")
    output, err := cmd.CombinedOutput()
    if err != nil {
        log.Fatalf("Command execution failed: %v", err)
    }
    log.Printf("Command output: %s", output)
}
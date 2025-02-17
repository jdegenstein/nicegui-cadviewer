package main

import (
    "log"
    "os"
    "os/exec"
)

func main() {
    cmd := exec.Command("./python/python.exe", "-m", "nice123d")

    // Redirect the command's standard output and standard error to the Go program's standard output and standard error
    cmd.Stdout = os.Stdout
    cmd.Stderr = os.Stderr

    // Run the command
    err := cmd.Run()
    if err != nil {
        log.Fatalf("Command execution failed: %v", err)
    }
}

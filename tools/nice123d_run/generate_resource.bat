python create_icon.py

go install github.com/akavel/rsrc@latest'
rsrc -arch 386 -ico app.ico
rsrc -arch amd64 -ico app.ico

go build -o nice123d_run.exe

# -*- coding: utf-8 -*-
# Tämä skripti katsoo auditin lokeista käytetyt tiedostot ja tallentaa ne importantFiles.txt -tiedostoon.

from pathlib import Path


filesAndPaths = []
cwd = ""
fileCount = 0
pathCount = 0
deletedCount = 0

accessedFilesListPath = "/path/to/importantFiles.txt"
auditLogFilePath = "/var/log/audit/audit.log"


with file(accessedFilesListPath, "r") as oldFiles:
    for oldFile in oldFiles:
        filesAndPaths.append(oldFile)

with file(auditLogFilePath, "r") as auditLog:
    for row in auditLog:
        if "type=CWD" in row:
            cwd = row.split("\"")[1]

        if "type=PATH" in row:
            if "\"" in row:
                path = row.split("\"")[1] + "\n"
                if path.startswith(cwd):
                    # print "Current work dir already in the path", cwd, " ", path
                    pass
                else:
                    # print "Current work dir not found in the path", cwd, " ", path
                    if path.startswith("./"):
                        path = path.replace("./", "/")
                    path = cwd + path
                if not any(path in w for w in filesAndPaths) and path.startswith("/var/www/"):
                    filesAndPaths.append(path)

with file(accessedFilesListPath, "w") as oldFiles:
    for path in sorted(filesAndPaths):
        if Path(path[:-1]).is_file():
            fileCount += 1
            # print path,
            oldFiles.write(path)
        elif Path(path[:-1]).is_dir():
            pathCount += 1
        else:
            deletedCount += 1

print "Results\nFiles:", fileCount, "	Paths:", pathCount, "	Deleted:", deletedCount, "\n"

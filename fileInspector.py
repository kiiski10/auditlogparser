# -*- coding: utf-8 -*-
# Skripti katsoo auditin lokeista käytetyt tiedostot ja tallentaa ne importantFiles.txt -tiedostoon.

filePaths = []
fileCount = 0
newFileCount = 0
cwd = ""

accessedFilesListPath = "importantFiles.txt"
auditLogFilePath = "/var/log/audit/audit.log"

with file(accessedFilesListPath, "r") as oldFiles:
    for oldFile in oldFiles:
        fileCount += 1
        filePaths.append(oldFile)

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
                if not any(path in w for w in filePaths) and path.startswith("/var/www/"):
                    filePaths.append(path)
                    newFileCount += 1

with file(accessedFilesListPath, "w") as oldFiles:
    for path in sorted(filePaths):
        # print path,
        oldFiles.write(path)

print "Total of", newFileCount + fileCount, "files which of", newFileCount, "was new"

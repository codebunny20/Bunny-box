Option Explicit

Dim fso, wmi, drives, d
Dim pattern, results, maxShown, logPath

pattern = InputBox("Enter full or partial file name to search for:", "System File Search")

If pattern = "" Then
    WScript.Quit
End If

Set fso = CreateObject("Scripting.FileSystemObject")
Set wmi = GetObject("winmgmts:\\.\root\cimv2")
Set drives = wmi.ExecQuery("Select * from Win32_LogicalDisk Where DriveType = 3") ' fixed drives

results = ""
maxShown = 50
logPath = fso.BuildPath(fso.GetSpecialFolder(2), "system_file_search_results.txt")

Dim logFile
Set logFile = fso.CreateTextFile(logPath, True)

For Each d In drives
    On Error Resume Next
    SearchFolder d.DeviceID & "\", pattern, logFile
    On Error GoTo 0
Next

logFile.Close

If results = "" Then
    MsgBox "No files found matching: " & pattern
Else
    MsgBox "Matches found. Opening results file..."
    CreateObject("WScript.Shell").Run Chr(34) & logPath & Chr(34)
End If


Sub SearchFolder(folderPath, pattern, logFile)
    Dim folder, file, subFolder, shownCount

    On Error Resume Next
    Set folder = fso.GetFolder(folderPath)
    If Err.Number <> 0 Then
        Err.Clear
        Exit Sub
    End If
    On Error GoTo 0

    For Each file In folder.Files
        If InStr(1, LCase(file.Name), LCase(pattern), vbTextCompare) > 0 Then
            logFile.WriteLine file.Path

            If shownCount < maxShown Then
                results = results & file.Path & vbCrLf
                shownCount = shownCount + 1
            End If
        End If
    Next

    For Each subFolder In folder.SubFolders
        SearchFolder subFolder.Path, pattern, logFile
    Next
End Sub

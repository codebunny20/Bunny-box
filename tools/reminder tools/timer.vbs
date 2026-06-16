Option Explicit

' Relaunch under wscript.exe if started via cscript.exe (which hides GUI dialogs).
If InStr(LCase(WScript.FullName), "cscript") > 0 Then
    Dim oShell : Set oShell = CreateObject("WScript.Shell")
    oShell.Run "wscript.exe """ & WScript.ScriptFullName & """"
    WScript.Quit
End If

Dim minutesInput
Dim minutes
Dim sleepMs

minutesInput = Trim(InputBox("Enter number of minutes (decimals allowed):", "Timer"))

If Len(minutesInput) = 0 Then
    WScript.Quit
End If

If Not IsNumeric(minutesInput) Then
    MsgBox "Invalid input. Please enter a numeric value.", 48, "Timer"
    WScript.Quit
End If

minutes = CDbl(minutesInput)

If minutes <= 0 Then
    MsgBox "Enter a number greater than zero.", 48, "Timer"
    WScript.Quit
End If

sleepMs = CLng(minutes * 60000)

' WScript.Sleep accepts a 32-bit millisecond value.
If sleepMs > 2147483647 Then
    MsgBox "Timer is too long. Use 35791 minutes or fewer.", 48, "Timer"
    WScript.Quit
End If

WScript.Sleep sleepMs

MsgBox "Time's up! (" & CStr(minutes) & " minutes)", 64, "Timer"

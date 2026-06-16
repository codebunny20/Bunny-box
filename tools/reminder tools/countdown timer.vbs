Option Explicit

Dim minutes, ms

minutes = InputBox("Minutes to wait:", "Countdown Timer", 10)
If minutes = "" Then WScript.Quit
If Not IsNumeric(minutes) Then
    MsgBox "Enter a number."
    WScript.Quit
End If

minutes = CLng(minutes)
If minutes <= 0 Then
    MsgBox "Minutes must be greater than zero."
    WScript.Quit
End If

ms = minutes * 60 * 1000

MsgBox "Timer started for " & minutes & " minute(s)."
WScript.Sleep ms
MsgBox "Time's up! (" & minutes & " minute(s))"

Option Explicit

Dim msg, res

msg = InputBox("Reminder message (shown every hour):", "Hourly Reminder", "Take a break")
If msg = "" Then WScript.Quit

Do
    WScript.Sleep 60 * 60 * 1000 ' 1 hour
    res = MsgBox(msg & vbCrLf & vbCrLf & "Continue hourly reminders?", vbYesNo + vbInformation, "Hourly Reminder")
    If res = vbNo Then Exit Do
Loop

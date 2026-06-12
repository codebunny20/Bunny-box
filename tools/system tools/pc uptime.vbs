Set wmi = GetObject("winmgmts:\\.\root\cimv2")
Set os = wmi.ExecQuery("Select * from Win32_OperatingSystem")

For Each o In os
    raw = o.LastBootUpTime
Next

' --- Parse WMI timestamp ---
yr  = Left(raw, 4)
mo  = Mid(raw, 5, 2)
dy  = Mid(raw, 7, 2)
hr  = Mid(raw, 9, 2)
mn  = Mid(raw, 11, 2)
sc  = Mid(raw, 13, 2)

bootTime = CDate(mo & "/" & dy & "/" & yr & " " & hr & ":" & mn & ":" & sc)

' --- Calculate uptime ---
nowTime = Now
diff = DateDiff("s", bootTime, nowTime)

uptimeDays    = diff \ 86400
uptimeHours   = (diff Mod 86400) \ 3600
uptimeMinutes = (diff Mod 3600) \ 60
uptimeSeconds = diff Mod 60

hh = Right("0" & uptimeHours, 2)
mm = Right("0" & uptimeMinutes, 2)
ss = Right("0" & uptimeSeconds, 2)

msg = "System Uptime:" & vbCrLf & vbCrLf & _
      "Boot Time: " & bootTime & vbCrLf & vbCrLf & _
      "Days: " & uptimeDays & vbCrLf & _
      "Hours: " & uptimeHours & vbCrLf & _
      "Minutes: " & uptimeMinutes & vbCrLf & _
      "Seconds: " & uptimeSeconds & vbCrLf & vbCrLf & _
      "HH:MM:SS → " & hh & ":" & mm & ":" & ss & vbCrLf & _
      "Total Minutes: " & Round(diff / 60, 2) & vbCrLf & _
      "Total Seconds: " & diff

MsgBox msg

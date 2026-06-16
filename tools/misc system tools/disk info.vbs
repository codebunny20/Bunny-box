Set wmi = GetObject("winmgmts:\\.\root\cimv2")
Set disks = wmi.ExecQuery("Select * from Win32_LogicalDisk Where DriveType = 3")

msg = "Disk Info:" & vbCrLf & vbCrLf

For Each d In disks
    total = Round(d.Size / 1024 / 1024 / 1024, 2)
    free  = Round(d.FreeSpace / 1024 / 1024 / 1024, 2)
    msg = msg & d.DeviceID & ":  " & free & " GB free / " & total & " GB total" & vbCrLf
Next

MsgBox msg

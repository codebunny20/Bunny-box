Set wmi = GetObject("winmgmts:\\.\root\cimv2")
Set bios = wmi.ExecQuery("Select * from Win32_BIOS")

For Each b In bios
    vendor = b.Manufacturer
    version = b.SMBIOSBIOSVersion
    Exit For
Next

MsgBox "BIOS:" & vbCrLf & vbCrLf & vendor & " - " & version

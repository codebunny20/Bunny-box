Set wmi = GetObject("winmgmts:\\.\root\cimv2")
Set procs = wmi.ExecQuery("Select * from Win32_Process")

count = 0
For Each p In procs
    count = count + 1
Next

MsgBox "Running Processes: " & count

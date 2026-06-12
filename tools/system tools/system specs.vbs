Set wmi = GetObject("winmgmts:\\.\root\cimv2")

' --- CPU ---
Set cpus = wmi.ExecQuery("Select * from Win32_Processor")
For Each cpu In cpus
    cpuName = cpu.Name
    cpuCores = cpu.NumberOfCores
    cpuThreads = cpu.NumberOfLogicalProcessors
Next

' --- RAM ---
Set ram = wmi.ExecQuery("Select * from Win32_ComputerSystem")
For Each r In ram
    totalRAM = Round(r.TotalPhysicalMemory / 1024 / 1024 / 1024, 2)
Next

' --- GPU ---
Set gpus = wmi.ExecQuery("Select * from Win32_VideoController")
For Each gpu In gpus
    gpuName = gpu.Name
    Exit For
Next

' --- OS ---
Set os = wmi.ExecQuery("Select * from Win32_OperatingSystem")
For Each o In os
    osName = o.Caption
    osBuild = o.BuildNumber
Next

msg = "PC Specs:" & vbCrLf & vbCrLf & _
      "CPU: " & cpuName & vbCrLf & _
      "Cores: " & cpuCores & " | Threads: " & cpuThreads & vbCrLf & vbCrLf & _
      "RAM: " & totalRAM & " GB" & vbCrLf & vbCrLf & _
      "GPU: " & gpuName & vbCrLf & vbCrLf & _
      "OS: " & osName & " (Build " & osBuild & ")"

MsgBox msg

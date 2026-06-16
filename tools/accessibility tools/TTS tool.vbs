Option Explicit

' If launched under cscript.exe, InputBox dialogs are suppressed.
' Relaunch under wscript.exe so all prompts appear correctly.
If InStr(LCase(WScript.FullName), "cscript") > 0 Then
    Dim oShell : Set oShell = CreateObject("WScript.Shell")
    oShell.Run "wscript.exe """ & WScript.ScriptFullName & """"
    WScript.Quit
End If

Dim voice
Dim text
Dim volumeInput
Dim rateInput
Dim volume
Dim rate

On Error Resume Next
Set voice = CreateObject("SAPI.SpVoice")
If Err.Number <> 0 Then
    MsgBox "Unable to initialize speech engine.", 16, "TTS"
    WScript.Quit
End If
On Error GoTo 0

text = Trim(InputBox("Enter text for Text to Speech:", "Text to Speech"))

If Len(text) = 0 Then
    MsgBox "No text entered.", 48, "TTS"
    WScript.Quit
End If

volume = 100
rate = 0

volumeInput = Trim(InputBox("Volume (0-100):", "TTS Settings", "100"))
If Len(volumeInput) > 0 Then
    If Not IsNumeric(volumeInput) Then
        MsgBox "Volume must be a number from 0 to 100.", 48, "TTS"
        WScript.Quit
    End If

    volume = CInt(volumeInput)
    If volume < 0 Or volume > 100 Then
        MsgBox "Volume must be between 0 and 100.", 48, "TTS"
        WScript.Quit
    End If
End If

rateInput = Trim(InputBox("Rate (-10 to 10):", "TTS Settings", "0"))
If Len(rateInput) > 0 Then
    If Not IsNumeric(rateInput) Then
        MsgBox "Rate must be a number from -10 to 10.", 48, "TTS"
        WScript.Quit
    End If

    rate = CInt(rateInput)
    If rate < -10 Or rate > 10 Then
        MsgBox "Rate must be between -10 and 10.", 48, "TTS"
        WScript.Quit
    End If
End If

voice.Volume = volume
voice.Rate = rate
voice.Speak text

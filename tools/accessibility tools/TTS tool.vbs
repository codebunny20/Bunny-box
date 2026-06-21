' File: tts_tool.vbs
Option Explicit

Dim args, textToSpeak, voice, rate, volume

Set args = WScript.Arguments

' If text is passed as an argument, use that; otherwise prompt
If args.Count > 0 Then
    textToSpeak = JoinArgs(args)
Else
    textToSpeak = InputBox("Enter the text to speak:", "TTS Tool")
End If

If Trim(textToSpeak) = "" Then WScript.Quit

' Create SAPI voice
On Error Resume Next
Set voice = CreateObject("SAPI.SpVoice")
If Err.Number <> 0 Or voice Is Nothing Then
    MsgBox "Error: Could not create SAPI.SpVoice. Is SAPI installed?", vbCritical, "TTS Tool"
    WScript.Quit
End If
On Error GoTo 0

' Configure defaults (tweak if you want)
rate = 0      ' Range is typically -10 to 10
volume = 100  ' 0–100

voice.Rate = rate
voice.Volume = volume

' Speak synchronously
voice.Speak textToSpeak, 0

' Cleanup
Set voice = Nothing

' -------- Helpers --------
Function JoinArgs(a)
    Dim i, tmp
    tmp = ""
    For i = 0 To a.Count - 1
        If i > 0 Then tmp = tmp & " "
        tmp = tmp & a(i)
    Next
    JoinArgs = tmp
End Function

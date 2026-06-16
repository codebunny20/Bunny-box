Set voice = CreateObject("SAPI.SpVoice")

text = InputBox("Enter text for Text to Speech:", "Text to Speech")

If text = "" Then
    MsgBox "No text entered.", 48, "TTS"
    WScript.Quit
End If

voice.Volume = 100   '0–100
voice.Rate = 0       '‑10 to +10

voice.Speak text

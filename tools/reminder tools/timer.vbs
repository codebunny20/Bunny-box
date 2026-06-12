minutes = InputBox("Enter number of minutes:", "Timer")

If minutes = "" Then
    WScript.Quit
End If

If Not IsNumeric(minutes) Then
    MsgBox "Invalid input. Please enter a number."
    WScript.Quit
End If

minutes = CInt(minutes)

If minutes <= 0 Then
    MsgBox "Enter a number greater than zero."
    WScript.Quit
End If

WScript.Sleep minutes * 60000

MsgBox "Time's up! (" & minutes & " minutes)"

' =============================================================================
' =============================================================================
Function MainCalc()
	Dim V, H, L, tol As Double
	Dim MaxIter As Integer

	V = Val(TextBoxV.Text)
	H = Val(TextBoxH.Text)
	L = Val(TextBoxL.Text)
	tol = Val(TextBoxTol.Text)
	MaxIter = Val(TextBoxMaxIter.Text)
	'check L
	Dim minL As Double
	minL = Math.Sqrt(H ^ 2 + V ^ 2)
	If L < minL Then
		MsgBox("Error. L must be at least Sqr(H^2+V^2).")
		Return 1
		'Exit Function
	End If
	'check tol and maxiter
	If Not (IsNumeric(tol) Or IsNumeric(MaxIter)) Then
		MsgBox("Error. Tolerance and maximum number of iterations must be numbers.")
		Return 1
	End If

	Dim retval(7), MBR, TA1, TA2, L1, L2, MaxD, solverOutput As Double
	retval = CalculateDoubleCatenary(V, H, L, tol, MaxIter)
	MBR = retval(0)
	TA1 = retval(1)
	TA2 = retval(2)
	L1 = retval(3)
	L2 = retval(4)
	MaxD = retval(5)
	solverOutput = retval(6)

	'fill in values in text boxes
	TextBoxTA1.Text = Format(TA1, "0.00")
	TextBoxTA2.Text = Format(TA2, "0.00")
	If RadioButtonTA1.Checked Then TextBoxTA.Text = Format(TA1, "0.00")
	If RadioButtonTA2.Checked Then TextBoxTA.Text = Format(TA2, "0.00")
	'apply correction if catenary is taut or otherwise
	If TA1 <= 90 Then
		TextBoxD.Text = Format(Math.Abs(MaxD), "0.00")
		TextBoxMBR.Text = Format(MBR, "0.00")
		TextBoxL1.Text = Format(L1, "0.00")
		TextBoxL2.Text = Format(L2, "0.00")
	ElseIf TA1 > 90 Then
		TextBoxD.Text = Format(V, "0.00")
		TextBoxMBR.Text = "Taut"
		TextBoxL1.Text = "Taut"
		TextBoxL2.Text = "Taut"
	End If

	TextBoxErr.Text = Format(solverOutput, "0.0E+0")
	If solverOutput >= tol Then
		TextBoxErr.ForeColor = Color.Red
		MsgBox("Solver not converged. Try increasing max. number of iterations or tolerance.")
	Else
		TextBoxErr.ForeColor = Color.Green
	End If

	'enables plot
	'this button is disabled when inputs parameters are changed
	ButtonPlot.Enabled = True

	Return 0
End Function
' =============================================================================
' =============================================================================
Private Function CalcTA()
	Dim V, H, TA, tol As Double
	Dim MaxIter As Integer
	V = Val(TextBoxV.Text)
	H = Val(TextBoxH.Text)
	TA = Val(TextBoxTA.text)
	MaxIter = Val(TextBoxMaxIter.Text)
	tol = Val(TextBoxTol.Text)
	'check inpu top angle
	'number must be positive and smaller than 
	'the straight line angle 
	'1deg extra is added to avoid numeric error
	Dim LimTA As Double
	LimTA = 180.0 / Math.PI * Math.Atan(V / H)
	If RadioButtonTA1.Checked Then LimTA = LimTA + 90 - 1
	If RadioButtonTA2.Checked Then LimTA = 90 - LimTA - 1
    
	If TA > LimTA Or TA <= 0 Then
		Dim str As String
		str = "Error: top angle must be greater than 0.00deg and smaller then " & Format(LimTA, "0.00") & "deg"
		MsgBox(str)
		Return 1
	End If

	'check tol
	If Not (IsNumeric(tol) Or IsNumeric(MaxIter)) Then
		MsgBox("Error. Tolerance must be a number.")
		Return 1
	End If

	Dim L As Double
	'note that tol is divided and MaxIter multiiplied by 10 
	'this is because results are very sensitive to TA
	Dim FlagTA1 As Boolean
	FlagTA1 = RadioButtonTA1.Checked
	L = AdjustTopAngle(TA, H, V, tol / 100.0, MaxIter * 100, FlagTA1)
	TextBoxL.Text = Format(L, "0.000000000000")

	Call MainCalc()

	Return 0
End Function
' =============================================================================
' =============================================================================
Function AdjustTopAngle( TA As Double,  H As Double,  V As Double,  tolerance As Double,  MaxIter As Integer,  FlagTA1 As Boolean) As Double
	'this function iterates the catenray solver to adjust the top angle
	' at the point with higher elevation (vessel)
	' this function returns the required length

	Dim deltaL, erro, L As Double
	Dim iter As Integer
	Dim retval As Array
	'solver parameters
	erro = 999
	deltaL = 30
	iter = 0
	'set initial guess for L
	L = H + V
	'calculate catenary for initial L
	retval = CalculateDoubleCatenary(V, H, L, tolerance, MaxIter)
	'get top angle - checking if TA1 or TA2 is being adjusted
	Dim TAindex As Integer
	If FlagTA1 Then TAindex = 1
	If Not FlagTA1 Then TAindex = 2
	Dim retTA As Double
	retTA = retval(TAindex)

	If retTA < TA Then deltaL = -deltaL
	If retTA > TA Then deltaL = deltaL
	Do
		iter = iter + 1
		L = L + deltaL
		retval = CalculateDoubleCatenary(V, H, L, tolerance, MaxIter)
		retTA = retval(TAindex)
		If Not (((retTA < TA) And (deltaL < 0)) Or ((retTA > TA) And (deltaL > 0))) Then
			deltaL = -0.5 * deltaL
		End If
		erro = Math.Abs(retTA - TA)
	Loop Until (erro < tolerance) Or (iter > MaxIter)

	Return L
End Function
' =============================================================================
' =============================================================================
Function CalculateDoubleCatenary( V,  H,  L,  tol,  MaxIter)
	Const Pi As Double = 3.14159265358979

	'call function to solve catenary factor (MBR)
	Dim a, solverOutput, retval(2) As Double
	retval = SolveCatenaryFactor(V, H, L, tol, MaxIter)
	a = retval(0)
	solverOutput = retval(1)
	'calculate catenary parameters
	Dim x1, x2, y1, y2, L1, L2, TA1, TA2, MaxD As Double
	'x values
	x1 = 0.5 * (a * Math.Log((L + V) / (L - V)) - H)
	x2 = 0.5 * (a * Math.Log((L + V) / (L - V)) + H)
	'y values
	y1 = a * cosh(x1 / a)
	y2 = a * cosh(x2 / a)
	' lengths
	L1 = -a * sinh(x1 / a)
	L2 = a * sinh(x2 / a)
	'top angles
	TA1 = 90 + 180 / Pi * Math.Atan(sinh(x1 / a))
	TA2 = 90 - 180 / Pi * Math.Atan(sinh(x2 / a))
	'maximum depth
	MaxD = max(y1, y2) - a

	'set the class properties
	SetPlotParameters(a, L, V, H)

	'return values
	Dim retfun = New Double() {a, TA1, TA2, L1, L2, MaxD, solverOutput}
	Return retfun
End Function
' =============================================================================
' =============================================================================
Function SolveCatenaryFactor(V As Double, H As Double, L As Double, tolerance As Double, MaxIter As Integer)
	'this function implements a Netwon-Raphson method to find roots of equations
	' this is used to find the catenary parameter a
	Dim a, fa, dfa As Double
	Dim iter As Integer
	'initial guess of catenary parameter
	a = 10.0
	iter = 0
	Do
		iter = iter + 1
		fa = 2 * a * sinh(H / 2 / a) - Math.Sqrt(L ^ 2 - V ^ 2)
		dfa = 2 * sinh(H / 2 / a) - H / a * cosh(H / 2 / a)
		a = Math.Abs(a - fa / dfa)
	Loop Until (iter > MaxIter) Or (Math.Abs(fa) < tolerance)

	'return catenary factor and solver final error
	Dim retfun = New Double() {a, Math.Abs(fa)}
	Return retfun
End Function
' =============================================================================
' =============================================================================




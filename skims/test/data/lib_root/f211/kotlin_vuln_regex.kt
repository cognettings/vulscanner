public class Test {

fun validate(request: javax.servlet.http.HttpServletRequest): Boolean {
    val regex = "(A+)+".toRegex()
    val input = request.getParameter("input")
    return input.matches(regex)  // Not-safe
}

fun validate(request: javax.servlet.http.HttpServletRequest): Boolean {
    val regex = "(A+)+".toRegex()
    val input = request.getParameter("input")
    return input.matches(Regex.escape(regex.pattern))  // Safe
}

fun validate(request: javax.servlet.http.HttpServletRequest): Boolean {
    val regex = Regex.escape("(A+)+")
    val input = request.getParameter("input")
    return input.matches(regex)  // Safe
}

fun validate(request: javax.servlet.http.HttpServletRequest): Boolean {
    val regex = "(A+)+".toRegex()
    val input = "hello"
    return input.matches(regex)  // Safe
}

fun validate(request: javax.servlet.http.HttpServletRequest): Boolean {
    val regex = "[a-zA-Z0-9]+".toRegex()
    val input = request.getParameter("input")
    return input.matches(regex)  // Safe
}

fun validate(personal_object: Any): Boolean {
    val regex = "(A+)+".toRegex()
    val input = personal_object.getParameter(1)
    return input.matches(regex)  // Safe
}

fun isValid(alphanumericField: String, cxt: ConstraintValidatorContext): Boolean {
    val pattern = "(A+)+".toRegex()
    return pattern.matches(alphanumericField)
}
}

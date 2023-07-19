import java.io.IOException
import javax.servlet.http.HttpServletRequest

class CookieController {
    fun unsafe(request: HttpServletRequest) {
        var input: String = request.getParameter("input") ?: ""
        var process = Runtime.getRuntime()
        var execution = process.exec(" ls ${input}", null, null)
        process.waitFor()
    }

    fun safe(request: HttpServletRequest) {
        var inputArray = request.getParameterValues("input") ?: emptyArray()
        var validatedInput: String = inputArray.filter(matches(Regex())).joinToString(" ")
        var process = ProcessBuilder("ls", validatedInput).start()
        process.waitFor()
    }
}

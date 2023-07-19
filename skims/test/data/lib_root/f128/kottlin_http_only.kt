public class CookieController {

    // unsafe: missing-httponly
    public fun setCookie(value: String, response: HttpServletResponse) {
        val cookie: Cookie = Cookie("cookie", value)
        response.addCookie(cookie)
    }
    // unsafe: missing-httponly
    public fun setSecureCookie(value: String, response: HttpServletResponse) {
        val cookie: Cookie = Cookie("cookie", value)
        cookie.setSecure(true)
        response.addCookie(cookie)
    }
    // unsafe: missing-httponly
    public fun explicitDisable(value: String, response: HttpServletResponse) {
        val cookie: Cookie = Cookie("cookie", value)
        cookie.setSecure(false)
        cookie.setHttpOnly(false)
        response.addCookie(cookie)
    }
    // safe- httponly setted
    public fun setSecureHttponlyCookie(value: String, response: HttpServletResponse ) {
        val cookie: Cookie = Cookie("cookie", value)
        cookie.setSecure(true)
        cookie.setHttpOnly(true)
        response.addCookie(cookie)
    }
}

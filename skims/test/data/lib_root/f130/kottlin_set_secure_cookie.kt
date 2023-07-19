public class CookieController {
    public fun setCookie(value: String, response: HttpServletResponse) {
        var cookie: Cookie = Cookie("cookie", value)
        response.addCookie(cookie)
    }

    public fun setSecureCookie(@RequestParam value: String, response: HttpServletResponse) {
       var cookie: Cookie = Cookie("cookie", value)
        cookie.setHttpOnly(true)
        response.addCookie(cookie)
    }

    public fun setSecureHttponlyCookie(@RequestParam value: String, response: HttpServletResponse) {
       var cookie: Cookie = Cookie("cookie", value)
        cookie.setSecure(true)
        cookie.setHttpOnly(true)
        response.addCookie(cookie)
    }

    public fun explicitDisable(@RequestParam value: String, response: HttpServletResponse) {
       var cookie: Cookie = Cookie("cookie", value)
        cookie.setSecure(false)
        cookie.setHttpOnly(false)
        response.addCookie(cookie)
    }
}

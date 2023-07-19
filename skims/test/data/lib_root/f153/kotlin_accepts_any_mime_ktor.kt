import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.http.*

val client = HttpClient {
    // Configuración del cliente
}

val response = client.get<String> {
    url("https://example.com/api/resource")
    headers {
        append(HttpHeaders.ContentType, "*/*")
        append(HttpHeaders.Authorization, "Bearer your_access_token_here")
    }
}

val response: HttpResponse = client.get("https://ktor.io/docs/welcome.html")

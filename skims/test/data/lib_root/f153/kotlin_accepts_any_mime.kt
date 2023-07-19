import java.net.URL
import java.net.HttpURLConnection
import java.io.BufferedReader
import java.io.InputStreamReader

val url = URL("https://example.com/api/resource")
val connection = url.openConnection() as HttpURLConnection
connection.requestMethod = "GET"

// Set headers
connection.setRequestProperty("Accept", "*/*")
connection.setRequestProperty("Authorization", "Bearer your_access_token_here")

// Make the request
val responseCode = connection.responseCode
val inputStream = if (responseCode == HttpURLConnection.HTTP_OK) {
    connection.inputStream
} else {
    connection.errorStream
}
val response = BufferedReader(InputStreamReader(inputStream)).use {
    it.readText()
}

package com.exampleweb.controller

import org.apache.http.Header
import org.apache.http.HttpResponse
import org.apache.http.client.HttpClient
import org.apache.http.client.methods.HttpGet
import org.apache.http.impl.client.DefaultHttpClient

public class WebCrawler {

    public fun crawl(args: Array<String>): Void {
        // ruleid: defaulthttpclient-is-deprecated
        val client: HttpClient = DefaultHttpClient()
        val request: HttpGet = HttpGet("http://google.com")
        val response: HttpResponse= client.execute(request)
    }

}

import org.xml.sax.InputSource
import org.xml.sax.SAXException
import org.xml.sax.helpers.DefaultHandler
import org.xml.sax.XMLReader
import org.xml.sax.helpers.XMLReaderFactory
import org.w3c.dom.Document
import org.w3c.dom.Node
import org.w3c.dom.NodeList
import org.w3c.dom.Element
import javax.xml.parsers.DocumentBuilder
import javax.xml.parsers.DocumentBuilderFactory
import javax.xml.parsers.SAXParserFactory
import javax.xml.parsers.SAXParser
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RequestMethod
import org.springframework.web.bind.annotation.RestController
import javax.servlet.http.HttpServletRequest
import org.slf4j.LoggerFactory
import java.io.StringReader

@RestController
class XXE {
    private val logger = LoggerFactory.getLogger(XXE::class.java)
    private val EXCEPT = "xxe except"

    @RequestMapping(value = ["/SAXParser/vuln"], method = [RequestMethod.POST])
    fun SAXParserVuln(request: HttpServletRequest): String {
        try {
            val body = WebUtils.getRequestBody(request)
            logger.info(body)
            // ruleid:owasp.java.xxe.javax.xml.parsers.SAXParserFactory
            val spf = SAXParserFactory.newInstance()
            val parser = spf.newSAXParser()
            parser.parse(InputSource(StringReader(body)), DefaultHandler())  // parse xml
            return "SAXParser xxe vuln code"
        } catch (e: Exception) {
            logger.error(e.toString())
            return EXCEPT
        }
    }


    @RequestMapping(value = ["/SAXParser/sec"], method = [RequestMethod.POST])
    fun SAXParserSec(request: HttpServletRequest) {
        try {
            val body = WebUtils.getRequestBody(request)
            logger.info(body)
            val spf = SAXParserFactory.newInstance()
            spf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true)
            spf.setFeature("http://xml.org/sax/features/external-general-entities", false)
            spf.setFeature("http://xml.org/sax/features/external-parameter-entities", false)
            val parser = spf.newSAXParser()
            parser.parse(InputSource(StringReader(body)), DefaultHandler())  // parse xml
        } catch (e: Exception) {
            logger.error(e.toString())
            return EXCEPT
        }
        return "SAXParser xxe security code"
    }

    @PostMapping("/xmlReader/vuln")
    fun xmlReaderVuln(request: HttpServletRequest): String {
        try {
            val body = WebUtils.getRequestBody(request)
            logger.info(body)
            // ruleid:owasp.java.xxe.org.xml.sax.XMLReader
            val xmlReader: XMLReader = XMLReaderFactory.createXMLReader()
            xmlReader.parse(InputSource(StringReader(body)))  // parse xml
            return "xmlReader xxe vuln code"
        } catch (e: Exception) {
            logger.error(e.toString())
            return EXCEPT
        }
    }


    @PostMapping("/XMLReader/sec")
    fun XMLReaderSec(request: HttpServletRequest): String {
    try {
        val body = WebUtils.getRequestBody(request)
        logger.info(body)
        val spf = SAXParserFactory.newInstance()
        val saxParser = spf.newSAXParser()
        val xmlReader = saxParser.xmlReader
        xmlReader.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true)
        xmlReader.setFeature("http://xml.org/sax/features/external-general-entities", false)
        xmlReader.setFeature("http://xml.org/sax/features/external-parameter-entities", false)
        xmlReader.parse(InputSource(StringReader(body)))
        } catch (e: Exception) {
            logger.error(e.toString())
            return EXCEPT
        }
        return "XMLReader xxe security code"
    }


    @RequestMapping(value = ["/DocumentBuilder/Sec"], method = [RequestMethod.POST])
    fun DocumentBuilderSec(request: HttpServletRequest): String {
        try {
            val body = WebUtils.getRequestBody(request)
            logger.info(body)
            // ruleid:owasp.java.xxe.javax.xml.parsers.DocumentBuilderFactory
            val dbf = DocumentBuilderFactory.newInstance()
            dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true)
            dbf.setFeature("http://xml.org/sax/features/external-general-entities", false)
            dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false)
            val db = dbf.newDocumentBuilder()
            val sr = StringReader(body)
            val is = InputSource(sr)
            db.parse(is) // parse xml
            sr.close()
        } catch (e: Exception) {
            logger.error(e.toString())
            return EXCEPT
        }
        return "DocumentBuilder xxe security code"
}

}

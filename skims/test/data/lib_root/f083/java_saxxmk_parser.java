import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.SAXParserFactory;
import javax.xml.parsers.SAXParser;

public class Test {

    public String sAXParserVuln(HttpServletRequest request) {
        String body = WebUtils.getRequestBody(request);
        SAXParserFactory spf = SAXParserFactory.newInstance();
        SAXParser parser = spf.newSAXParser();
        parser.parse(body);  // parse xml
    }

    public String sAXParserSec(HttpServletRequest request) {
        String body = WebUtils.getRequestBody(request);
        SAXParserFactory spf = SAXParserFactory.newInstance();
        spf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
        spf.setFeature("http://xml.org/sax/features/external-general-entities", false);
        spf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
        SAXParser parser = spf.newSAXParser();
        parser.parse(body);  // parse xml
    }

    public String xmlReaderVuln(HttpServletRequest request) {
        String body = WebUtils.getRequestBody(request);
        XMLReader xmlReader = XMLReaderFactory.createXMLReader();
        xmlReader.parse(body);  // parse xml
    }

    public String xMLReaderSec(HttpServletRequest request) {
        String body = WebUtils.getRequestBody(request);
        XMLReader xmlReader = XMLReaderFactory.createXMLReader();
        xmlReader.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
        xmlReader.setFeature("http://xml.org/sax/features/external-general-entities", false);
        xmlReader.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
        xmlReader.parse(body);
    }

    public String documentBuilderVuln(HttpServletRequest request) {
        String body = WebUtils.getRequestBody(request);
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        DocumentBuilder db = dbf.newDocumentBuilder();
        db.parse(body);  // parse xml
    }

    public String documentBuilderSec(HttpServletRequest request) {
        String body = WebUtils.getRequestBody(request);
        DocumentBuilderFactory df = DocumentBuilderFactory.newInstance();
        df.setAttribute(XMLConstants.ACCESS_EXTERNAL_DTD, "");
        df.setAttribute(XMLConstants.ACCESS_EXTERNAL_SCHEMA, "");
        DocumentBuilder db = df.newDocumentBuilder();
        db.parse(body);  // parse xml
    }
}

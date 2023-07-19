public class Test{
    public void insecure1(HttpServletRequest req) {
        String param1 = req.getParameter("param");
        Logger.info("Param1: " + param1);
    }

    public void insecure2(HttpServletRequest request){
        param =	request.getHeader("header");
        log.debug("Dangerous" + param);
    }

    public void insecure3(@PathParam(value = "collectorId") String collectorId) {
        log.debug("Something dangerous:" + collectorId);
    }

    public void safe(HttpServletRequest req) {
        String param2 = req.getParameter("param2");
        param2 = param2.replaceAll("[\n\r\t]", "_"); //Sanitize parameter
        logger.info("Param1: " + param2); //Safe
    }
}

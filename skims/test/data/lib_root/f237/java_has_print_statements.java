import System.out;

class Test {
    public static void unsafe_print(String[] args) {
        System.out.println(args);
        System.err.println(args);
        out.print(args);
        println("Have" + args.message + "concatenation");
    }
    public static void safe_print() {
        System.out.println("String Literal");
        System.err.println();
        // Custom made class with a print method. Not vulnerable
        dateTimeFormatter.print(new DateTime().withZone(DateTimeZone.forID(zoneId)));
    }
}

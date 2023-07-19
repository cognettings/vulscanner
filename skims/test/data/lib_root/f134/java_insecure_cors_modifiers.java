
@RestController
public class CategoryParametersController {

    private ParametersCategory parametersCategory;

		@CrossOrigin(origins = "*", methods = {RequestMethod.GET, RequestMethod.POST})
    @PostMapping("/test")
    public ResponseEntity<Response> getRoute() {
        return parametersCategory.generateResponse();
    }

		@CrossOrigin(origins = "mysite.com", methods = {RequestMethod.GET, RequestMethod.POST})
    public ResponseEntity<Response> getRoute() {
        return parametersCategory.generateResponse();
    }
}

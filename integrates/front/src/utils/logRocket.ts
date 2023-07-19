import LogRocket from "logrocket";

function initializeLogRocket(): void {
  LogRocket.init("3ktlih/integrates", {
    dom: {
      inputSanitizer: true,
    },
    network: {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      requestSanitizer: (request): any => {
        const protectedData = [
          "cardCvc",
          "compliance",
          "content",
          "credentials",
          "disambiguation",
          "groupContext",
          "inactivityPeriod",
          "nationalNumber",
          "urlId",
        ];
        const foundData = protectedData.find(
          (protectedKey): boolean | undefined => {
            const requestBody = request.body;

            return requestBody === undefined
              ? undefined
              : requestBody.includes(protectedKey);
          }
        );
        // If the request body contains any restricted word
        if (foundData ?? "") {
          /*
           * Scrub out the body
           * This will make the entire request dissapear from logRocket
           */
          return { ...request, body: "" };
        }

        return request;
      },
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      responseSanitizer: (response): any => {
        const protectedData = [
          "disambiguation",
          "evidence",
          "groupContext",
          "id",
          "maxAcceptanceSeverity",
          "nationalNumber",
          "sessionJwt",
          "where",
        ];
        const foundData = protectedData.find(
          (protectedKey): boolean | undefined => {
            const responseBody = response.body;

            return responseBody === undefined
              ? undefined
              : responseBody.includes(protectedKey);
          }
        );
        // If the response body contains any restricted word
        if (foundData ?? "") {
          // Scrub out the body
          return { ...response, body: "" };
        }

        return response;
      },
    },
  });
}

export { initializeLogRocket };

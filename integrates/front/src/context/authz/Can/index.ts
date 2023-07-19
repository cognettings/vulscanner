import { createContextualCan } from "@casl/react";

import { authzPermissionsContext } from "context/authz/config";

const can = createContextualCan(authzPermissionsContext.Consumer);

export { can as Can };

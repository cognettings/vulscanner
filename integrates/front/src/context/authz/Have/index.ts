import { createContextualCan } from "@casl/react";

import { authzGroupContext } from "context/authz/config";

const have = createContextualCan(authzGroupContext.Consumer);

export { have as Have };

import React from "react";

import {
  authzPermissionsContext,
  organizationLevelPermissions,
} from "context/authz/config";
import { OrganizationContent } from "scenes/Dashboard/containers/Organization-Content/OrganizationNav";

const Organization: React.FC = (): JSX.Element => {
  return (
    <authzPermissionsContext.Provider value={organizationLevelPermissions}>
      <OrganizationContent />
    </authzPermissionsContext.Provider>
  );
};

export { Organization };

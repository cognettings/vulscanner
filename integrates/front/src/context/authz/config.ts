import { PureAbility } from "@casl/ability";
import { createContext } from "react";

const groupAttributes = new PureAbility<string>();
const groupLevelPermissions = new PureAbility<string>();
const organizationLevelPermissions = new PureAbility<string>();
const userLevelPermissions = new PureAbility<string>();

const authzPermissionsContext = createContext(
  new PureAbility<string, unknown>()
);

const authzGroupContext = createContext(new PureAbility<string>());

export {
  groupAttributes,
  groupLevelPermissions,
  organizationLevelPermissions,
  userLevelPermissions,
  authzPermissionsContext,
  authzGroupContext,
};

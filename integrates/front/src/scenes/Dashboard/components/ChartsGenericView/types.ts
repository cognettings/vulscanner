declare type EntityType = "group" | "organization" | "portfolio";

interface IChartsGenericViewProps {
  bgChange: boolean;
  entity: EntityType;
  reportMode: boolean;
  subject: string;
}

export type { EntityType, IChartsGenericViewProps };

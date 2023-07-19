const About = [
  "about/introduction",
  {
    type: "category",
    label: "Compare",
    items: [
      "about/compare/introduction",
      {
        type: "category",
        label: "SAST",
        items: [
          "about/compare/sast",
          "about/compare/bishopfox",
          "about/compare/checkmarx",
          "about/compare/fortify",
          "about/compare/kiuwan",
          "about/compare/mend",
          "about/compare/netspi",
          "about/compare/qwiet",
          "about/compare/snyk",
          "about/compare/sonarqube",
          "about/compare/synopsys",
          "about/compare/tenable",
          "about/compare/trustit",
          "about/compare/veracode",
        ],
      },
      {
        type: "category",
        label: "DAST",
        items: [
          "about/compare/dast",
          "about/compare/acunetix",
          "about/compare/astra",
          "about/compare/bishopfox",
          "about/compare/checkmarx",
          "about/compare/crashtest-security",
          "about/compare/data-theorem",
          "about/compare/detectify",
          "about/compare/escape",
          "about/compare/fortify",
          "about/compare/immuniweb",
          "about/compare/intruder",
          "about/compare/nowsecure",
          "about/compare/prancer",
          "about/compare/probely",
          "about/compare/soos",
          "about/compare/stackhawk",
          "about/compare/synopsys",
          "about/compare/tenable",
          "about/compare/veracode",
        ],
      },
      {
        type: "category",
        label: "IAST",
        items: [
          "about/compare/iast",
          "about/compare/acunetix",
          "about/compare/checkmarx",
          "about/compare/synopsys",
          "about/compare/veracode",
        ],
      },
      {
        type: "category",
        label: "SCA",
        items: [
          "about/compare/sca",
          "about/compare/bishopfox",
          "about/compare/checkmarx",
          "about/compare/data-theorem",
          "about/compare/fortify",
          "about/compare/immuniweb",
          "about/compare/kiuwan",
          "about/compare/mend",
          "about/compare/nowsecure",
          "about/compare/prisma-cloud",
          "about/compare/qwiet",
          "about/compare/snyk",
          "about/compare/soos",
          "about/compare/synopsys",
          "about/compare/tenable",
          "about/compare/veracode",
        ],
      },
      {
        type: "category",
        label: "RE",
        items: ["about/compare/re", "about/compare/bishopfox"],
      },
      {
        type: "category",
        label: "SCR",
        items: ["about/compare/scr", "about/compare/bishopfox"],
      },
      {
        type: "category",
        label: "MPT",
        items: [
          "about/compare/mpt",
          "about/compare/align",
          "about/compare/astra",
          "about/compare/bishopfox",
          "about/compare/cyver",
          "about/compare/faraday",
          "about/compare/hackmetrix",
          "about/compare/immuniweb",
          "about/compare/intigriti",
          "about/compare/intruder",
          "about/compare/m3",
          "about/compare/netspi",
          "about/compare/nowsecure",
          "about/compare/s2",
          "about/compare/strike",
          "about/compare/synopsys",
          "about/compare/trustit",
          "about/compare/veracode",
          "about/compare/vulnscope",
          "about/compare/whitejaguars",
        ],
      },
      {
        type: "category",
        label: "CSPM",
        items: ["about/compare/cspm", "about/compare/prisma-cloud"],
      },
      {
        type: "category",
        label: "ASOC",
        items: [
          "about/compare/asoc",
          "about/compare/checkmarx",
          "about/compare/cider",
          "about/compare/dazz",
          "about/compare/faraday",
          "about/compare/kondukto",
          "about/compare/plextrac",
        ],
      },
      {
        type: "category",
        label: "ASPM",
        items: ["about/compare/aspm", "about/compare/bionic"],
      },
    ],
  },
  {
    type: "category",
    label: "Security",
    items: [
      "about/security/introduction",
      {
        type: "category",
        label: "Transparency",
        items: [
          "about/security/transparency/information-security-responsibility",
          "about/security/transparency/open-source",
          "about/security/transparency/hacking-our-technology",
          "about/security/transparency/public-incidents",
          "about/security/transparency/data-leakage-policy",
          "about/security/transparency/help-channel",
          "about/security/transparency/status-page",
        ],
      },
      {
        type: "category",
        label: "Confidentiality",
        items: [
          "about/security/confidentiality/encryption-rest",
          "about/security/confidentiality/encryption-transit",
          "about/security/confidentiality/personnel-nda",
          "about/security/confidentiality/hire-directly",
          "about/security/confidentiality/formatting-data",
        ],
      },
      {
        type: "category",
        label: "Authentication",
        items: [
          "about/security/authentication/clients",
          "about/security/authentication/internal",
          "about/security/authentication/password-policies",
        ],
      },
      {
        type: "category",
        label: "Authorization",
        items: [
          "about/security/authorization/clients",
          "about/security/authorization/internal",
          "about/security/authorization/secret-rotation",
          "about/security/authorization/access-revocation",
          "about/security/authorization/endpoint",
        ],
      },
      {
        type: "category",
        label: "Privacy",
        items: [
          "about/security/privacy/project-pseudonymization",
          "about/security/privacy/email-obfuscation",
          "about/security/privacy/secure-data-delivery",
          "about/security/privacy/unsubscribe-email",
          "about/security/privacy/transparent-use-cookies",
          "about/security/privacy/data-policies",
          "about/security/privacy/otr-messaging",
          "about/security/privacy/talent-time-tracking",
          "about/security/privacy/polygraph-tests",
        ],
      },
      {
        type: "category",
        label: "Non-repudiation",
        items: [
          "about/security/non-repudiation/everything-as-code",
          "about/security/non-repudiation/extensive-logs",
        ],
      },
      {
        type: "category",
        label: "Availability",
        items: [
          "about/security/availability/distributed-applications",
          "about/security/availability/distributed-firewall",
          "about/security/availability/everything-backed-up",
          "about/security/availability/recovery-objective",
          "about/security/availability/multiple-zones",
        ],
      },
      {
        type: "category",
        label: "Resilience",
        items: [
          "about/security/resilience/redundant-roles",
          "about/security/resilience/everything-decentralized",
          "about/security/resilience/equipment-telecommuting",
        ],
      },
      {
        type: "category",
        label: "Integrity",
        items: [
          "about/security/integrity/certified-cloud-provider",
          "about/security/integrity/certified-hackers",
          "about/security/integrity/hiring-process",
          "about/security/integrity/secure-emails",
          "about/security/integrity/developing-integrity",
          "about/security/integrity/static-website",
          "about/security/integrity/supply-chain-levels-for-software-artifacts",
        ],
      },
      "about/security/awareness",
      "about/security/detection",
    ],
  },
  "about/glossary",
  "about/faq",
];

const Criteria = [
  "criteria/introduction",
  {
    type: "category",
    label: "Compliance",
    items: [
      {
        type: "autogenerated",
        dirName: "criteria/Compliance",
      },
    ],
  },
  {
    type: "category",
    label: "Requirements",
    items: [
      "criteria/Requirements/introduction",
      {
        type: "category",
        label: "Credentials",
        items: [
          {
            type: "autogenerated",
            dirName: "criteria/Requirements/Credentials",
          },
        ],
      },
      {
        type: "category",
        label: "Authentication",
        items: [
          {
            type: "autogenerated",
            dirName: "criteria/Requirements/Authentication",
          },
        ],
      },
      {
        type: "category",
        label: "Authorization",
        items: [
          {
            type: "autogenerated",
            dirName: "criteria/Requirements/Authorization",
          },
        ],
      },
      {
        type: "category",
        label: "Session",
        items: [
          {
            type: "autogenerated",
            dirName: "criteria/Requirements/Session",
          },
        ],
      },
      {
        type: "category",
        label: "Legal",
        items: [
          {
            type: "autogenerated",
            dirName: "criteria/Requirements/Legal",
          },
        ],
      },
      {
        type: "category",
        label: "Privacy",
        items: [
          {
            type: "autogenerated",
            dirName: "criteria/Requirements/Privacy",
          },
        ],
      },
      {
        type: "category",
        label: "Data",
        items: [
          {
            type: "autogenerated",
            dirName: "criteria/Requirements/Data",
          },
        ],
      },
      {
        type: "category",
        label: "Source",
        items: [
          {
            type: "autogenerated",
            dirName: "criteria/Requirements/Source",
          },
        ],
      },
      {
        type: "category",
        label: "System",
        items: [
          {
            type: "autogenerated",
            dirName: "criteria/Requirements/System",
          },
        ],
      },
      {
        type: "category",
        label: "Files",
        items: [
          {
            type: "autogenerated",
            dirName: "criteria/Requirements/Files",
          },
        ],
      },
      {
        type: "category",
        label: "Logs",
        items: [
          {
            type: "autogenerated",
            dirName: "criteria/Requirements/Logs",
          },
        ],
      },
      {
        type: "category",
        label: "Emails",
        items: [
          {
            type: "autogenerated",
            dirName: "criteria/Requirements/Emails",
          },
        ],
      },
      {
        type: "category",
        label: "Services",
        items: [
          {
            type: "autogenerated",
            dirName: "criteria/Requirements/Services",
          },
        ],
      },
      {
        type: "category",
        label: "Certificates",
        items: [
          {
            type: "autogenerated",
            dirName: "criteria/Requirements/Certificates",
          },
        ],
      },
      {
        type: "category",
        label: "Cryptography",
        items: [
          {
            type: "autogenerated",
            dirName: "criteria/Requirements/Cryptography",
          },
        ],
      },
      {
        type: "category",
        label: "Architecture",
        items: [
          {
            type: "autogenerated",
            dirName: "criteria/Requirements/Architecture",
          },
        ],
      },
      {
        type: "category",
        label: "Networks",
        items: [
          {
            type: "autogenerated",
            dirName: "criteria/Requirements/Networks",
          },
        ],
      },
      {
        type: "category",
        label: "Virtualization",
        items: [
          {
            type: "autogenerated",
            dirName: "criteria/Requirements/Virtualization",
          },
        ],
      },
      {
        type: "category",
        label: "Devices",
        items: [
          {
            type: "autogenerated",
            dirName: "criteria/Requirements/Devices",
          },
        ],
      },
      {
        type: "category",
        label: "Social",
        items: [
          {
            type: "autogenerated",
            dirName: "criteria/Requirements/Social",
          },
        ],
      },
    ],
  },
  {
    type: "category",
    label: "Vulnerabilities",
    items: [
      {
        type: "autogenerated",
        dirName: "criteria/Vulnerabilities",
      },
    ],
  },
  {
    type: "category",
    label: "Fixes",
    items: [
      {
        type: "autogenerated",
        dirName: "criteria/Fixes",
      },
    ],
  },
];

const Development = [
  "development/intro",
  "development/philosophy",
  "development/governance",
  {
    type: "category",
    label: "Values",
    items: ["development/values/daily-progress", "development/values/quality"],
  },
  {
    type: "category",
    label: "Products",
    items: [
      "development/products/intro",
      "development/products/airs",
      {
        type: "category",
        label: "Common",
        items: [
          "development/products/common/intro",
          "development/products/common/ci",
          "development/products/common/cluster",
          "development/products/common/compute",
          "development/products/common/criteria",
          "development/products/common/dns",
          "development/products/common/status",
          "development/products/common/users",
          "development/products/common/vpc",
          "development/products/common/vpn",
        ],
      },
      "development/products/docs",
      "development/products/forces",
      {
        type: "category",
        label: "Integrates",
        items: [
          "development/products/integrates/intro",
          "development/products/integrates/security",
          "development/products/integrates/model",
          {
            type: "category",
            label: "Backend",
            items: [
              "development/products/integrates/backend/introduction",
              "development/products/integrates/backend/multitasking",
              "development/products/integrates/backend/graphql-api",
              "development/products/integrates/backend/migrations",
              {
                type: "category",
                label: "Testing",
                items: [
                  "development/products/integrates/backend/testing/introduction",
                  "development/products/integrates/backend/testing/unit-tests",
                ],
              },
            ],
          },
          "development/products/integrates/frontend",
        ],
      },
      "development/products/melts",
      {
        type: "category",
        label: "Observes",
        items: [
          "development/products/observes/intro",
          {
            type: "category",
            label: "Guidelines",
            items: [
              "development/products/observes/guidelines/analytics-conventions",
            ],
          },
          {
            type: "category",
            label: "ETLs",
            items: [
              "development/products/observes/etls/platform-etl",
              "development/products/observes/etls/zoho-etl",
            ],
          },
        ],
      },
      {
        type: "category",
        label: "Skims",
        items: [
          "development/products/skims/intro",
          {
            type: "category",
            label: "Guidelines",
            items: [
              {
                type: "category",
                label: "Lib module",
                items: [
                  "development/products/skims/guidelines/lib-module/dast",
                  "development/products/skims/guidelines/lib-module/sast",
                  "development/products/skims/guidelines/lib-module/sca",
                  "development/products/skims/guidelines/lib-module/root",
                ],
              },
            ],
          },
        ],
      },
      "development/products/sorts",
    ],
  },
  {
    type: "category",
    label: "Guidelines",
    items: [
      "development/guidelines/intro",
      "development/guidelines/licensing-and-copyright",
      {
        type: "category",
        label: "Writing",
        items: [
          "development/guidelines/writing/intro",
          {
            type: "category",
            label: "General",
            items: [
              "development/guidelines/writing/general/main",
              "development/guidelines/writing/general/capital-letters",
              "development/guidelines/writing/general/quotation-marks",
              "development/guidelines/writing/general/italics",
              "development/guidelines/writing/general/bold",
              "development/guidelines/writing/general/numbers",
              "development/guidelines/writing/general/others",
              "development/guidelines/writing/general/lists",
              "development/guidelines/writing/general/links",
            ],
          },
          {
            type: "category",
            label: "Blog",
            items: [
              "development/guidelines/writing/blog/main",
              "development/guidelines/writing/blog/code",
              "development/guidelines/writing/blog/metadata",
              "development/guidelines/writing/blog/submissions",
            ],
          },
          {
            type: "category",
            label: "Documentation",
            items: [
              "development/guidelines/writing/documentation/main",
              "development/guidelines/writing/documentation/metadata",
              "development/guidelines/writing/documentation/markdown",
            ],
          },
          "development/guidelines/writing/slb",
        ],
      },
    ],
  },
  {
    type: "category",
    label: "Stack",
    items: [
      "development/stack/introduction",
      {
        type: "category",
        label: "AWS",
        items: [
          "development/stack/aws/introduction",
          "development/stack/aws/batch",
          "development/stack/aws/cloudwatch",
          "development/stack/aws/cost-management",
          {
            type: "category",
            label: "DynamoDB",
            items: [
              "development/stack/aws/dynamodb/introduction",
              "development/stack/aws/dynamodb/patterns",
              "development/stack/aws/dynamodb/streams",
            ],
          },
          "development/stack/aws/ebs",
          "development/stack/aws/ec2",
          "development/stack/aws/eks",
          "development/stack/aws/elb",
          "development/stack/aws/iam",
          "development/stack/aws/kms",
          "development/stack/aws/lambda",
          "development/stack/aws/opensearch",
          "development/stack/aws/redshift",
          "development/stack/aws/s3",
          "development/stack/aws/sagemaker",
          "development/stack/aws/vpc",
          "development/stack/aws/vpn",
        ],
      },
      "development/stack/cloudflare",
      {
        type: "category",
        label: "Commitlint",
        items: [
          "development/stack/commitlint/introduction",
          {
            type: "category",
            label: "Syntax",
            items: [
              "development/stack/commitlint/syntax/commit",
              "development/stack/commitlint/syntax/merge-request",
            ],
          },
        ],
      },
      "development/stack/gitlab",
      "development/stack/gitlab-ci",
      "development/stack/kubernetes",
      "development/stack/makes",
      "development/stack/nix",
      "development/stack/okta",
      "development/stack/sops",
      "development/stack/terraform",
      "development/stack/ubiquiti",
    ],
  },
  "development/contributing",
  "development/faq",
];

const Technology = [
  "tech/introduction",
  {
    type: "category",
    label: "Platform",
    items: [
      "tech/platform/introduction",
      {
        type: "category",
        label: "Organization",
        items: [
          "tech/platform/organization/introduction",
          "tech/platform/organization/portfolios",
          "tech/platform/organization/members",
          "tech/platform/organization/policies",
          "tech/platform/organization/outside",
          "tech/platform/organization/credentials",
          'tech/platform/organization/compliance',
        ],
      },
      "tech/platform/user",
      "tech/platform/notifications",
      "tech/platform/subscription",
      "tech/platform/reattacks",
      {
        type: "category",
        label: "Support",
        items: [
          "tech/platform/support/talk-hacker",
          "tech/platform/support/chat",
          "tech/platform/support/demo",
          "tech/platform/support/tutorials",
          "tech/platform/support/email",
          "tech/platform/support/consulting",
        ],
      },
      {
        type: "category",
        label: "Groups",
        items: [
          "tech/platform/groups/introduction",
          "tech/platform/groups/group-view",
          "tech/platform/groups/vulnerabilities",
          "tech/platform/groups/reports",
          "tech/platform/groups/events",
          "tech/platform/groups/members",
          "tech/platform/groups/roles",
          "tech/platform/groups/authors",
          "tech/platform/groups/surface",
          {
            type: "category",
            label: "Scope",
            items: [
              "tech/platform/groups/scope/introduction",
              "tech/platform/groups/scope/roots",
              "tech/platform/groups/scope/exclusions",
              {
                type: "category",
                label: "Other sections",
                items: [
                  "tech/platform/groups/scope/other-sections/files",
                  "tech/platform/groups/scope/other-sections/creating-portfolios",
                  "tech/platform/groups/scope/other-sections/services",
                  "tech/platform/groups/scope/other-sections/information",
                  "tech/platform/groups/scope/other-sections/policies",
                  "tech/platform/groups/scope/other-sections/context",
                  "tech/platform/groups/scope/other-sections/agent",
                  "tech/platform/groups/scope/other-sections/unsubscribe",
                  "tech/platform/groups/scope/other-sections/delete",
                  "tech/platform/groups/scope/other-sections/aws-enrollment",
                ],
              },
            ],
          },
        ],
      },
      {
        type: "category",
        label: "Vulnerabilities",
        items: [
          {
            type: "category",
            label: "Management",
            items: [
              "tech/platform/vulnerabilities/management/introduction",
              "tech/platform/vulnerabilities/management/locations",
              "tech/platform/vulnerabilities/management/details",
              "tech/platform/vulnerabilities/management/vulnerability-assignment",
              "tech/platform/vulnerabilities/management/treatments",
              "tech/platform/vulnerabilities/management/to-do",
              "tech/platform/vulnerabilities/management/description",
              "tech/platform/vulnerabilities/management/severity",
              "tech/platform/vulnerabilities/management/evidence",
              "tech/platform/vulnerabilities/management/tracking",
              "tech/platform/vulnerabilities/management/records",
              "tech/platform/vulnerabilities/management/consulting",
              "tech/platform/vulnerabilities/management/zero-risk",
            ],
          },
        ],
      },
      {
        type: "category",
        label: "Analytics",
        items: [
          "tech/platform/analytics/introduction",
          "tech/platform/analytics/common",
          "tech/platform/analytics/organization",
          "tech/platform/analytics/portfolio",
          "tech/platform/analytics/groups",
          "tech/platform/analytics/reports",
          "tech/platform/analytics/chart-tools",
        ],
      },
    ],
  },
  {
    type: "category",
    label: "API",
    items: ["tech/api/api-token", "tech/api/basics"],
  },
  {
    type: "category",
    label: "Scanner",
    items: [
      "tech/scanner/introduction",
      {
        type: "category",
        label: "Getting Started",
        items: [
          "tech/scanner/plans/introduction",
          "tech/scanner/plans/saas",
          "tech/scanner/plans/foss",
        ],
      },
      {
        type: "category",
        label: "Standalone",
        items: [
          "tech/scanner/standalone/introduction",
          "tech/scanner/standalone/getting_started",
          "tech/scanner/standalone/options",
          {
            type: "category",
            label: "Configuration",
            items: [
              "tech/scanner/standalone/configuration/introduction",
              "tech/scanner/standalone/configuration/apk",
              "tech/scanner/standalone/configuration/dast",
              "tech/scanner/standalone/configuration/sast",
              "tech/scanner/standalone/configuration/sca",
            ],
          },
          "tech/scanner/standalone/format",
          {
            type: "category",
            label: "Output",
            items: [
              "tech/scanner/standalone/output/introduction",
              "tech/scanner/standalone/output/common",
              "tech/scanner/standalone/output/cli",
              "tech/scanner/standalone/output/csv",
            ],
          },
          "tech/scanner/standalone/casa",
        ],
      },
      "tech/scanner/benchmark",
      "tech/scanner/reproducibility",
      "tech/scanner/results",
      "tech/scanner/sca",
    ],
  },
  {
    type: "category",
    label: "CI Agent",
    items: ["tech/ci/introduction", "tech/ci/installation"],
  },
  "tech/ide",
];

const Plans = [
  "plans/introduction",
  {
    type: "category",
    label: "Machine",
    items: ["plans/machine/introduction"],
  },
  {
    type: "category",
    label: "Squad",
    items: ["plans/squad/counting-authors", "plans/squad/weapons"],
  },
  {
    type: "category",
    label: "SLA",
    items: [
      "plans/sla/introduction",
      "plans/sla/availability",
      "plans/sla/accuracy",
      "plans/sla/response",
      "plans/sla/false-negatives",
    ],
  },
];

const Talent = [
  "talent/introduction",
  "talent/diversity",
  {
    type: "category",
    label: "Everyone",
    items: [
      "talent/everyone/introduction",
      {
        type: "category",
        label: "Onboarding",
        items: [
          "talent/everyone/onboarding/introduction",
          "talent/everyone/onboarding/okta"
        ],
      }
    ],
  },
  {
    type: "category",
    label: "Engineering",
    items: [
      "talent/engineering/introduction",
      "talent/engineering/onboarding"
    ],
  },
  {
    type: "category",
    label: "Hacking",
    items: [
      "talent/hacking/introduction",
      {
        type: "category",
        label: "Onboarding",
        items: [
          "talent/hacking/onboarding/introduction",
          {
            type: "category",
            label: "Analysts",
            items: [
              "talent/hacking/onboarding/analysts/introduction",
              "talent/hacking/onboarding/analysts/new-vuln-description",
              "talent/hacking/onboarding/analysts/new-vuln-severity",
              "talent/hacking/onboarding/analysts/delete",
              "talent/hacking/onboarding/analysts/reporting-vulns",
              "talent/hacking/onboarding/analysts/creating-an-event",
              "talent/hacking/onboarding/analysts/vs-code",
            ],
          },
        ],
      },
    ],
  },
];

module.exports = {
  About: About,
  Criteria: Criteria,
  Technology: Technology,
  Plans: Plans,
  Development: Development,
  Talent: Talent,
};

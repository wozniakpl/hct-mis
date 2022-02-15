import { HouseholdNode } from '../../src/__generated__/graphql';

export const fakeHousehold = {
  id: 'SG91c2Vob2xkTm9kZTo3NjExNzM2Ny0yYWFiLTRmNTEtODUwOC1mMzBmODliYWUzYzE=',
  createdAt: '2022-02-07T11:46:27.904164',
  residenceStatus: 'REFUGEE',
  size: 4,
  totalCashReceived: '19318.00',
  totalCashReceivedUsd: '24697.00',
  currency: '',
  firstRegistrationDate: '2020-08-22T00:00:00',
  lastRegistrationDate: '2020-08-22T00:00:00',
  status: 'ACTIVE',
  sanctionListPossibleMatch: false,
  sanctionListConfirmedMatch: false,
  hasDuplicates: false,
  unicefId: 'HH-20-0000.0001',
  flexFields: { months_displaced_h_f: 12, difficulty_breathing_h_f: '1' },
  unhcrId: '',
  geopoint: { type: 'Point', coordinates: [70.210209, 172.085021] },
  village: '',
  adminAreaTitle: 'Achin',
  admin1: {
    id: 'QWRtaW5BcmVhTm9kZTo3NmU0MDRlYS1mYjVhLTRkMDktODVkMS1hNTA3MjU4OThmNzk=',
    title: 'Nangarhar',
    level: 1,
    pCode: 'AF06',
    __typename: 'AdminAreaNode',
  },
  admin2: {
    id: 'QWRtaW5BcmVhTm9kZTpkMTU1MjA2MC05NWExLTQ5ODItODY3MC0yMzg4NDcxZDUxYTA=',
    title: 'Achin',
    level: 2,
    pCode: 'AF0617',
    __typename: 'AdminAreaNode',
  },
  headOfHousehold: {
    id: 'SW5kaXZpZHVhbE5vZGU6ZjVmMzgwN2ItYTBjOS00Mjk0LTg0Y2QtNDhkMjllMjZhODU3',
    fullName: 'Agata Kowalska',
    givenName: 'Agata',
    familyName: 'Kowalska',
    __typename: 'IndividualNode',
  },
  address: '938 Luna Cliffs Apt. 551\nJameschester, SC 24934',
  individuals: {
    totalCount: 3,
    __typename: 'IndividualNodeConnection',
    edges: [
      {
        node: {
          id:
            'SW5kaXZpZHVhbE5vZGU6YTI2ODYyMTAtYjBhNi00NTI1LWI4YTAtYTFmY2FlMWIwMjE5',
          age: 80,
          lastRegistrationDate: '1942-12-12',
          createdAt: '2022-02-07T11:46:27.919328',
          updatedAt: '2022-02-07T11:46:27.919378',
          fullName: 'Alicja Kowalska',
          sex: 'FEMALE',
          unicefId: 'IND-42-0000.0001',
          birthDate: '1941-08-26',
          maritalStatus: 'MARRIED',
          phoneNo: '0048503123555',
          sanctionListPossibleMatch: false,
          sanctionListConfirmedMatch: false,
          deduplicationGoldenRecordStatus: 'UNIQUE',
          sanctionListLastCheck: '2022-02-08T07:35:39.718645',
          role: 'ALTERNATE',
          relationship: 'NON_BENEFICIARY',
          status: 'ACTIVE',
          documents: {
            edges: [
              {
                node: {
                  id:
                    'RG9jdW1lbnROb2RlOjYzYjM1NzA4LWZhNzYtNDExMy1iMmIyLWE5MGU1YWE2OTZiOA==',
                  country: 'Poland',
                  documentNumber: 'BSH221315',
                  photo: null,
                  type: {
                    country: 'Poland',
                    label: 'National ID',
                    type: 'NATIONAL_ID',
                    countryIso3: 'POL',
                    __typename: 'DocumentTypeNode',
                  },
                  __typename: 'DocumentNode',
                },
                __typename: 'DocumentNodeEdge',
              },
            ],
            __typename: 'DocumentNodeConnection',
          },
          identities: {
            edges: [],
            __typename: 'IndividualIdentityNodeConnection',
          },
          household: null,
          __typename: 'IndividualNode',
        },
        __typename: 'IndividualNodeEdge',
      },
      {
        node: {
          id:
            'SW5kaXZpZHVhbE5vZGU6ZjVmMzgwN2ItYTBjOS00Mjk0LTg0Y2QtNDhkMjllMjZhODU3',
          age: 58,
          lastRegistrationDate: '1988-06-15',
          createdAt: '2022-02-07T11:46:27.922172',
          updatedAt: '2022-02-07T11:46:27.922194',
          fullName: 'Agata Kowalska',
          sex: 'FEMALE',
          unicefId: 'IND-88-0000.0005',
          birthDate: '1964-01-10',
          maritalStatus: 'SINGLE',
          phoneNo: '0048875012932',
          sanctionListPossibleMatch: false,
          sanctionListConfirmedMatch: false,
          deduplicationGoldenRecordStatus: 'UNIQUE',
          sanctionListLastCheck: '2022-02-08T07:35:39.718645',
          role: 'PRIMARY',
          relationship: 'HEAD',
          status: 'ACTIVE',
          documents: {
            edges: [
              {
                node: {
                  id:
                    'RG9jdW1lbnROb2RlOjg5ZTE2YzQ4LWYwOWMtNGVlMC1iYWYyLTZiOWFiYjZjMjVlNg==',
                  country: 'Poland',
                  documentNumber: 'TSH221375',
                  photo: null,
                  type: {
                    country: 'Poland',
                    label: 'National ID',
                    type: 'NATIONAL_ID',
                    countryIso3: 'POL',
                    __typename: 'DocumentTypeNode',
                  },
                  __typename: 'DocumentNode',
                },
                __typename: 'DocumentNodeEdge',
              },
            ],
            __typename: 'DocumentNodeConnection',
          },
          identities: {
            edges: [],
            __typename: 'IndividualIdentityNodeConnection',
          },
          household: {
            id:
              'SG91c2Vob2xkTm9kZTo3NjExNzM2Ny0yYWFiLTRmNTEtODUwOC1mMzBmODliYWUzYzE=',
            unicefId: 'HH-20-0000.0001',
            status: 'ACTIVE',
            admin1: {
              id:
                'QWRtaW5BcmVhTm9kZTo3NmU0MDRlYS1mYjVhLTRkMDktODVkMS1hNTA3MjU4OThmNzk=',
              title: 'Nangarhar',
              level: 1,
              pCode: 'AF06',
              __typename: 'AdminAreaNode',
            },
            admin2: {
              id:
                'QWRtaW5BcmVhTm9kZTpkMTU1MjA2MC05NWExLTQ5ODItODY3MC0yMzg4NDcxZDUxYTA=',
              title: 'Achin',
              level: 2,
              pCode: 'AF0617',
              __typename: 'AdminAreaNode',
            },
            programs: {
              edges: [
                {
                  node: {
                    id:
                      'UHJvZ3JhbU5vZGU6YzRkNTY1N2QtMWEyOS00NmUxLTgxOTAtZGY3Zjg1YTBkMmVm',
                    name:
                      'Surface campaign practice actually about about will what.',
                    __typename: 'ProgramNode',
                  },
                  __typename: 'ProgramNodeEdge',
                },
              ],
              __typename: 'ProgramNodeConnection',
            },
            __typename: 'HouseholdNode',
          },
          __typename: 'IndividualNode',
        },
        __typename: 'IndividualNodeEdge',
      },
      {
        node: {
          id:
            'SW5kaXZpZHVhbE5vZGU6YWI5YWZhNzUtMTg0Yy00NDIxLWJmMGUtNTIzZGUxNWMyOGFm',
          age: 22,
          lastRegistrationDate: '1988-06-15',
          createdAt: '2022-02-07T11:46:27.922555',
          updatedAt: '2022-02-07T11:46:27.922577',
          fullName: 'Angela Kowalska',
          sex: 'FEMALE',
          unicefId: 'IND-88-0000.0006',
          birthDate: '2000-01-10',
          maritalStatus: 'SINGLE',
          phoneNo: '0048724467321',
          sanctionListPossibleMatch: false,
          sanctionListConfirmedMatch: false,
          deduplicationGoldenRecordStatus: 'UNIQUE',
          sanctionListLastCheck: '2022-02-08T07:35:39.718645',
          role: 'NO_ROLE',
          relationship: 'BROTHER_SISTER',
          status: 'ACTIVE',
          documents: {
            edges: [
              {
                node: {
                  id:
                    'RG9jdW1lbnROb2RlOjM0NjQwYmU2LTc4ZTgtNDc2Zi1iYWM2LWFjOTIwZTIwYmExOQ==',
                  country: 'Poland',
                  documentNumber: 'CSH221395',
                  photo: null,
                  type: {
                    country: 'Poland',
                    label: 'National ID',
                    type: 'NATIONAL_ID',
                    countryIso3: 'POL',
                    __typename: 'DocumentTypeNode',
                  },
                  __typename: 'DocumentNode',
                },
                __typename: 'DocumentNodeEdge',
              },
            ],
            __typename: 'DocumentNodeConnection',
          },
          identities: {
            edges: [],
            __typename: 'IndividualIdentityNodeConnection',
          },
          household: {
            id:
              'SG91c2Vob2xkTm9kZTo3NjExNzM2Ny0yYWFiLTRmNTEtODUwOC1mMzBmODliYWUzYzE=',
            unicefId: 'HH-20-0000.0001',
            status: 'ACTIVE',
            admin1: {
              id:
                'QWRtaW5BcmVhTm9kZTo3NmU0MDRlYS1mYjVhLTRkMDktODVkMS1hNTA3MjU4OThmNzk=',
              title: 'Nangarhar',
              level: 1,
              pCode: 'AF06',
              __typename: 'AdminAreaNode',
            },
            admin2: {
              id:
                'QWRtaW5BcmVhTm9kZTpkMTU1MjA2MC05NWExLTQ5ODItODY3MC0yMzg4NDcxZDUxYTA=',
              title: 'Achin',
              level: 2,
              pCode: 'AF0617',
              __typename: 'AdminAreaNode',
            },
            programs: {
              edges: [
                {
                  node: {
                    id:
                      'UHJvZ3JhbU5vZGU6YzRkNTY1N2QtMWEyOS00NmUxLTgxOTAtZGY3Zjg1YTBkMmVm',
                    name:
                      'Surface campaign practice actually about about will what.',
                    __typename: 'ProgramNode',
                  },
                  __typename: 'ProgramNodeEdge',
                },
              ],
              __typename: 'ProgramNodeConnection',
            },
            __typename: 'HouseholdNode',
          },
          __typename: 'IndividualNode',
        },
        __typename: 'IndividualNodeEdge',
      },
    ],
  },
  programs: {
    edges: [
      {
        node: {
          id:
            'UHJvZ3JhbU5vZGU6YzRkNTY1N2QtMWEyOS00NmUxLTgxOTAtZGY3Zjg1YTBkMmVm',
          name: 'Surface campaign practice actually about about will what.',
          __typename: 'ProgramNode',
        },
        __typename: 'ProgramNodeEdge',
      },
    ],
    __typename: 'ProgramNodeConnection',
  },
  __typename: 'HouseholdNode',
  activeIndividualsCount: 2,
  countryOrigin: 'San Marino',
  country: 'Isle of Man',
  femaleAgeGroup05Count: 0,
  femaleAgeGroup611Count: 0,
  femaleAgeGroup1217Count: 0,
  femaleAgeGroup1859Count: null,
  femaleAgeGroup60Count: null,
  pregnantCount: null,
  maleAgeGroup05Count: 0,
  maleAgeGroup611Count: 0,
  maleAgeGroup1217Count: 0,
  maleAgeGroup1859Count: null,
  maleAgeGroup60Count: null,
  femaleAgeGroup05DisabledCount: 0,
  femaleAgeGroup611DisabledCount: 0,
  femaleAgeGroup1217DisabledCount: 0,
  femaleAgeGroup1859DisabledCount: null,
  femaleAgeGroup60DisabledCount: null,
  maleAgeGroup05DisabledCount: 0,
  maleAgeGroup611DisabledCount: 0,
  maleAgeGroup1217DisabledCount: 0,
  maleAgeGroup1859DisabledCount: null,
  maleAgeGroup60DisabledCount: null,
  fchildHoh: false,
  childHoh: false,
  start: null,
  deviceid: '',
  orgNameEnumerator: 'UNICEF',
  returnee: false,
  nameEnumerator: 'Harley Rawlings',
  lastSyncAt: null,
  consentSharing: [
    'HUMANITARIAN_PARTNER',
    'PRIVATE_PARTNER',
    'GOVERNMENT_PARTNER',
    'UNICEF',
    '',
  ],
  orgEnumerator: 'UNICEF',
  updatedAt: '2022-02-07T11:46:27.904196',
  consent: true,
  registrationDataImport: {
    name: 'romaniaks',
    dataSource: 'XLS',
    importDate: '2022-02-07T11:45:52.336512',
    importedBy: {
      firstName: 'Maciej',
      lastName: 'Szewczyk',
      email: 'fffff@gmail.com',
      username: 'maciej.szewczyk@tivix.com',
      __typename: 'UserNode',
    },
    __typename: 'RegistrationDataImportNode',
  },
  paymentRecords: {
    edges: [
      {
        node: {
          id:
            'UGF5bWVudFJlY29yZE5vZGU6ZGViY2E5YWQtNzBhNS00MDk2LTkxYjctMmU3MGRkZjRhYmMy',
          fullName: 'Brian Morgan',
          cashPlan: {
            id:
              'Q2FzaFBsYW5Ob2RlOjI1ZTNkODA0LTAzMzEtNDhkOC1iYTk2LWVmZjEzYmU3ZDdiYQ==',
            totalPersonsCovered: 2,
            program: {
              id:
                'UHJvZ3JhbU5vZGU6YzRkNTY1N2QtMWEyOS00NmUxLTgxOTAtZGY3Zjg1YTBkMmVm',
              name: 'Surface campaign practice actually about about will what.',
              __typename: 'ProgramNode',
            },
            totalDeliveredQuantity: 88608141.04,
            assistanceMeasurement: 'Vietnamese đồng',
            __typename: 'CashPlanNode',
          },
          __typename: 'PaymentRecordNode',
        },
        __typename: 'PaymentRecordNodeEdge',
      },
      {
        node: {
          id:
            'UGF5bWVudFJlY29yZE5vZGU6ODZhZmQ4NjQtYmNlNS00N2Q0LWE5YmEtYzlkZTVjZGYwMDJm',
          fullName: 'Jennifer Weber MD',
          cashPlan: {
            id:
              'Q2FzaFBsYW5Ob2RlOjI1ZTNkODA0LTAzMzEtNDhkOC1iYTk2LWVmZjEzYmU3ZDdiYQ==',
            totalPersonsCovered: 2,
            program: {
              id:
                'UHJvZ3JhbU5vZGU6YzRkNTY1N2QtMWEyOS00NmUxLTgxOTAtZGY3Zjg1YTBkMmVm',
              name: 'Surface campaign practice actually about about will what.',
              __typename: 'ProgramNode',
            },
            totalDeliveredQuantity: 88608141.04,
            assistanceMeasurement: 'Vietnamese đồng',
            __typename: 'CashPlanNode',
          },
          __typename: 'PaymentRecordNode',
        },
        __typename: 'PaymentRecordNodeEdge',
      },
      {
        node: {
          id:
            'UGF5bWVudFJlY29yZE5vZGU6ZDJiMTAzNjUtMDBlMy00ZjMyLTg2MTUtN2UyMDUxM2YyZmQ1',
          fullName: 'Jason Jacobs',
          cashPlan: {
            id:
              'Q2FzaFBsYW5Ob2RlOmUwZGUxMGMyLTMxNWUtNDhjYS1hNDU5LWM2NTQyZDc1MmJlNw==',
            totalPersonsCovered: 3,
            program: {
              id:
                'UHJvZ3JhbU5vZGU6YzRkNTY1N2QtMWEyOS00NmUxLTgxOTAtZGY3Zjg1YTBkMmVm',
              name: 'Surface campaign practice actually about about will what.',
              __typename: 'ProgramNode',
            },
            totalDeliveredQuantity: 2058088.16,
            assistanceMeasurement: 'Nigerian naira',
            __typename: 'CashPlanNode',
          },
          __typename: 'PaymentRecordNode',
        },
        __typename: 'PaymentRecordNodeEdge',
      },
      {
        node: {
          id:
            'UGF5bWVudFJlY29yZE5vZGU6NGM4ZGYyYjQtNTI5Ni00YmJhLTgzOTQtNGNkMGI0M2MyZjEy',
          fullName: 'Micheal Massey',
          cashPlan: {
            id:
              'Q2FzaFBsYW5Ob2RlOmUwZGUxMGMyLTMxNWUtNDhjYS1hNDU5LWM2NTQyZDc1MmJlNw==',
            totalPersonsCovered: 3,
            program: {
              id:
                'UHJvZ3JhbU5vZGU6YzRkNTY1N2QtMWEyOS00NmUxLTgxOTAtZGY3Zjg1YTBkMmVm',
              name: 'Surface campaign practice actually about about will what.',
              __typename: 'ProgramNode',
            },
            totalDeliveredQuantity: 2058088.16,
            assistanceMeasurement: 'Nigerian naira',
            __typename: 'CashPlanNode',
          },
          __typename: 'PaymentRecordNode',
        },
        __typename: 'PaymentRecordNodeEdge',
      },
      {
        node: {
          id:
            'UGF5bWVudFJlY29yZE5vZGU6YzZlYzMwMDUtZWUzZC00MjI3LWI2YzctM2MxZDcxNzQwYTA4',
          fullName: 'Stephen Smith',
          cashPlan: {
            id:
              'Q2FzaFBsYW5Ob2RlOjkyZDc0NTRiLWVlNWEtNDM3Yy1hNTJiLWVmZjI0NGQyZjYyZA==',
            totalPersonsCovered: 4,
            program: {
              id:
                'UHJvZ3JhbU5vZGU6YzRkNTY1N2QtMWEyOS00NmUxLTgxOTAtZGY3Zjg1YTBkMmVm',
              name: 'Surface campaign practice actually about about will what.',
              __typename: 'ProgramNode',
            },
            totalDeliveredQuantity: 17600499.7,
            assistanceMeasurement: 'Vietnamese đồng',
            __typename: 'CashPlanNode',
          },
          __typename: 'PaymentRecordNode',
        },
        __typename: 'PaymentRecordNodeEdge',
      },
      {
        node: {
          id:
            'UGF5bWVudFJlY29yZE5vZGU6OThjMzVmNzEtOWY1Ni00NjMwLWJjNWItOWFlODkxNmU0OThh',
          fullName: 'Jessica Thornton',
          cashPlan: {
            id:
              'Q2FzaFBsYW5Ob2RlOjkyZDc0NTRiLWVlNWEtNDM3Yy1hNTJiLWVmZjI0NGQyZjYyZA==',
            totalPersonsCovered: 4,
            program: {
              id:
                'UHJvZ3JhbU5vZGU6YzRkNTY1N2QtMWEyOS00NmUxLTgxOTAtZGY3Zjg1YTBkMmVm',
              name: 'Surface campaign practice actually about about will what.',
              __typename: 'ProgramNode',
            },
            totalDeliveredQuantity: 17600499.7,
            assistanceMeasurement: 'Vietnamese đồng',
            __typename: 'CashPlanNode',
          },
          __typename: 'PaymentRecordNode',
        },
        __typename: 'PaymentRecordNodeEdge',
      },
      {
        node: {
          id:
            'UGF5bWVudFJlY29yZE5vZGU6MDVkNDkyNjctMjhhNy00ZDU5LTllOTgtYmRjMjJjNGRlNzg3',
          fullName: 'Bethany Rodriguez',
          cashPlan: {
            id:
              'Q2FzaFBsYW5Ob2RlOjkyZDc0NTRiLWVlNWEtNDM3Yy1hNTJiLWVmZjI0NGQyZjYyZA==',
            totalPersonsCovered: 4,
            program: {
              id:
                'UHJvZ3JhbU5vZGU6YzRkNTY1N2QtMWEyOS00NmUxLTgxOTAtZGY3Zjg1YTBkMmVm',
              name: 'Surface campaign practice actually about about will what.',
              __typename: 'ProgramNode',
            },
            totalDeliveredQuantity: 17600499.7,
            assistanceMeasurement: 'Vietnamese đồng',
            __typename: 'CashPlanNode',
          },
          __typename: 'PaymentRecordNode',
        },
        __typename: 'PaymentRecordNodeEdge',
      },
      {
        node: {
          id:
            'UGF5bWVudFJlY29yZE5vZGU6MjEwMWVmNmUtODZjYi00MDI2LWI1MmUtMzdjMmQyNWQzZmE0',
          fullName: 'Melanie Haley MD',
          cashPlan: {
            id:
              'Q2FzaFBsYW5Ob2RlOjkyZDc0NTRiLWVlNWEtNDM3Yy1hNTJiLWVmZjI0NGQyZjYyZA==',
            totalPersonsCovered: 4,
            program: {
              id:
                'UHJvZ3JhbU5vZGU6YzRkNTY1N2QtMWEyOS00NmUxLTgxOTAtZGY3Zjg1YTBkMmVm',
              name: 'Surface campaign practice actually about about will what.',
              __typename: 'ProgramNode',
            },
            totalDeliveredQuantity: 17600499.7,
            assistanceMeasurement: 'Vietnamese đồng',
            __typename: 'CashPlanNode',
          },
          __typename: 'PaymentRecordNode',
        },
        __typename: 'PaymentRecordNodeEdge',
      },
      {
        node: {
          id:
            'UGF5bWVudFJlY29yZE5vZGU6NWRhNGFjZjYtYjc5My00ZThkLWJlYzktMDRiMTI4ZTJkOGNi',
          fullName: 'Greg Cohen',
          cashPlan: {
            id:
              'Q2FzaFBsYW5Ob2RlOjkyZDc0NTRiLWVlNWEtNDM3Yy1hNTJiLWVmZjI0NGQyZjYyZA==',
            totalPersonsCovered: 4,
            program: {
              id:
                'UHJvZ3JhbU5vZGU6YzRkNTY1N2QtMWEyOS00NmUxLTgxOTAtZGY3Zjg1YTBkMmVm',
              name: 'Surface campaign practice actually about about will what.',
              __typename: 'ProgramNode',
            },
            totalDeliveredQuantity: 17600499.7,
            assistanceMeasurement: 'Vietnamese đồng',
            __typename: 'CashPlanNode',
          },
          __typename: 'PaymentRecordNode',
        },
        __typename: 'PaymentRecordNodeEdge',
      },
    ],
    __typename: 'PaymentRecordNodeConnection',
  },
  programsWithDeliveredQuantity: [
    {
      id: 'c4d5657d-1a29-46e1-8190-df7f85a0d2ef',
      name: 'Surface campaign practice actually about about will what.',
      quantity: [
        {
          totalDeliveredQuantity: '3251.00',
          currency: 'USD',
          __typename: 'DeliveredQuantityNode',
        },
        {
          totalDeliveredQuantity: '3048.00',
          currency: 'BAM',
          __typename: 'DeliveredQuantityNode',
        },
        {
          totalDeliveredQuantity: '2959.00',
          currency: 'BND',
          __typename: 'DeliveredQuantityNode',
        },
        {
          totalDeliveredQuantity: '4904.00',
          currency: 'ISK',
          __typename: 'DeliveredQuantityNode',
        },
        {
          totalDeliveredQuantity: '2505.00',
          currency: 'LSL',
          __typename: 'DeliveredQuantityNode',
        },
        {
          totalDeliveredQuantity: '115.00',
          currency: 'TMT',
          __typename: 'DeliveredQuantityNode',
        },
        {
          totalDeliveredQuantity: '484.00',
          currency: 'UAH',
          __typename: 'DeliveredQuantityNode',
        },
        {
          totalDeliveredQuantity: '2073.00',
          currency: 'UGX',
          __typename: 'DeliveredQuantityNode',
        },
        {
          totalDeliveredQuantity: '895.00',
          currency: 'UZS',
          __typename: 'DeliveredQuantityNode',
        },
        {
          totalDeliveredQuantity: '2335.00',
          currency: 'YER',
          __typename: 'DeliveredQuantityNode',
        },
      ],
      __typename: 'ProgramsWithDeliveredQuantityNode',
    },
  ],
} as HouseholdNode;

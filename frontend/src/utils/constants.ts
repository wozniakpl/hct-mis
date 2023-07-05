import {
  PaymentPlanBackgroundActionStatus,
  PaymentPlanStatus,
  ProgramStatus,
  TargetPopulationStatus,
} from '../__generated__/graphql';

export const TARGETING_STATES = {
  NONE: 'None',
  [TargetPopulationStatus.Open]: 'Open',
  [TargetPopulationStatus.Locked]: 'Locked',
  [TargetPopulationStatus.ReadyForCashAssist]: 'Ready For Cash Assist',
  [TargetPopulationStatus.ReadyForPaymentModule]: 'Ready For Payment Module',
  [TargetPopulationStatus.Processing]: 'Processing',
  [TargetPopulationStatus.SteficonWait]: 'Entitlement Formula Wait',
  [TargetPopulationStatus.SteficonRun]: 'Entitlement Formula Run',
  [TargetPopulationStatus.SteficonCompleted]: 'Entitlement Formula Completed',
  [TargetPopulationStatus.SteficonError]: 'Entitlement Formula Error',
  [TargetPopulationStatus.Assigned]: 'Assigned',
};

export const PROGRAM_STATES = {
  [ProgramStatus.Active]: 'Active',
  [ProgramStatus.Draft]: 'Draft',
  [ProgramStatus.Finished]: 'Finished',
};

export const PAYMENT_PLAN_STATES = {
  [PaymentPlanStatus.Open]: 'Open',
  [PaymentPlanStatus.Locked]: 'Locked',
  [PaymentPlanStatus.LockedFsp]: 'FSP Locked',
  [PaymentPlanStatus.InApproval]: 'In Approval',
  [PaymentPlanStatus.InAuthorization]: 'In Authorization',
  [PaymentPlanStatus.InReview]: 'In Review',
  [PaymentPlanStatus.Accepted]: 'Accepted',
  [PaymentPlanStatus.Finished]: 'Finished',
};

export const PAYMENT_PLAN_BACKGROUND_ACTION_STATES = {
  [PaymentPlanBackgroundActionStatus.RuleEngineRun]: 'Entitlement Formula Run',
  [PaymentPlanBackgroundActionStatus.RuleEngineError]:
    'Entitlement Formula Error',
  [PaymentPlanBackgroundActionStatus.XlsxExporting]: 'XLSX Exporting',
  [PaymentPlanBackgroundActionStatus.XlsxExportError]: 'XLSX Export Error',
  [PaymentPlanBackgroundActionStatus.XlsxImportingEntitlements]:
    'XLSX Importing Entitlements',
  [PaymentPlanBackgroundActionStatus.XlsxImportingReconciliation]:
    'XLSX Importing Reconciliation',
  [PaymentPlanBackgroundActionStatus.XlsxImportError]: 'XLSX Import Error',
};

export const PAYMENT_PLAN_ACTIONS = {
  LOCK: 'LOCK',
  UNLOCK: 'UNLOCK',
  SEND_FOR_APPROVAL: 'SEND_FOR_APPROVAL',
  APPROVE: 'APPROVE',
  AUTHORIZE: 'AUTHORIZE',
  REVIEW: 'REVIEW',
  REJECT: 'REJECT',
};

export const GRIEVANCE_TICKET_STATES = {
  NEW: 1,
  ASSIGNED: 2,
  IN_PROGRESS: 3,
  ON_HOLD: 4,
  FOR_APPROVAL: 5,
  CLOSED: 6,
};

export const GRIEVANCE_CATEGORIES = {
  PAYMENT_VERIFICATION: '1',
  DATA_CHANGE: '2',
  SENSITIVE_GRIEVANCE: '3',
  GRIEVANCE_COMPLAINT: '4',
  NEGATIVE_FEEDBACK: '5',
  REFERRAL: '6',
  POSITIVE_FEEDBACK: '7',
  DEDUPLICATION: '8',
  SYSTEM_FLAGGING: '9',
};

export const GRIEVANCE_ISSUE_TYPES = {
  EDIT_HOUSEHOLD: '13',
  EDIT_INDIVIDUAL: '14',
  DELETE_INDIVIDUAL: '15',
  ADD_INDIVIDUAL: '16',
  DELETE_HOUSEHOLD: '17',
  PAYMENT_COMPLAINT: '18',
  FSP_COMPLAINT: '19',
  REGISTRATION_COMPLAINT: '20',
  OTHER_COMPLAINT: '21',
  PARTNER_COMPLAINT: '22',
};

export const REPORT_TYPES = {
  INDIVIDUALS: '1',
  HOUSEHOLD_DEMOGRAPHICS: '2',
  CASH_PLAN_VERIFICATION: '3',
  PAYMENTS: '4',
  PAYMENT_VERIFICATION: '5',
  CASH_PLAN: '6',
  PROGRAM: '7',
  INDIVIDUALS_AND_PAYMENT: '8',
};

export const REPORTING_STATES = {
  PROCESSING: 1,
  GENERATED: 2,
  FAILED: 3,
};

export const COLLECT_TYPES_MAPPING = {
  A_: 'Unknown',
  A_0: 'None',
  A_1: 'Full',
  A_2: 'Partial',
};
export const GRIEVANCE_TICKETS_TYPES = {
  userGenerated: 0,
  systemGenerated: 1,
};

export const GrievanceTypes = {
  0: 'user',
  1: 'system',
};

export const GrievanceStatuses = {
  All: 'all',
  Active: 'active',
  Closed: 'Closed',
};

export const GrievanceSearchTypes = {
  TicketID: 'ticket_id',
  HouseholdID: 'ticket_hh_id',
  LastName: 'last_name',
};

export const GrievanceSteps = {
  Selection: 0,
  Lookup: 1,
  Verification: 2,
  Description: 3,
};

export const FeedbackSteps = {
  Selection: 0,
  Lookup: 1,
  Verification: 2,
  Description: 3,
};

export const ISSUE_TYPE_CATEGORIES = {
  DATA_CHANGE: 'Data Change',
  SENSITIVE_GRIEVANCE: 'Sensitive Grievance',
  GRIEVANCE_COMPLAINT: 'Grievance Complaint',
};

export const CommunicationSteps = {
  LookUp: 0,
  SampleSize: 1,
  Details: 2,
};

export const CommunicationTabsValues = {
  HOUSEHOLD: 0,
  TARGET_POPULATION: 1,
  RDI: 2,
};

export const SurveySteps = {
  LookUp: 0,
  SampleSize: 1,
  Details: 2,
};

export const SurveyTabsValues = {
  PROGRAM: 0,
  TARGET_POPULATION: 1,
  RDI: 2,
  A_: 'Unknown',
  A_0: 'None',
  A_1: 'Full',
  A_2: 'Partial',
};

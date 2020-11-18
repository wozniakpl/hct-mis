export const TARGETING_STATES = {
  NONE: 'None',
  DRAFT: 'Open',
  APPROVED: 'Locked',
  FINALIZED: 'Sent',
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
  //system flagging missing
};

export const GRIEVANCE_ISSUE_TYPES = {
  ADD_INDIVIDUAL: '16',
  EDIT_INDIVIDUAL: '14',
};

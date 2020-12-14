export const PERMISSIONS = {
  // RDI
  RDI_VIEW_LIST: 'RDI_VIEW_LIST',
  RDI_VIEW_DETAILS: 'RDI_VIEW_DETAILS',
  RDI_IMPORT_DATA: 'RDI_IMPORT_DATA',
  RDI_RERUN_DEDUPE: 'RDI_RERUN_DEDUPE',
  RDI_MERGE_IMPORT: 'RDI_MERGE_IMPORT',

  // Population
  POPULATION_VIEW_HOUSEHOLDS_LIST: 'POPULATION_VIEW_HOUSEHOLDS_LIST',
  POPULATION_VIEW_HOUSEHOLDS_DETAILS: 'POPULATION_VIEW_HOUSEHOLDS_DETAILS',
  POPULATION_VIEW_INDIVIDUALS_LIST: 'POPULATION_VIEW_INDIVIDUALS_LIST',
  POPULATION_VIEW_INDIVIDUALS_DETAILS: 'POPULATION_VIEW_INDIVIDUALS_DETAILS',

  // User Management
  USER_MANAGEMENT_VIEW_LIST: 'USER_MANAGEMENT_VIEW_LIST',

  // Programme
  PRORGRAMME_VIEW_LIST_AND_DETAILS: 'PRORGRAMME_VIEW_LIST_AND_DETAILS',
  PROGRAMME_VIEW_PAYMENT_RECORD_DETAILS:
    'PROGRAMME_VIEW_PAYMENT_RECORD_DETAILS',
  PROGRAMME_CREATE: 'PROGRAMME_CREATE',
  PROGRAMME_UPDATE: 'PROGRAMME_UPDATE',
  PROGRAMME_REMOVE: 'PROGRAMME_REMOVE',
  PROGRAMME_ACTIVATE: 'PROGRAMME_ACTIVATE',
  PROGRAMME_FINISH: 'PROGRAMME_FINISH',

  // Targeting
  TARGETING_VIEW_LIST: 'TARGETING_VIEW_LIST',
  TARGETING_VIEW_DETAILS: 'TARGETING_VIEW_DETAILS',
  TARGETING_CREATE: 'TARGETING_CREATE',
  TARGETING_UPDATE: 'TARGETING_UPDATE',
  TARGETING_DUPLICATE: 'TARGETING_DUPLICATE',
  TARGETING_REMOVE: 'TARGETING_REMOVE',
  TARGETING_LOCK: 'TARGETING_LOCK',
  TARGETING_UNLOCK: 'TARGETING_UNLOCK',
  TARGETING_SEND: 'TARGETING_SEND',

  // Payment Verification
  PAYMENT_VERIFICATION_VIEW_LIST: 'PAYMENT_VERIFICATION_VIEW_LIST',
  PAYMENT_VERIFICATION_VIEW_DETAILS: 'PAYMENT_VERIFICATION_VIEW_DETAILS',
  PAYMENT_VERIFICATION_CREATE: 'PAYMENT_VERIFICATION_CREATE',
  PAYMENT_VERIFICATION_UPDATE: 'PAYMENT_VERIFICATION_UPDATE',
  PAYMENT_VERIFICATION_ACTIVATE: 'PAYMENT_VERIFICATION_ACTIVATE',
  PAYMENT_VERIFICATION_DISCARD: 'PAYMENT_VERIFICATION_DISCARD',
  PAYMENT_VERIFICATION_FINISH: 'PAYMENT_VERIFICATION_FINISH',
  PAYMENT_VERIFICATION_EXPORT: 'PAYMENT_VERIFICATION_EXPORT',
  PAYMENT_VERIFICATION_IMPORT: 'PAYMENT_VERIFICATION_IMPORT',
  PAYMENT_VERIFICATION_VERIFY: 'PAYMENT_VERIFICATION_VERIFY',
  PAYMENT_VERIFICATION_VIEW_PAYMENT_RECORD_DETAILS:
    'PAYMENT_VERIFICATION_VIEW_PAYMENT_RECORD_DETAILS',
};

export function hasPermissions(
  permission: string | string[],
  allowedPermissions: string[],
): boolean {
  // checks to see if has one permission or at least one from the array

  if (Array.isArray(permission)) {
    return allowedPermissions.some((perm) => permission.includes(perm));
  }
  return allowedPermissions.includes(permission);
}

export function hasPermissionInModule(
  module: string,
  allowedPermissions: string[],
): boolean {
  return allowedPermissions.some((perm) => perm.includes(module));
}

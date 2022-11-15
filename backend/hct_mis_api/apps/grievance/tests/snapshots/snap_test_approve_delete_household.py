# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestApproveDeleteHousehold::test_approve_delete_household 1'] = {
    'data': {
        'approveDeleteHousehold': {
            'grievanceTicket': {
                'deleteHouseholdTicketDetails': {
                    'reasonHousehold': None
                }
            }
        }
    }
}

snapshots['TestApproveDeleteHousehold::test_approve_delete_household 2'] = {
    'data': {
        'approveDeleteHousehold': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 11,
                    'line': 3
                }
            ],
            'message': "The original household (HH-22-0000.0142) hasn't to be in withdrawn status",
            'path': [
                'approveDeleteHousehold'
            ]
        }
    ]
}

snapshots['TestApproveDeleteHousehold::test_approve_delete_household 3'] = {
    'data': {
        'approveDeleteHousehold': {
            'grievanceTicket': {
                'deleteHouseholdTicketDetails': {
                    'reasonHousehold': {
                        'unicefId': 'HH-22-0000.0143'
                    }
                }
            }
        }
    }
}

snapshots['TestApproveDeleteHousehold::test_approve_delete_household 4'] = {
    'data': {
        'approveDeleteHousehold': {
            'grievanceTicket': {
                'deleteHouseholdTicketDetails': {
                    'reasonHousehold': None
                }
            }
        }
    }
}

snapshots['TestApproveDeleteHousehold::test_approve_delete_household 5'] = {
    'data': {
        'approveDeleteHousehold': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 11,
                    'line': 3
                }
            ],
            'message': 'No Household matches the given query.',
            'path': [
                'approveDeleteHousehold'
            ]
        }
    ]
}

snapshots['TestApproveDeleteHousehold::test_approve_delete_household 6'] = {
    'data': {
        'approveDeleteHousehold': {
            'grievanceTicket': {
                'deleteHouseholdTicketDetails': {
                    'reasonHousehold': {
                        'unicefId': 'HH-22-0000.0144'
                    }
                }
            }
        }
    }
}

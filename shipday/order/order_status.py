class OrderStatus:
    ALREADY_DELIVERED = 'ALREADY_DELIVERED'
    NOT_ASSIGNED = 'NOT_ASSIGNED'
    NOT_ACCEPTED = 'NOT_ACCEPTED'
    NOT_STARTED_YET = 'NOT_STARTED_YET'
    STARTED = 'STARTED'
    PICKED_UP = 'PICKED_UP'
    READY_TO_DELIVER = 'READY_TO_DELIVER'
    FAILED_DELIVERY = 'FAILED_DELIVERY'
    ACTIVE = 'ACTIVE'
    INCOMPLETE = 'INCOMPLETE'

    _list_ = ['ALREADY_DELIVERED', 'NOT_ASSIGNED', 'NOT_ACCEPTED', 'NOT_STARTED_YET', 'STARTED',
              'PICKED_UP', 'READY_TO_DELIVER', 'FAILED_DELIVERY', 'ACTIVE', 'INCOMPLETE']

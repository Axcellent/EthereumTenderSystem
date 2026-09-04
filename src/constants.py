# TENDERS
# tx
CREATE_TENDER = 'createTender'
CLOSE_TENDER = 'closeTender'
REVERT_TENDER = 'revertTender'
# view
GET_TENDER = 'tenders'
GET_TENDERS = 'getTenders'
GET_USERS_TENDERS = 'getUsersTenders'

# CONTRACTS
# tx
OPEN_CONTRACT = 'openContract'
FINANCE_CONTRACT = 'financeContract'
HAND_IN_JOB = 'finishContract'
ACCEPT_JOB = 'acceptFinishedContract'
# view
GET_TENDER_CONTRACT = 'tenderContract'
GET_CONTRACT = 'contracts'

# BIDS
# tx
SUBMIT_BID = 'submitBid'
REVERT_BID = 'withdrawBid'
# view
GET_BID = 'bids'
GET_TENDER_BIDS = 'getTenderBids'
GET_USER_BIDS = 'usersBids'

# REPORTS
# tx
CREATE_REPORT = 'submitReport'
REVIEW_REPORT = 'reviewReport'
# view
GET_REPORTS = 'getContractReports'
GET_REPORT = 'reports'

# REVIEWS
# tx
CREATE_REVIEW = 'submitReview'
EXAMINE_REVIEW = 'reviewReview'
# view
GET_REVIEW = 'reviews'

# USERS
# tx
USER_REGISTER = "register"
DELETE_USER = "deleteUser"
BAN_USER = "banUser"
UNBAN_USER = "unbanUser"
# view
GET_USER = "users"
GET_REPUTATION = "getReputation"
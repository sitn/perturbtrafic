class CustomError(Exception):
    general_exception = 'An error occured while executing the query'
    id_not_found_exception = 'Id not found'
    user_not_found_exception = 'User not found'
    not_authorized_exception = 'Not authorized'
    delegation_exists_exception = 'Delegation already exists for the user'

    pass
def create_error_response(api_error):
    return api_error.serialize(), api_error.code

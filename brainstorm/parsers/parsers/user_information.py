class UserInformationParser:
    tag = 'user_information'

    def __call__(self, context, whole_data):
        return whole_data.user_information

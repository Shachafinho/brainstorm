class UserInformationParser:
    tag = 'user_information'

    def __call__(self, context, mq_whole_data):
        context.user_id = mq_whole_data.user_information.user_id
        return context, mq_whole_data.user_information

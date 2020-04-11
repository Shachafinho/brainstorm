import attr

from .snapshot import Snapshot
from .user_information import UserInformation


_TYPE_KEY = 'whole_data'


@attr.s(auto_attribs=True, slots=True)
class WholeData():
    user_information: UserInformation
    snapshot: Snapshot

    def serialize(self, context):
        return {
            _TYPE_KEY: {
                **self.user_information.serialize(context),
                **self.snapshot.serialize(context),
            }
        }

    @classmethod
    def deserialize(cls, context, serialized_whole_data):
        user_information = UserInformation.deserialize(
            context, serialized_whole_data[_TYPE_KEY])
        snapshot = Snapshot.deserialize(
            context, serialized_whole_data[_TYPE_KEY])
        return cls(user_information, snapshot)

import http

import attr

from brainstorm.utils.converter import converter


def _code_converter(obj):
    if isinstance(obj, http.HTTPStatus):
        return obj.value
    return obj


@attr.s(auto_attribs=True, slots=True)
class Error:
    code: int = attr.ib(converter=_code_converter)
    message: str

    def serialize(self):
        return converter.unstructure(self)

    @classmethod
    def deserialize(cls, serialized_data):
        return converter.structure(serialized_data, cls)


@attr.s(auto_attribs=True, slots=True)
class BadRequestError(Error):
    code: int = attr.ib(default=http.HTTPStatus.BAD_REQUEST.value, kw_only=True)


@attr.s(auto_attribs=True, slots=True)
class NotFoundError(Error):
    code: int = attr.ib(default=http.HTTPStatus.NOT_FOUND.value, kw_only=True)

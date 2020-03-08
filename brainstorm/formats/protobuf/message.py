import construct

from construct import StreamError


Message = construct.Prefixed(
    construct.Int32ul, construct.GreedyBytes).compile()

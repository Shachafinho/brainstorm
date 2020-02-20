import construct


Message = construct.Prefixed(
    construct.Int32ul, construct.GreedyBytes).compile()

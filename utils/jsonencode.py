import jsonpickle


def dumps(value, indent=4, ensure_ascii=False, max_depth=3):
    jsonpickle.set_preferred_backend('json')
    jsonpickle.set_encoder_options('json', ensure_ascii=ensure_ascii)
    return jsonpickle.dumps(value, indent=indent, max_depth=max_depth)


def loads(value):
    jsonpickle.set_preferred_backend('json')
    jsonpickle.set_decoder_options('json', encoding='utf8')
    return jsonpickle.loads(value)


encode = dumps
decode = loads

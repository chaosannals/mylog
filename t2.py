from whoosh.fields import FieldType, TEXT

print(issubclass(TEXT, FieldType))
print(isinstance(TEXT(), FieldType))

a = {
    'a': 123,
    'b': 343,
}

b = {
    'a': 3434,
    'c': 34343,
}

a.update(b)
print(a)
def compress(text, windowlen):
    index = 0
    dictionary = []

    for i in range(windowlen):
        if i < len(text):
            dictionary.append(text[i])

    while index < len(text):
        length = 0
        count = windowlen
        notFound = 1

        for i in range(index, len(text)):
            count = text.rfind(text[index:index + length + 1], 0, index)
            if count >= 0:
                length += 1
                windowlen = count
                notFound = 0

        if notFound:
            dictionary.append([0, 0, text[index]])
            index += 1
        else:
            if index + length < len(text):
                dictionary.append([index - windowlen, length, text[index + length]])
                index += length + 1
            else:
                dictionary.append([index - windowlen, length - 1, text[index + length - 1]])
                break
    return dictionary

dictionary = compress("la la la la", 5000)

print(dictionary)
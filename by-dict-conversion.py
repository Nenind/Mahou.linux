dict = {}
def buildDict():
    ruline = 'ё1234567890-=\йцукенгшщзхъфывапролджэячсмитьбю.'
    rulineshift = 'Ё!"№;%:?*()_+/ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,'
    enline = '`1234567890-=\qwertyuiop[]asdfghjkl;\'zxcvbnm,./'
    enlineshift = '~!@#$%^&*()_+|QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?'
    for rc, ec, rcs, ecs in zip(ruline, enline, rulineshift, enlineshift):
        dict[rc] = ec
        dict[rcs] = ecs

def convert(string):
    out = ""
    words = string.split(' ')
    print("----Debug start(ignore this)----")
    for word in words:
        keys_count = 0
        vals_count = 0
        keys_word = word
        vals_word = word
        for i in word:
            for k, v in dict.items():
                if i == k:
                    keys_word = keys_word.replace(i, v)
                    keys_count+=1
                if i == v:
                    vals_word = vals_word.replace(i, k)
                    vals_count+=1
        print("Vals: " + str(vals_count) + ", Keys: " + str(keys_count)+" Valw: " + vals_word + ", Keyw: " + keys_word)
        if vals_count >= keys_count:
            out += vals_word
        else:
            out += keys_word
        if word != words[-1]:
            out+=' '
    print("----Debug end----")
    return out

buildDict()
print("Double side conversion demo:");
result = convert(input("Enter english or/and russian letters/words:\n"))
print("result:\n" + result)
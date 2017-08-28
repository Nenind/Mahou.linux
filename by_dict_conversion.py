import re
def buildDict():
    dict = {}
    ruline = 'ё1234567890-=\йцукенгшщзхъфывапролджэячсмитьбю.'
    rulineshift = 'Ё!"№;%:?*()_+/ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,'
    enline = '`1234567890-=\qwertyuiop[]asdfghjkl;\'zxcvbnm,./'
    enlineshift = '~!@#$%^&*()_+|QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?'
    for rc, ec, rcs, ecs in zip(ruline, enline, rulineshift, enlineshift):
        dict[rc] = ec
        dict[rcs] = ecs
    return dict

def convert(string, dict):
    out = ""
    strlf = re.sub("\r\n?|\n", "\n", string)
    lines = strlf.split('\n')
    for line in lines:
        words = line.split(' ')
        # print("----Debug start(ignore this)----")
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
            # print("Vals: " + str(vals_count) + ", Keys: " + str(keys_count)+" Valw: " + vals_word + ", Keyw: " + keys_word)
            if vals_count >= keys_count:
                out += vals_word
            else:
                out += keys_word
            if word != words[-1]:
                out+=' '
        if line != lines[-1]:
            out+='\n'
    # print("----Debug end----")
    return out
if __name__ == '__main__':
    dict = buildDict()
    import sys
    result = ""
    if len(sys.argv) > 0:
        if sys.argv[1] == '--file':
            with open(sys.argv[2],'r', encoding="utf-8") as f:
                result = convert(f.read(), dict)
        else:
            result = convert(sys.argv[1], dict)
    else:
        print("Double side conversion demo:");
        result = convert(input("Enter english or/and russian letters/words:\n"), dict)
    print("result:\n" + result)
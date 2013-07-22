def pretty_list(plain_list, conjunction = ' & '):
    if plain_list:
        length = len(plain_list)
        if length == 1:
            return plain_list[0]
        cnt = 0
        pretty_list_string = ''
        sep = ''
        for item in plain_list:
            pretty_list_string += sep + item
            cnt += 1
            if cnt == length-1:
                sep = conjunction
            else:
                sep = ', '
            
        return pretty_list_string
    return
    


def match_pattern(file_name, pattern):
    file_index = 0
    pattern_index = 0
    star_index = None
    file_index_after_star = None

    while file_index < len(file_name) and pattern_index < len(file_name):
        if pattern[pattern_index] == '?' or pattern[pattern_index] == file_name[file_index]:
            file_index += 1
            pattern_index += 1
        elif pattern[pattern_index] == '*':
            if pattern[pattern_index+1] is None:
                return 'Yes'
            else:
                star_index = pattern_index
                file_index_after_star = file_index
                while file_name[file_index_after_star] != pattern[star_index+1] and pattern[star_index+1] is not None:
                    file_index_after_star += 1
                pattern_index += 1

        elif star_index is not None:
            pattern_index = star_index + 1
            file_index = file_index_after_star
        else:
            return "NO"
        print(file_index, pattern_index, star_index, file_index_after_star)

    return "YES" if pattern_index == len(pattern) else "NO"


file_name = input().strip()
pattern = input().strip()

print(match_pattern(file_name, pattern))

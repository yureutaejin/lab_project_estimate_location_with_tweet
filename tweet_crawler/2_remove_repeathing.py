import sys

# 한 방에 돌릴 때 사용
# detroit는 따로 편집
# first_result_data_name_list = ['boston', 'denver', 'el_paso', 'jackonville_florida', 'las_vegas', 'memphis', 'nashville', 'seattle', 'washington_DC']

# first_result_data_name_list = ['Boston', 'Detroit', 'Jacksonville', 'San Francisco', 'Fort Worth']
first_result_data_name_list = ['Fort Worth']

for i in first_result_data_name_list:
    # user 반복되는 거 제거
    with open('/Users/jinyuntae/Desktop/Personal_project/estimate_location_with_tweet/data/tweet_data/1_result_data/{}.json'.format(i),encoding="UTF-8") as twfile:
        new_line = []
        for line in twfile:
            if line != '':
                new_line.append((line[7:]).strip())
        del new_line[0]
        del new_line[-1]

    with open('/Users/jinyuntae/Desktop/Personal_project/estimate_location_with_tweet/data/tweet_data/2_result_data/{}_remove_repeat_user.json'.format(i), 'w', encoding="UTF-8") as new_dict:
        sys.stdout = new_dict
        print("{\"users\":[")
        for i in new_line:
            print(i)

        print("]}")



#Function to make any text lowercase and remove spaces
def normalize(text):
    text = text.lower()
    text = text.replace(" ", "")
    return text

def main(file_name, ra_name):

    #Open File and convert Data into a 2D Array
    data = open(file_name, "r")
    arr_list = []
    for line in data:
        line = line.strip()
        parts = line.split(",")
        arr_list.append(parts)

    # OP1
    filtered=[]
    for i in range(1, len(arr_list)):
        if normalize(arr_list[i][16]) == normalize(ra_name):
            if (
                arr_list[i][5] == "2022/23"
                or arr_list[i][5] == "2023/24"
                or arr_list[i][5] == "2024/25"
                or arr_list[i][5] == "2025/26"
            ):
                filtered.append([int(arr_list[i][6]), arr_list[i][18], arr_list[i][2]])

    # Graceful handling: if no matching rows found, return defaults
    if len(filtered) == 0:
        return [], [], 0

    # Sort by MON_SUN ascending, then GlobalID ascending for ties
    filtered.sort()
    min_mon_sun_site = filtered[0][2]

    # Negate MON_SUN so highest becomes lowest, then sort again
    for item in filtered:
        item[0] = -item[0]
    filtered.sort()
    max_mon_sun_site = filtered[0][2]

    OP1 = [max_mon_sun_site, min_mon_sun_site]

    # OP2
    sum_all = 0
    sum_ra = 0
    count_ra = 0
    count_all = 0
    for i in range(1, len(arr_list)):
        # calculate mean of all areas PCT_HEAVY_MON_SUN
        sum_all += float(arr_list[i][9])
        count_all += 1
        if normalize(arr_list[i][16]) == normalize(ra_name):  
            # calculate mean of specific area PCT_HEAVY_MON_SUN
            sum_ra += float(arr_list[i][9])
            count_ra += 1

    if count_all == 0:
        mean_all = 0
    else:
        mean_all = sum_all / count_all

    if count_ra == 0:
        mean_ra = 0
    else:
        mean_ra = sum_ra / count_ra
    mean_ra_sq = 0
    mean_all_sq = 0

    for i in range(1, len(arr_list)):
        # calculate SD of all areas PCT_HEAVY_MON_SUN
        mean_all_sq += (float(arr_list[i][9]) - mean_all) ** 2
        if normalize(arr_list[i][16]) == normalize(ra_name):
            # calculate standard deviation of specific areas PCT_HEAVY_MON_SUN
            mean_ra_sq += (float(arr_list[i][9]) - mean_ra) ** 2
 
    if count_ra <= 1:
        std_dev_ra = 0
    else:
        std_dev_ra = round(((mean_ra_sq / (count_ra - 1)) ** (1 / 2)), 4)

    if count_all <= 1:
        std_dev_all = 0
    else:
        std_dev_all = round(((mean_all_sq / (count_all - 1)) ** (1 / 2)), 4)

    OP2 = [std_dev_ra, std_dev_all]

    # OP3
    sum_mon_fri = 0
    sum_sat_sun = 0
    for i in range(1, len(arr_list)):
        if arr_list[i][12] == "Yes":
            sum_mon_fri += float(arr_list[i][7])
            sum_sat_sun += float(arr_list[i][8])

    if len(arr_list) <= 1:
        mean_mon_fri = 0
        mean_sat_sun = 0
    else:
        mean_mon_fri = sum_mon_fri / (len(arr_list) - 1)
        mean_sat_sun = sum_sat_sun / (len(arr_list) - 1)
    mean_sq_mon_fri = 0
    mean_sq_sat_sun = 0
    sum_cor = 0
    
    for i in range(1, len(arr_list)):
        if arr_list[i][12] == "Yes":
            mean_sq_mon_fri += (float(arr_list[i][7]) - mean_mon_fri) ** 2
            mean_sq_sat_sun += (float(arr_list[i][8]) - mean_sat_sun) ** 2
            sum_cor += (float(arr_list[i][7]) - mean_mon_fri) * (
                float(arr_list[i][8]) - mean_sat_sun
            )
    denominator = (mean_sq_mon_fri * mean_sq_sat_sun) ** (1 / 2)
    if denominator == 0:
        correlation = 0
    else:
        correlation = round(sum_cor / denominator, 4)
    OP3 = correlation

    return OP1, OP2, OP3

OP1, OP2, OP3 = main("SampleData_Lab4.csv", "Metropolitan")
print(OP1)
print(OP2)
print(OP3)

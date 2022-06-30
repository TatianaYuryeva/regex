import re
import csv


def read_phonebook():
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
        return contacts_list


def check_phones(contacts_list):
    for el in contacts_list[slice(1, None, 1)]:
        tel = re.sub(r'[\D]', '', el[-2])
        pattern = re.compile(r"(7|8)?(\d{3})(\d{3})(\d{2})(\d{2})(\d*)")
        res = pattern.sub(r"+7(\2)\3-\4-\5", tel)
        if len(tel) > 11:
            res = pattern.sub(r"+7(\2)\3-\4-\5 доб.\6", tel)
        el[-2] = res


def check_names(contacts_list):
    i = 0
    names_list = []
    for el in contacts_list[slice(1, None, 1)]:
        names_list.append(f"{el[0]} {el[1]} {el[2]}")
        pattern2 = re.compile(r"(\w+)")
        res2 = re.findall(pattern2, names_list[i])
        if len(res2) < 3:
            res2.append('')
        el[0] = res2[0]
        el[1] = res2[1]
        el[2] = res2[2]
        i += 1


def check_duplicate(contacts_list):
    names_dict = {}
    i = 0
    for el in contacts_list:
        lastname_firstname = (el[0] + el[1])
        k = lastname_firstname
        if lastname_firstname in names_dict.keys():
            count = 0
            for _ in el:
                if names_dict[k][count] == el[count]:
                    count += 1
                    continue
                contacts_list[i][count] = names_dict[k][count] + el[count]
                count += 1
        names_dict[k] = el
        i += 1
    checked_contacts_list = list(names_dict.values())
    return checked_contacts_list


def write_phonebook(checked_contacts_list):
    with open("phonebook.csv", "w", encoding='utf-8', newline='') as f:
        data_writer = csv.writer(f, delimiter=',')
        data_writer.writerows(checked_contacts_list)


if __name__ == '__main__':
    contact_list = read_phonebook()
    check_phones(contact_list)
    check_names(contact_list)
    checked_list = check_duplicate(contact_list)
    write_phonebook(checked_list)

import csv
import re


def format_last_name(contact):
    last_name = re.split('\s', contact[0])
    contact[0] = last_name[0]
    if 1 < len(last_name):
        contact[1] = last_name[1]
    if 2 < len(last_name):
        contact[2] = last_name[2]
    return contact


def format_first_name(contact):
    first_name = re.split('\s', contact[1])
    contact[1] = first_name[0]
    if 1 < len(first_name):
        contact[2] = first_name[1]
    return contact


def format_phone(contact):
    if contact[5]:
        phone = contact[5]
        phone = re.sub('(\-|\s|\(|\)|\+)', '', phone)
        phone = re.sub('^(7|8)', '+7', phone)
        additional = re.split('доб.', phone)
        if len(additional) > 1:
            phone = ' доб.'.join(additional)
        phone = phone[:2] + '(' + phone[2:5] + ')' + phone[5:8] + '-' + phone[8:10] + '-' + phone[10:12]
        contact[5] = phone


def merge_field(field1, field2):
    if field1:
        return field1
    else:
        return field2


def merge_contact(contact1, contact2):
    result = []
    for i in range(7):
        if not contact1[i]:
            new_field = contact2[i]
        elif not contact2[i]:
            new_field = contact1[i]
        else:
            new_field = merge_field(contact1[i], contact2[i])
        result.append(new_field)
    return result


def check_duplicate(contact1, contact2):
    if contact1[0] == contact2[0] and contact1[1] == contact2[1]:
        return True
    else:
        return False


def find_duplicates(contacts):
    duplicates = []
    uniq = contacts
    for item_uniq in uniq:
        counter = 0
        for item_init in contacts:
            if check_duplicate(item_uniq, item_init):
                counter += 1
                if counter > 1:
                    uniq.remove(item_uniq)
                    uniq.remove(item_init)
                    duplicates.append(merge_contact(item_uniq, item_init))
    result = uniq + duplicates
    print(result)
    return result


if __name__ == '__main__':
    with open("phonebook_raw.csv") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    for i in range(1, len(contacts_list)):
        format_last_name(contacts_list[i])
        format_first_name(contacts_list[i])
        format_phone(contacts_list[i])

    headers = [contacts_list[0]]
    list_to_check = contacts_list[1:len(contacts_list)]
    list_to_check = find_duplicates(list_to_check)
    contacts_list = headers + list_to_check

    with open("phonebook.csv", "w") as f:
        data_writer = csv.writer(f, delimiter=',')
        data_writer.writerows(contacts_list)

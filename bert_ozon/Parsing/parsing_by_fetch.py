import requests
from fake_useragent import UserAgent
import json
from pathlib import Path
root_dir = Path(__file__).parent.parent.parent.resolve()  # directory of source root


class FetchParser:
    def __init__(self, path):
        self.file_data = []
        with open(path, 'r') as file:
            for line in file:
                self.file_data.append(line)

    def find_string_idx_by_item(self, item):
        if item >= self.__len__():
            raise IndexError
        idx = 0
        counter = 0
        for i, line in enumerate(self.file_data):
            if "fetch(" in line.split('"'):
                counter += 1
                if counter - 1 == item:
                    idx = i
                    break
        return idx

    def __len__(self):
        length = 0
        for line in self.file_data:
            if "fetch(" in line.split('"'):
                length += 1
        return length

    def __getitem__(self, item):
        str_idx = self.find_string_idx_by_item(item)

        # url - srt
        string = self.file_data[str_idx]
        string = string[7:]
        string = string[:-5]
        url = string

        # params - dict
        # [:-1] - delete 0-determined
        string = "{" + self.file_data[str_idx + 1][:-1]
        for i in range(2, 19):
            string += self.file_data[str_idx + i][:-1]
        string += self.file_data[str_idx + 19][:-1]
        string += self.file_data[str_idx + 20][:-1]
        string += "}"
        dict_ = json.loads(string)
        params = dict_
        return url, params


def parsing_by_fetch(path_for_save_product_json_information):
    buffer_path = Path(root_dir)
    buffer_path /= Path('bert_ozon/Parsing/collecting_data/fetches_from_buffer/buffer_example.txt')

    parsed_fetches = FetchParser(buffer_path)
    # print(parsed_fetches.find_string_idx_by_item(2587))
    # return 0
    products_info = {}
    i = 0
    # 2587 for buffer 766-1018
    # overridden len method
    for p_fet in parsed_fetches:
        print(i)
        if i == 20:
            break
        i += 1
        url = p_fet[0]
        params = p_fet[1]

        if params["method"] == 'GET':
            print('GET')
        else:
            # отправляем запрос на сервер по имеющемуся fetch
            response = fetch(url, params)

            if response.status_code == 200:  # проверка на то что код возврата 200 (т.е. что все ок)
                try:  # ловим ошибки несуществующего ключа
                    products = response.json()['items']
                    for product in products:
                        key = str(product["variant_id"])
                        product_info = {"name": product["name"],
                                        "description": product["description"],
                                        "categories": product["categories"]}
                        products_info[key] = product_info
                except KeyError:
                    print('KeyError')
            else:
                print('status_code != 200')

    with open(path_for_save_product_json_information, 'w', encoding='utf8') as f:
        json.dump(products_info, f, ensure_ascii=False, indent=4)


def fetch(url, params):
    headers = params["headers"]
    headers['User-Agent'] = UserAgent().chrome
    body = params["body"].encode("utf-8")
    if params["method"] == "GET":
        return requests.get(url, headers=headers)
    if params["method"] == "POST":
        return requests.post(url, headers=headers, data=body)


if __name__ == '__main__':
    path_for_save_product_json_information = Path(root_dir)
    path_for_save_product_json_information /= Path('bert_ozon/data/example/example.json')
    parsing_by_fetch(path_for_save_product_json_information)

    """fetch("https://seller.ozon.ru/api/item/search-attribute-model-data-by-names", {
  "headers": {
    "accept": "application/json, text/plain, */*",
    "accept-language": "ru",
    "content-type": "application/json",
    "sec-ch-ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Linux\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-o3-app-name": "seller-ui",
    "x-o3-company-id": "1402962",
    "x-o3-language": "ru",
    "x-o3-page-type": "products-other",
    "cookie": "__cf_bm=YrfSLBVNQye27IrFhdYg12r5O1CffqGDv0HT_vz1INM-1696369420-0-AYYkei3QG3Len3qJ2wE1qcEzWjJvizmPhQ3u23dJnzuG0oZfcoerye3rqVBrZQvQe4lHA0SkQ5AyhB3e24qrCQE=; x-o3-language=ru; cf_clearance=3cYV_YwusX3kh7P10CxVuHo0.AZGsg7YSbahSethLWs-1696369421-0-1-97d040ff.369bf0c6.56863828-0.2.1696369421; __Secure-ab-group=15; xcid=448362e4be69ffa76e7bcb3f6fb7bf46; __Secure-ext_xcid=448362e4be69ffa76e7bcb3f6fb7bf46; rfuid=NjkyNDcyNDUyLDEyNC4wNDM0NzUyNzUxNjA3NCwxMzkzNjg1NDU1LC0xLC0xNDY1MjQ0MjIsVzNzaWJtRnRaU0k2SWxCRVJpQldhV1YzWlhJaUxDSmtaWE5qY21sd2RHbHZiaUk2SWxCdmNuUmhZbXhsSUVSdlkzVnRaVzUwSUVadmNtMWhkQ0lzSW0xcGJXVlVlWEJsY3lJNlczc2lkSGx3WlNJNkltRndjR3hwWTJGMGFXOXVMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4wc2V5SjBlWEJsSWpvaWRHVjRkQzl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOVhYMHNleUp1WVcxbElqb2lRMmh5YjIxbElGQkVSaUJXYVdWM1pYSWlMQ0prWlhOamNtbHdkR2x2YmlJNklsQnZjblJoWW14bElFUnZZM1Z0Wlc1MElFWnZjbTFoZENJc0ltMXBiV1ZVZVhCbGN5STZXM3NpZEhsd1pTSTZJbUZ3Y0d4cFkyRjBhVzl1TDNCa1ppSXNJbk4xWm1acGVHVnpJam9pY0dSbUluMHNleUowZVhCbElqb2lkR1Y0ZEM5d1pHWWlMQ0p6ZFdabWFYaGxjeUk2SW5Ca1ppSjlYWDBzZXlKdVlXMWxJam9pUTJoeWIyMXBkVzBnVUVSR0lGWnBaWGRsY2lJc0ltUmxjMk55YVhCMGFXOXVJam9pVUc5eWRHRmliR1VnUkc5amRXMWxiblFnUm05eWJXRjBJaXdpYldsdFpWUjVjR1Z6SWpwYmV5SjBlWEJsSWpvaVlYQndiR2xqWVhScGIyNHZjR1JtSWl3aWMzVm1abWw0WlhNaU9pSndaR1lpZlN4N0luUjVjR1VpT2lKMFpYaDBMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4xZGZTeDdJbTVoYldVaU9pSk5hV055YjNOdlpuUWdSV1JuWlNCUVJFWWdWbWxsZDJWeUlpd2laR1Z6WTNKcGNIUnBiMjRpT2lKUWIzSjBZV0pzWlNCRWIyTjFiV1Z1ZENCR2IzSnRZWFFpTENKdGFXMWxWSGx3WlhNaU9sdDdJblI1Y0dVaU9pSmhjSEJzYVdOaGRHbHZiaTl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOUxIc2lkSGx3WlNJNkluUmxlSFF2Y0dSbUlpd2ljM1ZtWm1sNFpYTWlPaUp3WkdZaWZWMTlMSHNpYm1GdFpTSTZJbGRsWWt0cGRDQmlkV2xzZEMxcGJpQlFSRVlpTENKa1pYTmpjbWx3ZEdsdmJpSTZJbEJ2Y25SaFlteGxJRVJ2WTNWdFpXNTBJRVp2Y20xaGRDSXNJbTFwYldWVWVYQmxjeUk2VzNzaWRIbHdaU0k2SW1Gd2NHeHBZMkYwYVc5dUwzQmtaaUlzSW5OMVptWnBlR1Z6SWpvaWNHUm1JbjBzZXlKMGVYQmxJam9pZEdWNGRDOXdaR1lpTENKemRXWm1hWGhsY3lJNkluQmtaaUo5WFgxZCxXeUp5ZFMxU1ZTSmQsMCwxLDAsMjQsMjM3NDE1OTMwLDgsMjI3MTI2NTIwLDEsMSwwLC00OTEyNzU1MjMsUjI5dloyeGxJRWx1WXk0Z1RtVjBjMk5oY0dVZ1IyVmphMjhnVEdsdWRYZ2dlRGcyWHpZMElEVXVNQ0FvV0RFeE95Qk1hVzUxZUNCNE9EWmZOalFwSUVGd2NHeGxWMlZpUzJsMEx6VXpOeTR6TmlBb1MwaFVUVXdzSUd4cGEyVWdSMlZqYTI4cElFTm9jbTl0WlM4eE1UY3VNQzR3TGpBZ1UyRm1ZWEpwTHpVek55NHpOaUF5TURBek1ERXdOeUJOYjNwcGJHeGgsZXlKamFISnZiV1VpT25zaVlYQndJanA3SW1selNXNXpkR0ZzYkdWa0lqcG1ZV3h6WlN3aVNXNXpkR0ZzYkZOMFlYUmxJanA3SWtSSlUwRkNURVZFSWpvaVpHbHpZV0pzWldRaUxDSkpUbE5VUVV4TVJVUWlPaUpwYm5OMFlXeHNaV1FpTENKT1QxUmZTVTVUVkVGTVRFVkVJam9pYm05MFgybHVjM1JoYkd4bFpDSjlMQ0pTZFc1dWFXNW5VM1JoZEdVaU9uc2lRMEZPVGs5VVgxSlZUaUk2SW1OaGJtNXZkRjl5ZFc0aUxDSlNSVUZFV1Y5VVQxOVNWVTRpT2lKeVpXRmtlVjkwYjE5eWRXNGlMQ0pTVlU1T1NVNUhJam9pY25WdWJtbHVaeUo5ZlgxOSw2NSwtMTI4NTU1MTMsMSwxLC0xLDE2OTk5NTQ4ODcsMTY5OTk1NDg4NywzMzYwMDc5MzMsMTI=; __Secure-access-token=3.113480185.rm7yI53cTSmzJJ8NHTOt6w.15.l8cMBQAAAABlHIs3M3KN1KN3ZWKrNzkyNTM1ODg4NjQAgJCg.20220910222325.20231003234423.6UZewOtIqgWEEWOHWkUCPBhym3QFArqpgGTToTCVSGs; __Secure-refresh-token=3.113480185.rm7yI53cTSmzJJ8NHTOt6w.15.l8cMBQAAAABlHIs3M3KN1KN3ZWKrNzkyNTM1ODg4NjQAgJCg.20220910222325.20231003234423.q7iipiRSkHvKiKH-YAL-s76-kNhmG-siCAMNcjvYEsU; __Secure-user-id=113480185; is_adult_confirmed=; is_alco_adult_confirmed=; bacntid=3196278; contentId=1402962",
    "Referer": "https://seller.ozon.ru/app/products/create",
    "Referrer-Policy": "strict-origin-when-cross-origin"
  },
  "body": "{\"limit\":10,\"names\":[\"Медицинская сумка\"],\"offset\":0}",
  "method": "POST"
})"""



import json
import urllib.request


CONFIG_FILE = "config.json"

OUTPUT_FILE = "fish.json"



def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



def save_json(path,data):

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )



def download_json(url):

    print("下载源配置:")
    print(url)


    request = urllib.request.Request(
        url,
        headers={
            "User-Agent":
            "Mozilla/5.0"
        }
    )


    with urllib.request.urlopen(
        request,
        timeout=30
    ) as response:


        text = response.read().decode(
            "utf-8"
        )


    return json.loads(text)



def filter_sites(data,remove_list):


    sites = data.get(
        "sites",
        []
    )


    new_sites = []



    print(
        "原始站点:",
        len(sites)
    )
    print("======全部站点======")

for s in sites:
    print(
        s.get("key"),
        "|",
        s.get("name")
    )

    print("===================")


    for site in sites:


        key = str(
            site.get(
                "key",
                ""
            )
        )


        name = str(
            site.get(
                "name",
                ""
            )
        )


        api = str(
            site.get(
                "api",
                ""
            )
        )


        # key/name/api 三项匹配

        if (
            key in remove_list
            or
            name in remove_list
            or
            api in remove_list
        ):

            print(
                "删除:",
                key,
                name
            )

            continue



        new_sites.append(site)



    data["sites"] = new_sites


    print(
        "剩余站点:",
        len(new_sites)
    )


    return data



def main():


    config = load_json(
        CONFIG_FILE
    )


    source_url = config[
        "source_url"
    ]


    remove_list = set(
        config[
            "remove_sites"
        ]
    )


    # 下载官方源

    data = download_json(
        source_url
    )


    # 过滤

    result = filter_sites(
        data,
        remove_list
    )


    # 输出

    save_json(
        OUTPUT_FILE,
        result
    )


    print(
        "=================="
    )

    print(
        "完成:"
        ,
        OUTPUT_FILE
    )



if __name__ == "__main__":

    main()

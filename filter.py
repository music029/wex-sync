import json
import urllib.request


CONFIG_FILE = "config.json"
OUTPUT_FILE = "fish.json"



def load_json(file):

    with open(
        file,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



def save_json(file, data):

    with open(
        file,
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

    print("下载接口:")
    print(url)


    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )


    with urllib.request.urlopen(
        req,
        timeout=30
    ) as r:

        text = r.read().decode(
            "utf-8"
        )


    data = json.loads(text)


    if "sites" not in data:

        raise Exception(
            "接口异常，没有sites字段"
        )


    return data



def get_order(key, order_list):

    for i, item in enumerate(order_list):

        if key == item:

            return i

    return 999



def sort_site(site, config):

    key = site.get(
        "key",
        ""
    )


    index = get_order(
        key,
        config.get(
            "function_order",
            []
        )
    )

    if index != 999:

        return (
            0,
            index
        )



    index = get_order(
        key,
        config.get(
            "fourk_order",
            []
        )
    )

    if index != 999:

        return (
            1,
            index
        )



    index = get_order(
        key,
        config.get(
            "movie_order",
            []
        )
    )

    if index != 999:

        return (
            2,
            index
        )



    index = get_order(
        key,
        config.get(
            "other_order",
            []
        )
    )

    if index != 999:

        return (
            3,
            index
        )


    return (
        9,
        999
    )



def main():

    config = load_json(
        CONFIG_FILE
    )


    data = download_json(
        config["source_url"]
    )


    old_sites = data.get(
        "sites",
        []
    )


    print(
        "原始站点:",
        len(old_sites)
    )


    if len(old_sites) == 0:

        raise Exception(
            "接口站点为空"
        )



    keep = set(
        config.get(
            "keep_sites",
            []
        )
    )


    rename = config.get(
        "rename_by_key",
        {}
    )


    new_sites = []

    seen = set()



    for site in old_sites:


        key = site.get(
            "key",
            ""
        )


        if not key:

            continue



        if key in seen:

            continue


        seen.add(key)



        # 只保留指定站点

        if key not in keep:

            continue



        # 修改名称

        if key in rename:

            site["name"] = rename[key]



        new_sites.append(site)



    # 排序

    new_sites.sort(
        key=lambda x:
        sort_site(
            x,
            config
        )
    )



    # ==========================
    # 安全保护
    # ==========================

    if len(new_sites) == 0:

        raise Exception(
            "过滤后没有站点，请检查keep_sites配置"
        )


    print("================")

    print(
        "过滤后站点:",
        len(new_sites)
    )


    for s in new_sites:

        print(
            s.get("key"),
            "|",
            s.get("name")
        )


    print("================")



    data["sites"] = new_sites



    save_json(
        OUTPUT_FILE,
        data
    )


    print(
        "生成完成:",
        OUTPUT_FILE
    )



if __name__ == "__main__":

    main()

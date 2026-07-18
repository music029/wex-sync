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



def download(url):

    print("下载接口:")
    print(url)

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent":
            "Mozilla/5.0"
        }
    )


    with urllib.request.urlopen(
        req,
        timeout=20
    ) as r:

        return json.loads(
            r.read()
            .decode("utf-8")
        )



def main():


    cfg = load_json(CONFIG_FILE)


    data = download(
        cfg["source"]
    )


    if "sites" not in data:

        raise Exception(
            "接口异常，没有sites字段"
        )


    old = len(
        data["sites"]
    )


    print(
        "原始站点:",
        old
    )


    keep = []


    for site in data["sites"]:


        key = site.get(
            "key",
            ""
        )


        name = site.get(
            "name",
            ""
        )


        text = key + name


        # 删除关键词

        remove = False


        for word in cfg["remove_keywords"]:

            if word in text:

                remove = True
                break


        if remove:

            continue



        # 保留列表

        if key in cfg["keep_keys"]:

            keep.append(site)



    # 改名

    for site in keep:


        key = site.get(
            "key"
        )


        if key in cfg["rename"]:

            site["name"] = cfg["rename"][key]



    # 排序

    order = cfg["order"]


    result = []


    for key in order:

        for site in keep:

            if site.get("key") == key:

                result.append(site)



    data["sites"] = result



    print(
        "过滤后站点:",
        len(result)
    )


    print("================")


    for s in result:

        print(
            s["key"],
            "|",
            s["name"]
        )


    print("================")



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

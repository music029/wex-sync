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



def save_json(path, data):

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

    print("=================")
    print("下载配置:")
    print(url)


    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )


    with urllib.request.urlopen(
        request,
        timeout=30
    ) as response:

        content = response.read().decode(
            "utf-8"
        )


    return json.loads(content)



def main():


    # 读取过滤配置

    config = load_json(
        CONFIG_FILE
    )


    source_url = config.get(
        "source_url"
    )


    # 下载作者配置

    data = download_json(
        source_url
    )


    sites = data.get(
        "sites",
        []
    )


    print("=================")
    print(
        "原始站点:",
        len(sites)
    )


    # 白名单

    keep_sites = set(
        config.get(
            "keep_sites",
            []
        )
    )


    new_sites = []



    print("=================")
    print("开始过滤")
    print("=================")



    for site in sites:


        key = site.get(
            "key",
            ""
        )


        name = site.get(
            "name",
            ""
        )


        if key in keep_sites:


            print(
                "保留:",
                key,
                "|",
                name
            )


            new_sites.append(
                site
            )


        else:


            print(
                "屏蔽:",
                key,
                "|",
                name
            )



    # 替换站点列表

    data["sites"] = new_sites



    print("=================")
    print(
        "最终站点:",
        len(new_sites)
    )



    # 输出 fish.json

    save_json(
        OUTPUT_FILE,
        data
    )


    print("=================")
    print(
        "完成:",
        OUTPUT_FILE
    )



if __name__ == "__main__":

    main()

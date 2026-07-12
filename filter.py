import json
import urllib.request


CONFIG_FILE = "config.json"
OUTPUT_FILE = "fish.json"


def load_json(path):

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)



def save_json(path, data):

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )



def download_json(url):

    print("下载配置:")
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
    ) as response:

        text = response.read().decode("utf-8")

    return json.loads(text)



def main():

    config = load_json(CONFIG_FILE)


    source_url = config["source_url"]


    data = download_json(source_url)


    sites = data.get("sites", [])


    print("=================")
    print("原始站点:", len(sites))


    print("======全部站点======")

    for s in sites:

        print(
            s.get("key"),
            "|",
            s.get("name")
        )

    print("=================")



    remove_sites = set(
        config.get("remove_sites", [])
    )


    new_sites = []


    for site in sites:


        key = site.get("key", "")
        name = site.get("name", "")
        api = site.get("api", "")


        if (
            key in remove_sites
            or name in remove_sites
            or api in remove_sites
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


    save_json(
        OUTPUT_FILE,
        data
    )


    print("=================")
    print("完成: fish.json")



if __name__ == "__main__":
    main()

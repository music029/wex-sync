import json
import urllib.request


CONFIG_FILE = "config.json"
OUTPUT_FILE = "fish.json"



# =========================
# 名称修改规则
# =========================

name_replace = {

    "NewDouBan": "✧豆瓣┃导航✧",

    "Doubana": "✧【更新:20260712】✧",

    "Wexconfig": "✧配置┃中心✧",


    "二小": "✧二小┃4K✧‍",

    "玩偶": "✧‍玩偶┃4K✧‍",

    "NewZhiZhen": "✧至臻┃4K✧",

    "NewMuOu": "✧木偶┃4K✧",

    "NewDuoDuo": "✧多多┃4K✧",

    "NewPanMe123": "✧123┃4K✧",


    "WexHanXiaoQuan": "✧韩剧┃秒播✧",

    "WexGuaZi": "✧瓜子┃秒播✧",

    "賤賤": "✧贱片┃秒播✧",

    "WexWenCai": "✧文才┃秒播✧",

    "WexDuBoKu": "✧独播┃秒播✧",

    "WexYueYue": "✧闪电┃秒播✧",

    "WexV6DaShiXiong": "✧师兄┃秒播✧",

    "WexV6TeGou": "✧太狗┃秒播✧",

    "WexYiYs": "✧伊影┃秒播✧",

    "WexReBo": "✧热播┃秒播✧",


    "ChildrenDuoDuo": "✧多多┃儿歌✧",

    "ChildrenBaoBao": "✧宝宝┃儿歌✧",

    "ChildrenBeiWa": "✧贝贝┃儿歌✧",


    "MusicIKtv": "✧KTV┃音乐✧",

    "Music163": "✧易听┃音乐✧",

    "MusicKuWo": "✧酷听┃音乐✧"

}



# =========================
# 读取json
# =========================

def load_json(file):

    with open(
        file,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



# =========================
# 保存json
# =========================

def save_json(file,data):

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



# =========================
# 下载作者接口
# =========================

def download_json(url):

    print("下载:")
    print(url)


    req = urllib.request.Request(
        url,
        headers={
            "User-Agent":"Mozilla/5.0"
        }
    )


    with urllib.request.urlopen(
        req,
        timeout=30
    ) as r:

        text = r.read().decode(
            "utf-8"
        )


    return json.loads(text)




# =========================
# 主程序
# =========================

def main():


    config = load_json(
        CONFIG_FILE
    )


    source_url = config["source_url"]


    data = download_json(
        source_url
    )


    sites = data.get(
        "sites",
        []
    )


    print("================")
    print(
        "原始站点:",
        len(sites)
    )



    keep_sites = set(
        config.get(
            "keep_sites",
            []
        )
    )



    new_sites = []



    print("================")
    print("开始过滤")
    print("================")



    for site in sites:


        key = site.get(
            "key",
            ""
        )


        name = site.get(
            "name",
            ""
        )



        # 白名单

        if key in keep_sites:



            # 修改名称

            if key in name_replace:

                site["name"] = name_replace[key]



            new_sites.append(site)



            print(
                "保留:",
                key,
                "|",
                site["name"]
            )


        else:


            print(
                "屏蔽:",
                key,
                "|",
                name
            )



    data["sites"] = new_sites



    print("================")
    print(
        "最终站点:",
        len(new_sites)
    )



    save_json(
        OUTPUT_FILE,
        data
    )


    print("================")
    print(
        "完成:",
        OUTPUT_FILE
    )




if __name__ == "__main__":

    main()

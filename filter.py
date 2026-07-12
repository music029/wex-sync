import json
import urllib.request
from datetime import datetime


SOURCE = "https://9280.kstore.vip/wex.json"


# =====================
# 读取配置
# =====================

with open(
    "config.json",
    "r",
    encoding="utf-8"
) as f:

    cfg = json.load(f)



# =====================
# 获取源数据
# =====================

try:

    response = urllib.request.urlopen(
        SOURCE,
        timeout=20
    )

    data = json.loads(
        response.read().decode("utf-8")
    )


except Exception as e:

    raise Exception(
        f"接口访问失败: {e}"
    )



# =====================
# 数据保护
# =====================

if "sites" not in data:

    raise Exception(
        "接口异常，没有sites字段"
    )



old_sites = data["sites"]


old_count = len(old_sites)



# =====================
# 排序辅助
# =====================

def get_order(
    key,
    name,
    order_list
):

    """
    根据key优先排序
    找不到再根据名称匹配
    """

    for index, item in enumerate(order_list):

        if key == item:

            return index


    for index, item in enumerate(order_list):

        if item in name:

            return index


    return 999



# =====================
# 过滤处理
# =====================


sites = []

seen_keys = set()

new_sites = []



for site in old_sites:


    key = site.get(
        "key",
        ""
    )


    name = site.get(
        "name",
        ""
    )



    # 空key跳过

    if not key:

        continue



    # 去重复

    if key in seen_keys:

        continue


    seen_keys.add(key)



    # =====================
    # key改名（最高优先）
    # =====================

    if key in cfg.get(
        "rename_by_key",
        {}
    ):

        site["name"] = cfg[
            "rename_by_key"
        ][key]



    else:


        # =====================
        # 名称改名
        # =====================

        for old_name, new_name in cfg.get(
            "rename_map",
            {}
        ).items():


            if old_name in name:

                site["name"] = new_name

                break



    name = site.get(
        "name",
        ""
    )



    # =====================
    # 删除关键词
    # =====================

    if any(
        word in name
        for word in cfg.get(
            "remove_keywords",
            []
        )
    ):

        continue



    # =====================
    # 4K白名单
    # =====================

    if "4K" in name:


        if key not in cfg.get(
            "keep_4k",
            []
        ):

            continue



    sites.append(site)



    # 新站点记录

    if key not in cfg.get(
        "rename_by_key",
        {}
    ):

        new_sites.append(
            {
                "key": key,
                "name": name
            }
        )



# =====================
# 数量保护
# =====================

min_sites = cfg.get(
    "min_sites",
    10
)


if len(sites) < min_sites:

    raise Exception(
        f"过滤异常，仅剩 {len(sites)} 个站点，停止更新"
    )
# =====================
# 排序
# =====================

def sort_site(site):

    key = site.get(
        "key",
        ""
    )

    name = site.get(
        "name",
        ""
    )


    # 第一组：功能区

    function_index = get_order(
        key,
        name,
        cfg.get(
            "function_order",
            []
        )
    )


    if function_index != 999:

        return (
            0,
            function_index
        )



    # 第二组：4K

    if "4K" in name:


        return (
            1,
            get_order(
                key,
                name,
                cfg.get(
                    "fourk_order",
                    []
                )
            )
        )



    # 第三组：APP

    app_index = get_order(
        key,
        name,
        cfg.get(
            "app_order",
            []
        )
    )


    if app_index != 999:

        return (
            2,
            app_index
        )



    # 第五组：固定尾部

    footer_index = get_order(
        key,
        name,
        cfg.get(
            "footer_order",
            []
        )
    )


    if footer_index != 999:

        return (
            4,
            footer_index
        )



    # 第四组：影视

    movie_index = get_order(
        key,
        name,
        cfg.get(
            "movie_order",
            []
        )
    )


    if movie_index != 999:

        return (
            3,
            movie_index
        )



    # 未知站点

    return (
        3,
        999
    )




sites.sort(
    key=sort_site
)




# =====================
# 写入数据
# =====================

data["sites"] = sites




with open(
    "fish.json",
    "w",
    encoding="utf-8"
) as f:


    json.dump(
        data,
        f,
        ensure_ascii=False,
        indent=2
    )



# =====================
# 日志
# =====================

print(
    "======================"
)


print(
    "同步成功"
)


print(
    "接口:",
    SOURCE
)


print(
    "同步时间:",
    datetime.now()
)


print(
    "原站点:",
    old_count
)


print(
    "重复删除:",
    old_count - len(seen_keys)
)


print(
    "删除:",
    old_count - len(sites)
)


print(
    "保留:",
    len(sites)
)



if new_sites:


    print(
        ""
    )

    print(
        "发现未配置站点:"
    )


    for item in new_sites:

        print(
            "-",
            item["key"],
            item["name"]
        )



print(
    "======================"
)

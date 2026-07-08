def generate_captions(query: str) -> list[str]:
    """MVP caption templates; replace this with an LLM endpoint when needed."""
    compact = query.strip().rstrip("。！？!?，,")

    if any(word in compact for word in ("加班", "工作", "老板", "周末")):
        return [
            "嘴上：没问题。心里：问题很大。",
            "好的老板（灵魂已离线）",
            "这个班，是非加不可吗？",
        ]
    if any(word in compact for word in ("学习", "考试", "作业", "论文")):
        return [
            "脑子：会了。手：你再说一遍？",
            "知识从眼前路过，但没有停留。",
            "努力了，努力保持清醒。",
        ]
    if any(word in compact for word in ("吃", "饿", "减肥")):
        return [
            "先吃饱，才有力气减肥。",
            "不是饿，只是嘴有自己的想法。",
            "这一口下去，烦恼少一半。",
        ]
    return [
        f"当我发现：{compact}",
        "表面波澜不惊，内心锣鼓喧天。",
        "我没事，我只是需要缓缓。",
    ]


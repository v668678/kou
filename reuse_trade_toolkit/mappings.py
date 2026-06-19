"""Deterministic multilingual mappings used by the normalizer."""

HEADER_ALIASES = {
    "item_id": {"item_id", "id", "sku", "inventory_id", "商品id", "商品编号", "管理番号", "商品番号", "在庫番号"},
    "category": {"category", "type", "product_type", "分类", "类别", "品类", "カテゴリ", "カテゴリー", "種別", "品目"},
    "brand": {"brand", "maker", "manufacturer", "品牌", "厂商", "制造商", "ブランド", "メーカー", "製造元"},
    "model": {"model", "model_name", "product_name", "型号", "机型", "产品名", "型番", "モデル", "商品名", "車種"},
    "condition": {"condition", "grade", "quality", "成色", "等级", "状态", "状態", "ランク", "グレード", "コンディション"},
    "quantity": {"quantity", "qty", "count", "数量", "台数", "個数", "数量合計"},
    "unit_price": {"unit_price", "price", "cost", "purchase_price", "单价", "价格", "仕入価格", "単価", "価格", "買取価格"},
    "currency": {"currency", "ccy", "币种", "货币", "通貨", "通貨コード"},
    "serial_number": {"serial_number", "serial", "sn", "序列号", "串号", "シリアル", "シリアル番号", "製造番号"},
    "imei": {"imei", "imei1", "端末識別番号", "识别码"},
    "notes": {"notes", "note", "remarks", "comment", "备注", "说明", "備考", "メモ", "コメント"},
}

CATEGORY_ALIASES = {
    "smartphone": {"smartphone", "phone", "mobile phone", "iphone", "android", "スマホ", "スマートフォン", "携帯電話", "手机", "智能手机"},
    "tablet": {"tablet", "ipad", "タブレット", "平板", "平板电脑"},
    "component": {"component", "electronic component", "ic", "chip", "semiconductor", "電子部品", "icチップ", "半導体", "电子元件", "芯片", "集成电路"},
    "vehicle": {"vehicle", "car", "used car", "automobile", "中古車", "自動車", "车辆", "汽车", "二手车"},
}

CONDITION_ALIASES = {
    "NEW": {"new", "unused", "sealed", "新品", "未使用", "未開封", "全新", "未使用品"},
    "A": {"a", "excellent", "like new", "美品", "極美品", "ほぼ新品", "充新", "99新", "95新"},
    "B": {"b", "good", "minor wear", "良品", "中古良品", "軽い傷", "轻微使用", "9成新", "90新"},
    "C": {"c", "fair", "used", "使用感あり", "傷あり", "中古", "明显使用", "8成新", "80新"},
    "D": {"d", "poor", "damaged", "破損", "ジャンク手前", "故障あり", "损坏", "故障"},
    "PARTS": {"parts", "for parts", "junk", "ジャンク", "部品取り", "配件机", "零件", "报废"},
}

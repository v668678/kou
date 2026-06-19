from decimal import Decimal
import unittest

from reuse_trade_toolkit.normalizer import mask_identifier, normalize_category, normalize_condition, normalize_row


class NormalizerTests(unittest.TestCase):
    def test_japanese_headers(self):
        row = {"管理番号": "JP-001", "カテゴリ": "スマホ", "メーカー": "Apple", "型番": "iPhone 14", "ランク": "美品", "台数": "2", "単価": "85,000", "通貨": "JPY"}
        result = normalize_row(row)
        self.assertEqual(result["item_id"], "JP-001")
        self.assertEqual(result["category"], "smartphone")
        self.assertEqual(result["condition"], "A")
        self.assertEqual(result["unit_price"], "85000.00")

    def test_chinese_headers(self):
        row = {"商品编号": "CN-1", "品类": "平板", "品牌": "Apple", "型号": "iPad Air", "成色": "9成新", "数量": "3", "单价": "3200", "币种": "CNY"}
        result = normalize_row(row)
        self.assertEqual(result["category"], "tablet")
        self.assertEqual(result["condition"], "B")

    def test_condition_mapping(self):
        self.assertEqual(normalize_condition("ジャンク"), "PARTS")
        self.assertEqual(normalize_condition("unused"), "NEW")

    def test_category_mapping(self):
        self.assertEqual(normalize_category("ICチップ"), "component")
        self.assertEqual(normalize_category("二手车"), "vehicle")

    def test_masks_identifier(self):
        self.assertEqual(mask_identifier("356789012345678"), "***********5678")

    def test_short_identifier_is_fully_masked(self):
        self.assertEqual(mask_identifier("123"), "***")

    def test_currency_conversion(self):
        row = {"model": "iPhone 13", "category": "phone", "condition": "B", "quantity": "1", "price": "10000", "currency": "JPY"}
        result = normalize_row(row, target_currency="USD", rate=Decimal("0.0064"))
        self.assertEqual(result["unit_price"], "64.00")
        self.assertEqual(result["currency"], "USD")

    def test_missing_model_is_reported(self):
        result = normalize_row({"condition": "A", "quantity": "1", "price": "10"})
        self.assertIn("model is required", result["validation_errors"])

    def test_invalid_quantity_is_reported(self):
        result = normalize_row({"model": "Chip", "condition": "A", "quantity": "zero", "price": "1"})
        self.assertIn("quantity must be an integer", result["validation_errors"])

    def test_unknown_condition_is_reported(self):
        result = normalize_row({"model": "Phone", "condition": "premium", "quantity": "1", "price": "1"})
        self.assertIn("condition is not recognized", result["validation_errors"])


if __name__ == "__main__":
    unittest.main()

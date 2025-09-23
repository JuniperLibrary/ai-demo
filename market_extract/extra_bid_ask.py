import pandas as pd
import json

class TestDataFrame:
    def __init__(self):
        # 模拟数据库查询返回的字段名
        self._columns = [
            'field_group', 'code', 'data_source', 'bid_entry_list', 'ask_entry_list',
            'source_time', 'amount', 'volume', 'last_px', 'last_size',
            'open_px', 'high_px', 'low_px', 'close_px', 'recv_time'
        ]

    def results_to_dataframe(self, results):

        columns = self._columns
        df = pd.DataFrame(results, columns=columns)

        # 解析 bid/ask 前5条
        def parse_entries(entry_str, topn=5):
            if pd.isna(entry_str):
                return []
            try:
                data = json.loads(entry_str)
                return data[:topn]  # 取前5个
            except Exception:
                return []

        bid_data = df['bid_entry_list'].apply(lambda x: parse_entries(x, 5))
        ask_data = df['ask_entry_list'].apply(lambda x: parse_entries(x, 5))

        # 直接保持 [{"price":xxx,"size":xxx}, ...] 格式
        bid_combined = bid_data.apply(lambda lst: json.dumps(lst))
        ask_combined = ask_data.apply(lambda lst: json.dumps(lst))

        final_df = pd.DataFrame({
            'FIELD_GROUP': df['field_group'],
            'CODE': df['code'],
            'SETTLE_TYPE': 'ODM-Matching',
            'DATA_SOURCE': df['data_source'],
            'REAL_TIME_TAKE_OVER': None,
            'COUNTER_PARTY': '',
            'BID_INFO': bid_combined,
            'ASK_INFO': ask_combined,
            'TIME': df['source_time'],
            'AMOUNT': df['amount'],
            'VOLUME': df['volume'],
            'LAST_PX': df['last_px'],
            'LAST_QTY': df['last_size'],
            'OPEN_PX': df['open_px'],
            'HIGH_PX': df['high_px'],
            'LOW_PX': df['low_px'],
            'CLOSE_PX': df['close_px'],
            'RECV_TIME': df['recv_time'],
        })

        return final_df


if __name__ == "__main__":

    # 模拟输入数据（只两行作为例子）
    results = [
        [
            "FG1", "CODE123", "SRC1",
            json.dumps([
                {"price": 100.1, "size": 10},
                {"price": 100.0, "size": 20},
                {"price": 99.9, "size": 30},
                {"price": 99.8, "size": 40},
                {"price": 99.7, "size": 50},
                {"price": 99.6, "size": 60}
            ]),
            json.dumps([
                {"price": 100.2, "size": 15},
                {"price": 100.3, "size": 25},
                {"price": 100.4, "size": 35}
            ]),
            "2025-09-08 12:00:00", 1000000, 500, 100.1, 50,
            99.5, 101.0, 99.0, 100.0, "2025-09-08 12:00:01"
        ],
        [
            "FG2", "CODE456", "SRC2",
            json.dumps([{"price": 200.1, "size": 100}]),
            json.dumps([{"price": 200.5, "size": 120}]),
            "2025-09-08 12:01:00", 2000000, 1000, 200.1, 100,
            199.5, 201.0, 199.0, 200.0, "2025-09-08 12:01:01"
        ]
    ]

    tdf = TestDataFrame()
    df = tdf.results_to_dataframe(results)

    print(df)
    print("\n第一行 BID_INFO 展示：")
    print(df.loc[0, "BID_INFO"])
    print("\n第一行 ASK_INFO 展示：")
    print(df.loc[0, "ASK_INFO"])

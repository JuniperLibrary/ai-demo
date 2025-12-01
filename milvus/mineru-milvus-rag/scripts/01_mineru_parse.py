from mineru import MinerU  # 参考具体包名与接口
m = MinerU()
m.parse_pdf("data/docs/sample.pdf", out_dir="data/parsed", format="json")

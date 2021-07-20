from icrawler.builtin import GoogleImageCrawler

crawler = GoogleImageCrawler(storage={"root_dir": "images"})
crawler.crawl(keyword="ここにダウンロードしたい画像名を入力", max_num=100)

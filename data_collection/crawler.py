"""
Crawler thu thập tin rao bán XE MÁY từ Chợ Tốt Xe (API công khai gateway.chotot.com)
Đồ án môn Khoa học dữ liệu – Minh (thu thập dữ liệu)

Chạy:  python crawler.py            (chạy tất cả các bước, chạy lại được nếu bị ngắt)
       BUDGET=150 python crawler.py (chạy tối đa 150 giây rồi dừng, lần sau chạy tiếp)
Kết quả nằm trong thư mục data/:
  regions.json                    mã tỉnh/thành có tin
  raw/region_<mã>.csv            dữ liệu thô từng tỉnh
  chotot_xemay_raw.csv            gộp tất cả tỉnh, đã bỏ trùng list_id (CHƯA làm sạch)
  mapping.csv                     bảng mã -> tên (hãng, dòng, loại, dung tích, xuất xứ)
  chotot_xemay_named.csv          dữ liệu thô + cột tên đã ánh xạ  -> GIAO CHO BẢO
Không thu thập tên, số điện thoại, ảnh, toạ độ của người bán.
"""
import os, json, time, glob, requests, pandas as pd

URL = "https://gateway.chotot.com/v1/public/ad-listing"
HEAD = {"User-Agent": "Mozilla/5.0 (student project - KHDL)"}
CG = 2020           # danh mục xe máy
SLEEP = 0.8         # nghỉ giữa các request
OUT = "../data/raw"  # chạy từ thư mục data_collection/
BUDGET = float(os.environ.get("BUDGET", "0"))  # giây; 0 = không giới hạn
T0 = time.time()
class OutOfTime(Exception): pass
def check_time():
    if BUDGET and time.time() - T0 > BUDGET:
        raise OutOfTime()
KEEP = ["list_id", "subject", "body", "price", "price_string", "regdate", "mileage_v2",
        "motorbikebrand", "motorbikemodel", "motorbiketype", "motorbikecapacity",
        "motorbikeorigin", "condition_ad", "condition_ad_name", "region_v2", "region_name",
        "area_v2", "area_name", "ward_name", "type", "is_price_not_valid",
        "number_of_images", "list_time", "orig_list_time"]
CODE_COLS = ["motorbikebrand", "motorbikemodel", "motorbiketype", "motorbikecapacity", "motorbikeorigin"]

def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)

def get(params=None, path="", retries=4):
    for i in range(retries):
        try:
            r = requests.get(URL + path, params=params, headers=HEAD, timeout=30)
            if r.status_code == 200:
                return r.json()
            log("HTTP", r.status_code, "-> thử lại")
        except Exception as e:
            log("Lỗi", e, "-> thử lại")
        time.sleep(5 * (i + 1))
    return {}

# ---------- Bước 1: dò mã tỉnh/thành ----------
def discover_regions():
    path = f"{OUT}/regions.json"
    if os.path.exists(path):
        return json.load(open(path, encoding="utf-8"))
    prog = f"{OUT}/regions_progress.json"
    st = json.load(open(prog, encoding="utf-8")) if os.path.exists(prog) else {"regions": {}, "done": []}
    regions = st["regions"]
    for g in range(1, 14):
        for i in range(0, 72):
            code = g * 1000 + i
            if code in st["done"]:
                continue
            if BUDGET and time.time() - T0 > BUDGET:
                json.dump(st, open(prog, "w", encoding="utf-8"), ensure_ascii=False)
                raise OutOfTime()
            st["done"].append(code)
            j = get({"cg": CG, "region_v2": code, "limit": 1})
            ads = j.get("ads", [])
            if ads and ads[0].get("region_v2") == code:
                regions[str(code)] = {"name": ads[0].get("region_name"), "total": j.get("total", 0)}
                log("Tỉnh", code, ads[0].get("region_name"), j.get("total"))
            time.sleep(0.15)
    json.dump(regions, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return regions

# ---------- Bước 2: crawl từng tỉnh ----------
def crawl(params, max_ads=10000, part=None):
    rows, start = [], 0
    if part and os.path.exists(part):
        st = json.load(open(part, encoding="utf-8")); rows, start = st["rows"], st["next"]
    for o in range(start, max_ads, 50):
        if BUDGET and time.time() - T0 > BUDGET:
            json.dump({"rows": rows, "next": o}, open(part, "w", encoding="utf-8"), ensure_ascii=False)
            raise OutOfTime()
        j = get({**params, "cg": CG, "limit": 50, "o": o})
        ads = j.get("ads", [])
        if not ads:
            break
        rows += [{k: a.get(k) for k in KEEP} for a in ads]
        time.sleep(SLEEP)
    if part:  # đánh dấu đã xong để đợt sau không crawl lại
        json.dump({"rows": rows, "next": max_ads}, open(part, "w", encoding="utf-8"), ensure_ascii=False)
    return rows

def crawl_regions(regions):
    os.makedirs(f"{OUT}/raw", exist_ok=True)
    for code, info in sorted(regions.items(), key=lambda x: -x[1]["total"]):
        f = f"{OUT}/raw/region_{code}.csv"
        if os.path.exists(f):
            continue
        log(f"Crawl {info['name']} ({code}) – {info['total']} tin")
        if info["total"] >= 10000:
            # vượt trần 10.000 tin/truy vấn -> chia thêm theo loại xe
            rows = []
            for t in range(1, 6):
                rows += crawl({"region_v2": code, "motorbiketype": t}, part=f"{OUT}/raw/part_{code}_{t}.json")
        else:
            rows = crawl({"region_v2": code}, part=f"{OUT}/raw/part_{code}.json")
        pd.DataFrame(rows).to_csv(f, index=False, encoding="utf-8-sig")
        # file part_*.json là file tạm, có thể xoá tay sau khi crawl xong
        log(f"  -> {len(rows)} tin")

# ---------- Bước 3: gộp + bỏ trùng ----------
def merge():
    df = pd.concat([pd.read_csv(f) for f in glob.glob(f"{OUT}/raw/region_*.csv") if os.path.getsize(f) > 5],
                   ignore_index=True)
    n = len(df)
    df = df.drop_duplicates("list_id")
    df["crawl_date"] = time.strftime("%Y-%m-%d")
    df.to_csv(f"{OUT}/chotot_xemay_raw.csv", index=False, encoding="utf-8-sig")
    log(f"Gộp: {n} dòng, sau bỏ trùng list_id: {len(df)}")
    return df

# ---------- Bước 4: bảng ánh xạ mã -> tên ----------
def build_mapping(df):
    path = f"{OUT}/mapping.csv"
    known = pd.read_csv(path) if os.path.exists(path) else pd.DataFrame(columns=["field", "code", "name"])
    have = set(zip(known["field"], known["code"].astype(str)))
    rows = known.to_dict("records")
    # lấy 1 tin đại diện cho mỗi cặp (hãng, dòng) chưa biết; 1 lần gọi chi tiết cho ra tên cả 5 trường
    df2 = df.dropna(subset=["motorbikebrand"]).copy()
    for c in CODE_COLS:
        df2[c] = df2[c].fillna(-1).astype(int).astype(str)
    need = df2[[not all((c, r[c]) in have for c in CODE_COLS if r[c] != "-1")
                for _, r in df2[CODE_COLS].iterrows()]]
    reps = need.drop_duplicates(["motorbikebrand", "motorbikemodel"])
    log(f"Cần gọi chi tiết {len(reps)} tin để lấy tên")
    for k, (_, r) in enumerate(reps.iterrows()):
        if BUDGET and time.time() - T0 > BUDGET:
            pd.DataFrame(rows).drop_duplicates(["field", "code"]).to_csv(path, index=False, encoding="utf-8-sig")
            raise OutOfTime()
        j = get(path=f"/{int(r['list_id'])}")
        params = {p.get("id"): p.get("value") for p in j.get("parameters", [])}
        for c in CODE_COLS:
            if r[c] != "-1" and (c, r[c]) not in have and params.get(c):
                rows.append({"field": c, "code": r[c], "name": params[c]})
                have.add((c, r[c]))
        if k % 50 == 0:
            pd.DataFrame(rows).to_csv(path, index=False, encoding="utf-8-sig")
            log(f"  mapping {k}/{len(reps)}")
        time.sleep(SLEEP)
    m = pd.DataFrame(rows).drop_duplicates(["field", "code"])
    m.to_csv(path, index=False, encoding="utf-8-sig")
    return m

def apply_mapping(df, m):
    m = m.copy(); m["code"] = m["code"].astype(str)
    for c in CODE_COLS:
        d = dict(zip(m[m.field == c].code, m[m.field == c].name))
        key = df[c].fillna(-1).astype(int).astype(str)
        df[c.replace("motorbike", "") + "_name"] = key.map(d)
    df.to_csv(f"{OUT}/chotot_xemay_named.csv", index=False, encoding="utf-8-sig")
    log(f"Xong: {OUT}/chotot_xemay_named.csv – {len(df)} dòng, {df.shape[1]} cột")

def main():
    os.makedirs(OUT, exist_ok=True)
    regions = discover_regions()
    log(f"{len(regions)} tỉnh/thành, tổng ~{sum(v['total'] for v in regions.values())} tin")
    crawl_regions(regions)
    df = merge()
    m = build_mapping(df)
    apply_mapping(df, m)

if __name__ == "__main__":
    try:
        main()
        print("ALL_DONE")
    except OutOfTime:
        log("Hết thời gian của đợt này – chạy lại lệnh để làm tiếp")

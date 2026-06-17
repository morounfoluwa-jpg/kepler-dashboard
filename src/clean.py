import pandas as pd

def load_and_clean(path="data/kepler_data.csv"):
    df = pd.read_csv(path, comment="#")

    cols = [
        "kepoi_name", "koi_disposition",
        "koi_period",
        "koi_prad",
        "koi_teq",
        "koi_insol",
        "koi_steff",
        "koi_slogg",
    ]
    df = df[[c for c in cols if c in df.columns]].copy()

    df.dropna(subset=["koi_period", "koi_prad", "koi_disposition"], inplace=True)
    df = df[df["koi_disposition"].isin(["CONFIRMED", "CANDIDATE"])]
    df = df[(df["koi_period"] > 0) & (df["koi_prad"] > 0)]

    print(f"Clean dataset: {len(df)} rows")
    return df

if __name__ == "__main__":
    df = load_and_clean()
    df.to_csv("data/kepler_clean.csv", index=False)
    print("Saved to data/kepler_clean.csv")
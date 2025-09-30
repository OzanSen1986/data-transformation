import json
import pandas as pd
from typing import Any, Callable, TypeAlias
from datetime import datetime
from dataclasses import dataclass, field

MetricFn: TypeAlias = Callable[[pd.DataFrame], dict[str, Any]]

@dataclass
class ReportConfig:
    input_file: str
    start_year: int
    end_year: int
    metrics: list[MetricFn] = field(default_factory=list)

def read_file(file: str) -> pd.DataFrame:
    return pd.read_csv(file)

def convert_data_type(df: pd.DataFrame) -> pd.DataFrame:
    df = df.astype({'Year': 'Int32', 'NA_Sales': 'Float32', 'EU_Sales': 'Float32', 'JP_Sales': 'Float32', 'Other_Sales': 'Float32', 'Global_Sales': 'Float32'})
    return df

def filter_games(df: pd.DataFrame, start_year: int | None = None, end_year: str | None = None) -> pd.DataFrame:
    if start_year:
        df = df[df["Year"] >= start_year]
    if end_year:
        df = df[df["Year"] <= end_year]
    return df

def games_count_metric(df: pd.DataFrame) -> dict[str, Any]:
    return {"Number of games": df["Name"].nunique()}

def total_sales_metric(df: pd.DataFrame) -> dict[str, Any]:
    return {"Total Sales by region": df[df["EU_Sales"] + df["NA_Sales"] + df["EU_Sales"] + df["JP_Sales"] + df["Global_Sales"]].sum()}

def average_sales_metric(df: pd.DataFrame) -> dict[str, Any]:
    sales = df[df["EU_Sales"] + df["NA_Sales"] + df["EU_Sales"] + df["JP_Sales"] + df["Global_Sales"]]
    avg = sales.mean() if not sales.empty else 0.0
    return {"Average sales value of games": round(avg, 2)}

def pct_by_genre_metric(df: pd.DataFrame, game_type: str = "Shooter") -> dict[str, Any]:
     # Fixed: convert Series to regular Python dict
    if df.empty:
        return {"pct_per_genre": {}}
    genre_counts = df["Genre"].value_counts(normalize=True) * 100
    # Convert to regular Python dict with float values
    genre_dict = {str(genre): round(float(percentage), 2) for genre, percentage in genre_counts.items()}
    return {"pct_per_genre": genre_dict}
    
def generate_report_data(df: pd.DataFrame, config: ReportConfig) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for metric in config.metrics:
        result.update(metric(df))
    
    result["report_start_year"] = (
        config.start_year if config.start_year else "N/A"
    )
    result["report_end_year"] = (
        config.end_year if config.end_year else "N/A"
    )
    return result

def write_report(data: dict[str, Any], filename: str):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    

def main() -> None:
    config = ReportConfig(
        input_file="vgsales.csv",
        start_year=2023,
        end_year= 2024,
        metrics=[
            games_count_metric,
            total_sales_metric,
            average_sales_metric,
            pct_by_genre_metric,
        ],
    )

    df = read_file(config.input_file)
    df = convert_data_type(df)
    df = filter_games(df, config.start_year, config.end_year)
    report_data = generate_report_data(df, config)
    write_report(report_data, "games_sales_report.json")

if __name__ == "__main__":
    main()
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

# df = pd.read_csv('vgsales.csv', index_col='Rank')
# df.rename(columns={'EU_Sales':'SalesInEurope', 'JP_Sales': 'SalesInJapan'}, inplace = True)
def read_file(file: str) -> pd.DataFrame:
    return pd.read_csv(file)

def convert_data_type(df: pd.DataFrame) -> pd.DataFrame:
    df = df.astype({'Year': 'Int32'})
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

def pct_by_genre_metric(df: pd.DataFrame, game_type: str) -> dict[str, Any]:
    total = df[df["Genre"] == game_type]
    pct = (len(total) / len(df)) * 100 if len(df) > 0.0 else 0.0
    return {"pct per genre": round(pct, 2)}
    
def generate_report_data(df: pd.DataFrame, config: ReportConfig) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for metric in config.metrics:
        result.update(df(metric))
    
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
        end_date=2024,
        metrics=[
            games_count_metric,
            total_sales_metric,
            average_sales_metric,
            pct_by_genre_metric,
        ],
    )

    df = read_file(config.input_file)
    df = filter_games(df, config.start_year, config.end_year)
    report_data = generate_report_data(df, config)
    write_report(report_data, "games_sales_report.json")

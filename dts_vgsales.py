import json
import pandas as pd
from collections.abc import Callable
from typing import Any, Literal
from datetime import datetime
from dataclasses import dataclass, field

MetricFn:Callable[[pd.DataFrame], dict[str, Any]]

@dataclass
class ReportConfig:
    input_file: str
    start_year: int
    end_year: int
    metrics: list["MetricFn"] = field(default_factory=list)

def read_file(file: str) -> pd.DataFrame:
    return pd.read_csv(file)

def convert_data_type(df: pd.DataFrame) -> pd.DataFrame:
    df = df.astype({'Year': 'Int32'})
    return df

def filter_games(df: pd.DataFrame, start_year: int | None = None, end_year: int | None = None) -> pd.DataFrame:
    df = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]
    return df

def games_count_metric(df: pd.DataFrame) -> dict[str, Any]:
    return {"Number of games": df["Name"].nunique()}

def total_sales_metric(df: pd.DataFrame) -> dict[str, Any]:
    return {"Total Sales": round(df[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]].sum().sum(),2)}

def average_sales_metric(df: pd.DataFrame) -> dict[str, Any]:
    sales = df[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]].sum()
    avg = sales.mean()
    return {"Average sales value of games": round(avg, 2)}

def pct_by_genre_metric(df: pd.DataFrame, game_type: str = "Shooter") -> dict[str, Any]:
    if df.empty:
        return {"pct_per_genre": {}}
    genre_counts = len(df[df["Genre"] == game_type])
    return {"pct_per_genre": round((genre_counts/len(df))*100,2)}
    
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
        start_year=2012,
        end_year= 2012,
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
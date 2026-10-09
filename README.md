# Residential Construction Growth in Kyrgyzstan: Regional Patterns and Geographic Concentration, 2021 to 2025

**Reproducibility package for the manuscript by Aruuke Bayakmatova, NYU Tandon School of Engineering**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23250551.svg)](https://doi.org/10.5281/zenodo.23250551)

## Overview

This repository contains the preserved source data, processed analytical dataset, Python analysis code, figures, and analytical workbook supporting a descriptive study of commissioned residential floor area across the nine territories reported by the National Statistical Committee of the Kyrgyz Republic: seven regions, Bishkek City, and Osh City.

The analysis covers 2021 through 2025. It measures the reconstructed national total, territory level growth, changes in regional shares, and concentration across the reported territorial units using the Herfindahl Hirschman index, or HHI. A sensitivity analysis combines Bishkek City with Chui Region and Osh City with Osh Region to reduce the effect of transfers within those paired units during the 2024 administrative territorial reform.

When run with the processed population dataset as shown below, the Python script reproduces the principal calculations from the preserved source extract, performs validation and robustness checks, generates the quantitative analytical tables as CSV files, and generates all six figures in PNG format.

**Project DOI for all Zenodo versions:** <https://doi.org/10.5281/zenodo.23250551>

**Archived Version 1.0.0:** <https://doi.org/10.5281/zenodo.23250552>

Version 1.0.0 is an immutable archived snapshot. The current `main` branch may contain documentation or metadata improvements made after that release. For exact reproduction of Version 1.0.0, use the version specific DOI above. If a later release becomes the version used for the final manuscript, cite that later version specific DOI instead.

**Manuscript status:** In preparation.

## Key results

| Measure | Result |
| --- | --- |
| Reconstructed national commissioned floor area | 1.313 million m² in 2021 to 1.820 million m² in 2025 |
| Overall growth | 38.6% |
| Compound annual growth rate | 8.5% |
| Largest absolute increase | Bishkek City, +268.4 thousand m² |
| Bishkek contribution to the reconstructed national increase | 53.0% |
| Territories below their 2021 level in 2025 | Naryn Region and Osh Region |
| Bishkek share of the reconstructed national total | 26.5% to 33.9% |
| Osh Region share of the reconstructed national total | 18.1% to 11.3% |
| HHI, nine territories | 0.1577 in 2021 to 0.1888 in 2025, with a peak of 0.1919 in 2024 |
| HHI, seven merged units | 0.2580 in 2021 to 0.2934 in 2025 |

Concentration increased between 2021 and 2025 within both territorial specifications. The nine territory series reached its highest HHI in 2024, while the seven unit sensitivity specification did not reproduce that 2024 peak.

Because the two specifications contain different numbers of units, their raw HHI levels should not be compared directly. The sensitivity analysis focuses on change over time within each specification. The generated `hhi_comparison.csv` also contains normalized HHI values that adjust for the number of units.

## Repository structure

```text
Residential-Construction-Growth-in-Kyrgyzstan-2021-to-2025/
├── data/
│   ├── raw/
│   │   └── kyrgyzstan_residential_construction_raw.json
│   └── processed/
│       └── kyrgyzstan_residential_construction_clean.csv
├── results/
│   ├── figures/
│   │   ├── figure1_national_total.pdf
│   │   ├── figure1_national_total.png
│   │   ├── figure2_territory_2021_vs_2025.pdf
│   │   ├── figure2_territory_2021_vs_2025.png
│   │   ├── figure3_index_small_multiples.pdf
│   │   ├── figure3_index_small_multiples.png
│   │   ├── figure4_regional_shares.pdf
│   │   ├── figure4_regional_shares.png
│   │   ├── figure5_hhi.pdf
│   │   ├── figure5_hhi.png
│   │   ├── figure6_per_1000_residents.pdf
│   │   └── figure6_per_1000_residents.png
│   └── kyrgyzstan_residential_construction_analysis.xlsx
├── scripts/
│   └── reproduce_analysis.py
├── .gitignore
├── CITATION.cff
├── LICENSE
├── README.md
└── requirements.txt
```

The tracked PDF figures are companion vector versions of the figures. The current reproduction script generates PNG figures and CSV analytical tables. It does not generate the PDF files or the Excel workbook.

The Excel workbook provides an additional auditable analytical package containing preserved and cleaned data, validation and source logs, national and regional summaries, population analysis, sensitivity analysis, HHI comparisons, robustness results, contribution decomposition, and literature documentation.

## Data sources

| Dataset or source | Source | Access information |
| --- | --- | --- |
| Dwelling houses by territory, thousand m² | National Statistical Committee of the Kyrgyz Republic: <https://stat.gov.kg/en/opendata/category/103/> | Accessed 2 October 2026 |
| Machine readable construction data | <https://stat.gov.kg/en/opendata/category/103/json> | Preserved as the raw JSON file in this repository |
| Resident population at start of year | National Statistical Committee: <https://www.stat.gov.kg/en/opendata/category/39/> | Accessed 2 October 2026 |
| Construction statistics, methodology, and annual releases | <https://stat.gov.kg/en/statistics/stroitelstvo/> | Used for definitions, methodological context, and revision checks |
| Administrative territorial reform context | Bishkek City Mayor's Office: <https://www.bishkek.gov.kg/ru/post/29825> | Used to document implementation of the 2024 reform |

The National Statistical Committee states that its open data are published under the Creative Commons Attribution NonCommercial ShareAlike 4.0 International license, commonly abbreviated CC BY NC SA 4.0.

License information: <https://creativecommons.org/licenses/by-nc-sa/4.0/>

### Preserved source extract

The raw JSON contains nine reported territories and five annual observations for each territory from 2021 through 2025.

The exact unit string stored in the source JSON is:

```text
thous. sq.m.
```

SHA 256 of the preserved JSON used in this repository:

```text
77c509a21af72285eff05fd76e9f1c76092b4c042323aa7ea25aacc8e3be0ac5
```

The reproduction script prints this hash when it runs so that the source extract can be checked against the archived file.

### Variable definitions

The primary variable is **commissioned residential floor area**, measured in thousands of square meters of total area. The National Statistical Committee source is titled *Dwelling houses by territory*. The associated construction metadata describe commissioning of residential houses and dormitories.

The variable measures residential floor area placed into service. It is not a measure of building permits, housing starts, investment expenditure, sales, prices, or the existing housing stock.

Values in the preserved source extract were retained as published in the accessed data vintage. No interpolation or correction was applied.

The processed dataset contains 45 territory year observations and these fields:

```text
year
region
residential_thousand_sqm
residential_sqm
national_total_sqm
regional_share_pct
annual_growth_pct
regional_growth_2021_2025_pct
cagr_2021_2025_pct
regional_share_change_pp
index_2021
hhi
population_thousand
population
residential_sqm_per_1000_residents
```

The 2021 annual growth field is undefined because there is no preceding year in the study period.

Population normalized results are exploratory and do not affect the four principal research questions.

## Reproducing the analysis

Use a compatible Python 3 environment. The repository currently pins package versions in `requirements.txt` but does not pin the Python interpreter version.

From the repository root, create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows, activate it with:

```text
.venv\Scripts\activate
```

Install the pinned dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the analysis with explicit paths:

```bash
python scripts/reproduce_analysis.py data/raw/kyrgyzstan_residential_construction_raw.json reproduction_output data/processed/kyrgyzstan_residential_construction_clean.csv
```

The output directory does not need to exist beforehand because the script creates it.

Explicit paths are used because the script's internal default filenames do not point to the repository's `data/raw` and `data/processed` directories.

The third argument supplies the processed dataset containing the population series used for the exploratory population normalized analysis and Figure 6. If that file is not supplied or cannot be found, the population outputs and Figure 6 are not generated.

The script performs the following operations:

1. Prints the SHA 256 hash of the preserved JSON source extract and the installed pandas and NumPy versions.

2. Checks the source unit, 45 construction observations, nine territories, the five required years, and the absence of missing or nonpositive construction values.

3. Reconstructs annual national totals by summing the nine territorial observations.

4. Computes annual national growth, overall growth, national CAGR, regional endpoint growth, regional CAGR, regional shares, share changes, territory contributions to national change, HHI, and normalized HHI.

5. Performs robustness checks using two year averages, the coefficient of variation across territories, and the largest year to year log changes.

6. Performs the boundary reform sensitivity analysis by combining Bishkek City with Chui Region and Osh City with Osh Region.

7. Generates six PNG figures when the population input is available.

8. Generates population normalized outputs when the processed population dataset is supplied.

### Script generated outputs

The script writes these CSV files into the specified output directory:

| File | Content |
| --- | --- |
| `table2_territory_year.csv` | Territory by year commissioned floor area |
| `table3_regional.csv` | Endpoint growth, CAGR, shares, share changes, and contribution to national change |
| `national_summary_v2.csv` | Reconstructed national totals, annual growth, HHI, normalized HHI, and largest territorial share |
| `hhi_comparison.csv` | HHI and normalized HHI for the nine territory and seven merged unit specifications |
| `sensitivity_city_region.csv` | Results after combining each major city with its surrounding region |
| `robustness_two_year_avg.csv` | 2021 and 2022 averages compared with 2024 and 2025 averages |
| `tableA1_population_thousand.csv` | Resident population by territory and year |
| `exploratory_sqm_per_1000.csv` | Commissioned floor area per 1,000 residents |

The script also generates these PNG files when the required inputs are present:

```text
figure1_national_total.png
figure2_territory_2021_vs_2025.png
figure3_index_small_multiples.png
figure4_regional_shares.png
figure5_hhi.png
figure6_per_1000_residents.png
```

The PDF versions stored under `results/figures/` are companion vector files and are not generated by the current reproduction script.

The Excel workbook under `results/` is also a companion analytical file rather than a direct script output.

## Figures

| Figure | Content |
| --- | --- |
| 1 | Reconstructed national commissioned residential floor area, 2021 to 2025 |
| 2 | Commissioned floor area by territory, 2021 versus 2025 |
| 3 | Regional growth index with 2021 equal to 100, one panel per territory |
| 4 | Each territory's share of the reconstructed national total |
| 5 | HHI for nine territories and seven merged units |
| 6 | Exploratory commissioned floor area per 1,000 residents |

Figure 5 includes a reference line at 1/9, the theoretical minimum HHI for nine equally sized territorial shares. That reference applies only to the nine territory specification. The theoretical minimum for seven equally sized units is 1/7 and is not shown on the figure.

Because the number of units differs, the raw HHI levels of the nine territory and seven unit specifications should not be interpreted as directly comparable concentration levels. Changes over time within each specification are the primary sensitivity comparison.

Figure 6 marks 2024 because territorial boundary changes affect interpretation of both the construction numerator and population denominator.

## Notes and limitations

### 2024 administrative territorial reform

Kyrgyzstan implemented a major administrative territorial reform in 2024. Official municipal reporting during implementation in August 2024 stated that the number of administrative territorial units was reduced from 484 to 268 and that 14 cities were enlarged, including Bishkek and Osh.

Several related laws and implementation dates were involved in the reform. This repository therefore treats 2024 as the reform year and does not assign one effective date to the entire reform.

### Population boundaries

The population observations used for 2024 and 2025 reflect the post reform territorial structure. The series shows substantial discontinuities around the reform for Bishkek City, Osh City, Chui Region, and Osh Region.

### Construction boundary consistency

The construction open data source does not document whether the 2021 through 2023 territorial observations were retrospectively recast to the later boundaries. Territory level comparisons spanning the reform should therefore be interpreted cautiously.

### Sensitivity specification

The seven unit analysis combines Bishkek City with Chui Region and Osh City with Osh Region. Transfers within those two pairs cancel in the combined totals. This reduces sensitivity to transfers between each city and its surrounding region, but it does not reconstruct fully constant historical boundaries and does not correct for every possible boundary change elsewhere.

### Data vintage and official revisions

The analysis is tied to the preserved National Statistical Committee open data extract accessed on 2 October 2026.

The nine territorial values in that extract sum to 1,573.4 thousand m² for 2024. An earlier National Statistical Committee publication reported a lower national 2024 value of 1,365.1 thousand m². A subsequent January through December 2025 release reports 1,819.9 thousand m² for 2025 and 115.7% relative to its 2024 comparison level, which implies a 2024 baseline of approximately 1,573 thousand m² and is consistent with the later open data extract.

This indicates that the 2024 statistical series was subsequently revised, reclassified, or otherwise updated. The open data page does not document the precise reason for the difference. This study therefore uses the preserved 2 October 2026 data vintage consistently and does not treat the earlier 2024 publication as interchangeable with the later extract.

### National totals

The national totals reported in this repository are reconstructed by summing the nine territorial observations in the preserved extract. They were not independently reconciled with a separately published national series. For this reason, the README uses the term **reconstructed national total** where precision matters.

### Individual housing

Broader National Statistical Committee construction statistics include substantial individual residential construction. However, the category 103 territorial open data table used here does not separately identify individual housing versus other commissioned residential housing. This study therefore analyzes total commissioned residential floor area and does not decompose it by builder, ownership, or financing type.

### Official revisions

Official statistical series may be revised after initial publication. Exact reproduction of this analysis should use the preserved JSON extract archived with the repository rather than a later version of the live web table.

### Population normalization

The square meters per 1,000 residents measure is exploratory because the 2024 reform affects territorial comparability in both the construction numerator and the population denominator.

### Scope

This is a descriptive study. It makes no causal or statistical significance claims. The HHI measures concentration across the reported territorial units but does not incorporate geographic distance, adjacency, or spatial interaction.

## How to cite

For the exact archived Version 1.0.0 package:

> Bayakmatova, A. (2026). *Residential Construction Growth in Kyrgyzstan, 2021 to 2025* (Version v1.0.0) [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.23250552

For the project across all current and future Zenodo versions:

<https://doi.org/10.5281/zenodo.23250551>

Citation metadata is also provided in `CITATION.cff`.

When the associated research article is published, cite the article separately as well. If a later repository release becomes the final reproducibility package used by the article, update the article and this section to cite that release's version specific DOI.

## License

**Original analysis code:** The Python code authored for this repository, including `scripts/reproduce_analysis.py`, is licensed under the MIT License. The root `LICENSE` file is intended to apply to that original software code.

**Source data:** National Statistical Committee of the Kyrgyz Republic open data are published under the Creative Commons Attribution NonCommercial ShareAlike 4.0 International license, or CC BY NC SA 4.0.

**Derived materials:** The processed dataset, derived tables, figures, and analytical workbook incorporate or are derived from National Statistical Committee data. Reuse should comply with the National Statistical Committee source license where that license applies, including applicable attribution, noncommercial, and share alike requirements.

The MIT software license does not replace, override, or relicense third party source data.

## Contact

Aruuke Bayakmatova  
NYU Tandon School of Engineering

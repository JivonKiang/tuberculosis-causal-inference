---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 26b1781be07ad8aded48426f78a59067_673c9bea6a2611f1a99c5254007bceed
    ReservedCode1: KxX0RlPEufiFaspQwPm/FxqemdtGnPgsBwhhvbl4va7/56gpI3ws8LoGSfUXZ7Y7t2JboOlF3l7NUzb1YaXc8Q8MLAGYFRuVErljeKKvCFEEf4qZy0eCLng3gbdd9mfyeUS9fTB2yw0GT9pcntpEuo0jWVBZv7c12R+1kUTsyvbWUbxvtjrJdlr9RvQ=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 26b1781be07ad8aded48426f78a59067_673c9bea6a2611f1a99c5254007bceed
    ReservedCode2: KxX0RlPEufiFaspQwPm/FxqemdtGnPgsBwhhvbl4va7/56gpI3ws8LoGSfUXZ7Y7t2JboOlF3l7NUzb1YaXc8Q8MLAGYFRuVErljeKKvCFEEf4qZy0eCLng3gbdd9mfyeUS9fTB2yw0GT9pcntpEuo0jWVBZv7c12R+1kUTsyvbWUbxvtjrJdlr9RvQ=
---

# Tuberculosis Causal Inference | 结核病因果推断

Repository for causal inference research on tuberculosis burden, incidence determinants, and risk factor attribution.

## Data Sources

### 1. WHO vs GBD Comparison (`data/who_gbd/`)
- **master_data.csv**: 217 countries with WHO-reported vs GBD-estimated TB incidence rates, including ratio and difference metrics.

### 2. TB Diagnosis Data (`data/diagnosis/`)
- **DiagnosisStats.xlsx**: AI-assisted TB diagnosis performance statistics
- Clinical bacterial datasets for deep learning in M-ROSE

### 3. GBD 2021 Raw Data (`data/gbd_raw/`)
- **incidence/**: Age-standardized TB incidence rates (GBD 2021)
- **prevalence/**: Age-standardized TB prevalence rates (ASPR)
- **dalys/**: TB-attributable DALYs

### 4. NHANES Survey Data (`data/nhanes/`)
Individual-level survey data tables for TB-related analyses.

### 5. World Bank Indicators (`data/external/worldbank_*/`)
10 categories of country-level covariates for causal inference:

| Indicator | Code | Relevance |
|-----------|------|-----------|
| TB Incidence | SH.TBS.INCD | Outcome validation |
| GDP per Capita | NY.GDP.PCAP.CD | Economic determinant |
| Health Expenditure | SH.XPD.CHEX.PC.CD | Health system capacity |
| Population | SP.POP.TOTL | Denominator/offset |
| HIV Prevalence | SH.DYN.AIDS.ZS | Key TB risk factor |
| Diabetes Prevalence | SH.STA.DIAB.ZS | TB comorbidity |
| Smoking Prevalence | SH.PRV.SMOK | Behavioral risk factor |
| Undernourishment | SN.ITK.DEFC.ZS | Nutritional determinant |
| Urban Population | SP.URB.TOTL.IN.ZS | Urbanization confounder |
| GINI Index | SI.POV.GINI | Inequality measure |

### 6. WHO Global TB Report 2025 (`data/external/who_tb_report_2025/`)
- **tb.rda**: Comprehensive TB burden estimates (R format)
- **finance.rda**: TB financing data
- **sty.rda**: TB strategy and policy data
- **drroutine.rda**: Drug resistance surveillance

## Causal Inference Framework

### Potential Research Questions
1. Causal effect of GDP/health expenditure on TB incidence
2. TB burden variance attribution: HIV vs undernourishment
3. Causal pathway: urbanization to crowding to TB incidence
4. Health expenditure causal effect on TB mortality
5. WHO vs GBD incidence divergence: covariate decomposition

### Methodological Approaches
- Instrumental Variables
- Difference-in-Differences
- Mendelian Randomization
- Mediation Analysis
- Panel Fixed Effects
- Propensity Score Matching
- Synthetic Control
*（内容由AI生成，仅供参考）*

# 🧬 NGS Automated Pipeline (`ngs-pipeline-automation`)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Conda](https://img.shields.io/badge/conda-bioconda-green?style=flat&logo=anaconda)](https://bioconda.github.io/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-blue.svg)](https://github.com/dariolobo/ngs-pipeline-automation)

An end-to-end, modular Next-Generation Sequencing (NGS) data processing pipeline developed in Python. This tool automates the entire workflow from raw paired-end FASTQ quality control, genome alignment, and SAM/BAM post-processing to generating consolidated MultiQC reports.

---

## ✨ Key Features

* 🧩 **Modular Architecture**: Clean separation of core steps into independent, reusable Python modules.
* ⚡ **Automated Quality Control**: Integrates `fastp` for ultrafast FASTQ pre-processing, adapter trimming, and quality filtering.
* 🎯 **Splice-Aware / Genome Alignment**: Employs `HISAT2` for high-throughput paired-end read mapping against reference genomes.
* 🛠️ **Streamlined SAM/BAM Processing**: Leverages `samtools` for automated SAM-to-BAM conversion, coordinate sorting, and index generation (`.bai`).
* 📊 **Consolidated Reporting**: Automatically aggregates QC metrics and alignment logs into an interactive HTML report via `MultiQC`.

---

## 🔄 Pipeline Workflow

```text
[ Raw Reads (R1/R2 FASTQ) ]
            │
            ▼
┌─────────────────────────────────────────┐
│ Module 1: Quality Control & Filtering   │ ➔ fastp (Trimmed FASTQ & QC JSON/HTML)
└────────────────────┬────────────────────┘
            │
            ▼
┌─────────────────────────────────────────┐
│ Module 2: Genome Alignment              │ ➔ HISAT2 (SAM alignment file)
└────────────────────┬────────────────────┘
            │
            ▼
┌─────────────────────────────────────────┐
│ Module 3: Post-Processing               │ ➔ samtools (Sorted BAM & BAI index)
└────────────────────┬────────────────────┘
            │
            ▼
┌─────────────────────────────────────────┐
│ Module 4: Consolidated Reporting        │ ➔ MultiQC (Interactive HTML Report)
└─────────────────────────────────────────┘
```

---

## 📁 Repository Structure

```text
ngs-pipeline-automation/
├── .gitignore               # Ignores heavy genomic data (*.fastq, *.bam) and outputs
├── environment.yml          # Conda environment file with all dependencies
├── main_pipeline.py         # Primary CLI orchestrator script
├── README.md                # Project documentation
└── modules/                 # Core modular execution scripts
    ├── __init__.py          # Package initialization
    ├── module_1_qc_filter.py        # Quality control & adapter trimming
    ├── module_2_alignment.py        # HISAT2 alignment execution
    ├── module_3_post_processing.py  # SAM to Sorted BAM processing
    └── module_4_reporting.py        # Consolidated MultiQC generation
```

---

## ⚙️ Installation & Environment Setup

### Prerequisites

* [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/)
* **Supported OS**: Linux or macOS.
* **Windows Users**: Must run via **WSL2** (Windows Subsystem for Linux - Ubuntu).

### 1. Clone the Repository

```bash
git clone [https://github.com/dariolobo/ngs-pipeline-automation.git](https://github.com/dariolobo/ngs-pipeline-automation.git)
cd ngs-pipeline-automation
```

### 2. Create and Activate the Conda Environment

Use the provided `environment.yml` to automatically install Python, `fastp`, `hisat2`, `samtools`, and `multiqc`:

```bash
conda env create -f environment.yml
conda activate ngs-pipeline
```

---

## 🚀 Usage

Run the main pipeline by specifying the input paired-end FASTQ files, reference genome index prefix, and output directory:

```bash
python main_pipeline.py \
  -1 data/sample_R1.fastq.gz \
  -2 data/sample_R2.fastq.gz \
  -x genome/hisat2_index/genome_prefix \
  -o pipeline_results \
  -t 8
```

### Command-Line Arguments

| Argument | Short | Required | Default | Description |
| :--- | :---: | :---: | :---: | :--- |
| `--read1` | `-1` | **Yes** | — | Path to Raw Forward (R1) FASTQ file |
| `--read2` | `-2` | **Yes** | — | Path to Raw Reverse (R2) FASTQ file |
| `--index` | `-x` | **Yes** | — | Path prefix to the HISAT2 reference genome index |
| `--outdir` | `-o` | No | `pipeline_results` | Main output directory for pipeline results |
| `--threads` | `-t` | No | `4` | Number of CPU threads to allocate |

---

## 📂 Output Structure

Upon successful execution, the output directory will contain structured subdirectories for each pipeline stage:

```text
pipeline_results/
├── 01_qc/                 # Cleaned FASTQ files and fastp HTML/JSON reports
├── 02_alignment/          # Raw alignment SAM file
├── 03_processed_bam/      # Coordinate-sorted BAM file and .bai index
└── 04_reports/            # Consolidated MultiQC interactive HTML report
```

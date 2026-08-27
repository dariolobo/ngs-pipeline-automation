import argparse
import subprocess
import sys
from pathlib import Path 

def run_command(cmd: str) -> str:
    """
    Executes a system shell command and handles execution errors.
    """
    print(f"[EXEC]: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR]: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return result.stdout

def run_quality_filter(
        read1: str,
        read2: str,
        output_dir: str,
        min_phred: int = 20,
        min_length: int = 50
) -> tuple[Path, Path]:
    """
    Performs automated quality filtering and generates metric reports.

    Returns:
        tuple[Path, Path]: Paths to filtered R1 and R2 FASTQ files
    """
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    filtered_r1 = out_path / "clean_R1.fastq.gz"
    filtered_r2 = out_path / "clean_R2.fastq.gz"
    json_report = out_path / "qc_metrics.json"
    html_report = out_path / "qc_metrics.html"

    # Run fastp for quality score filtering and adapter removal
    fastp_cmd = (
        f"fastp -i {read1} -I {read2} "
        f"-o {filtered_r1} -O {filtered_r2} "
        f"--qualified_quality_phred {min_phred} "
        f"--length_required {min_length} "
        f"-j {json_report} -h {html_report}"
    )

    run_command(fastp_cmd)
    print(f"[SUCCESS] Module 1 completed. Clean files generated in: {out_path}")

    return filtered_r1, filtered_r2

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Module 1: Automated NGS Quality Control & Filtering"
    )
    parser.add_argument("-1", "--read1", required=True, help="Path to input R1 FASTQ file")
    parser.add_argument("-2", "--read2", required=True, help="Path to input R2 FASTQ file")
    parser.add_argument("-o", "--outdir", default="01_qc_output", help="Output directory")
    parser.add_argument("-q", "--phred", type=int, default=20, help="Minimum Phred quality score (default: 20)")
    parser.add_argument("-l", "--minlen", type=int, default=50, help="Minimum read length required (default: 50)")

    args = parser.parse_args()
    run_quality_filter(args.read1, args.read2, args.outdir,args.phred, args.minlen)

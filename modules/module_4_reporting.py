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

def run_reporting(input_dir: str, output_dir: str) -> Path:
    """
    Generates a consolidated MultiQC report from all pipeline output logs.

    Returns:
        Path: Path to the output directory containing the HTML report.
    """
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    # MultiQC scans the main output directory to aggregate all tool logs
    multiqc_cmd = f"multiqc {input_dir} -o {out_path} --force"

    run_command(multiqc_cmd)
    print(f"[SUCCESS] Module 4 completed. MultiQC report generated in: {out_path}")

    return out_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Module 4: Automated Multi QC Report Generation"
    )
    parser.add_argument("-i", "--input", required=True, help="Input directory containing pipeline logs")
    parser.add_argument("-o", "--outdir", default="04_reports_output", help="Output directory for reports")

    args = parser.parse_args()
    run_reporting(args.input, args.outdir)